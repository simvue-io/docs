import pathlib
import jinja2
import re
import yaml
import inspect
import click

# Import objects we want to document
from simvue import Client, Run
from simvue.api.objects import (
    Run as RunObject,
    Metrics,
    Events,
    Artifact,
    FileArtifact,
    ObjectArtifact,
    Stats,
    Storage,
    S3Storage,
    FileStorage,
)


def format_annotation(annotation) -> str:
    """Convert annotation to string representation

    Parameters
    ----------
    annotation
        annotation to convert

    Returns
    -------
    str
        annotation as type string
    """
    if annotation is None:
        return "None"
    try:
        if annotation.__name__ in ("str", "int", "bool", "float"):
            return annotation.__name__
    except AttributeError:
        pass
    return f"{annotation}".replace("typing.", "").replace("Type", "")


def parse_numpydoc(
    func_name: str, input_text: str, signature: inspect.Signature | None
) -> dict[str, str | list[str] | dict | None]:
    """Parse the Numpydoc docstring

    Parameters
    ----------
    func_name : str
        current method name
    input_text : str
        docstring
    signature : inspect.Signature | None
        method signature

    Returns
    -------
    dict[str, str | list[str] | dict | None]
        parsed content
    """
    if not input_text:
        return {}

    log_section: str = "description"

    description: list[str] = []
    returns: list[str] = []
    yields: list[str] = []
    raises: list[str] = []
    examples: list[str] = []
    params: dict[str, dict[str, str | None]] = {}
    indent_level: int | None = None

    for i, line in enumerate(lines := input_text.splitlines()):
        if "Parameters" in line:
            log_section = "parameters"
            continue
        if "Returns" in line:
            log_section = "returns"
            continue
        if "Yields" in line:
            log_section = "yields"
            continue
        if "Raises" in line:
            log_section = "raises"
            continue
        if "Examples" in line:
            log_section = "examples"
            continue
        line = re.sub(r"-{3,}", "", line)

        if not line.strip():
            continue

        if log_section == "parameters":
            current_indent_level = len(line) - len(line.lstrip())
            if not indent_level:
                indent_level = current_indent_level
            if re.findall(r"^\s*[\w\d\_]+\s*:\s*.+", line) and (
                current_indent_level <= indent_level
            ):
                name, type_var = (i.strip() for i in line.split(":"))
                default_str = None
                annotation = None

                if signature:
                    if name not in signature.parameters:
                        if not name.startswith("*"):
                            raise ValueError(
                                f"Unknown parameter '{name}' in docstring for '{func_name}'"
                            )
                        annotation = type_var.strip()
                        if name.startswith("*"):
                            name = name.replace("*", "")
                            name = f"_{name}_"
                    elif (
                        default := signature.parameters[name].default
                    ) != inspect._empty:
                        default_str = f"{default}"
                    else:
                        default_str = None

                    if name in signature.parameters:
                        annotation = format_annotation(
                            signature.parameters[name].annotation
                        )

                params[name] = {
                    "type": annotation,
                    "description": "",
                    "default": default_str,
                }
            else:
                if line.strip().startswith("*") and "-" in line:
                    line_components = line.replace("*", "").split("-")
                    line = f"&emsp;`{line_components[0].strip()}` - {line_components[1].strip()}"
                    params[name]["description"] += f"{line}<br>"
                elif line.startswith(" "):
                    line_components = line.strip()
                    params[name]["description"] += f"{line}<br>"
        elif log_section == "returns":
            returns.append(line.strip())
        elif log_section == "yields":
            yields.append(line.strip())
        elif log_section == "raises":
            raises.append(line.strip())
        elif log_section == "examples":
            current_indent_level = len(line) - len(line.lstrip())
            examples.append(
                f"{(current_indent_level - indent_level) * ' '}{line.strip()}"
            )
        else:
            if re.findall(r"={3,}", line):
                continue
            elif i < len(lines) - 1 and re.findall(r"={3,}", lines[i + 1]):
                line = f"\n#### {line}"
            description.append(line)

    return {
        "description": description or None,
        "returns": returns or None,
        "raises": raises or None,
        "parameters": params or None,
        "yields": yields or None,
        "examples": examples or None,
    }


def create_markdown(
    name: str,
    docstring: str,
    signature: inspect.Signature | None,
    is_property: bool,
    sub_name: str | None = None,
    sub_label: str | None = None,
) -> str:
    """Create markdown text from jinja2 template

    Parameters
    ----------
    name : str
        name of method to document
    docstring : str
        docstring for this method
    signature : inspect.Signature | None
        signature of this method
    is_property : bool
        if the method is a class property
    sub_name: str | None, optional
        extra name
    sub_label: str | None, optional
        any additional info

    Returns
    -------
    str
        documentation in markdown
    """
    template_file = pathlib.Path(__file__).parent.joinpath("code_entry_markdown.jinja")
    template = jinja2.Template(template_file.open().read())
    metadata = parse_numpydoc(name, docstring, signature)

    return template.render(
        metadata=metadata,
        function_name=name.replace("_", "\\_"),
        is_property=is_property,
        sub_name=sub_name or "",
        sub_label=sub_label,
    )


@click.command
@click.argument("output_dir", type=click.Path(exists=True))
@click.argument("mkdocs_cfg", type=click.Path(exists=True))
def create_client_docs(output_dir: str, mkdocs_cfg: str) -> None:
    """Create documentation for Client and Run in the given location

    Parameters
    ----------
    output_dir : str
        directory to place reference docs
    mkdocs_cfg : str
        location of mkdocs configuration file
    """
    ref_dir = pathlib.Path(output_dir).joinpath("reference")
    ref_dir.mkdir(exist_ok=True)

    mkdocs_cfg_file = pathlib.Path(mkdocs_cfg)

    with mkdocs_cfg_file.open() as in_f:
        mkdocs_data = yaml.load(in_f, Loader=yaml.UnsafeLoader)

    for i, entry in enumerate(mkdocs_data["nav"]):
        if "Reference" in entry:
            mkdocs_data["nav"].pop(i)
            break

    mkdocs_nav: list[dict[str, str]] = []
    mkdocs_ll_nav: list[dict[str, str]] = []

    print(f"Writing reference to '{ref_dir}'")

    for label, module in zip(
        (
            "Client",
            "Run",
            "api.objects.Run",
            "api.objects.Artifact",
            "api.objects.FileArtifact",
            "api.objects.ObjectArtifact",
            "api.objects.Metrics",
            "api.objects.Events",
            "api.objects.Stats",
            "api.objects.Storage",
            "api.objects.S3Storage",
            "api.objects.FileStorage",
        ),
        (
            Client,
            Run,
            RunObject,
            Artifact,
            FileArtifact,
            ObjectArtifact,
            Metrics,
            Events,
            Stats,
            Storage,
            S3Storage,
            FileStorage,
        ),
    ):
        # Include initialisation method
        methods: list[str] = ["__init__"]
        methods += [i for i in dir(module) if not i.startswith("_")]
        properties = [i for i in methods if isinstance(getattr(module, i), property)]
        parent_class_str: str = ""

        if len(module.__mro__) > 1:
            parent_class_str = " > ".join(
                f"`{i.__name__}`"
                for i in reversed(module.__mro__[1:])
                if i is not object
            )

        file_name: str = f"{label.replace('.', '_').lower()}.md"
        output_file = ref_dir.joinpath(file_name)

        if "api.objects" in label:
            _entry = {label: f"reference/{file_name}"}
            mkdocs_ll_nav.append(_entry)
        else:
            _entry = {f"The {label} class": f"reference/{file_name}"}
            mkdocs_nav.append(_entry)

        with output_file.open("w") as out_f:
            out_f.write(f"# The `{label}` class\n")
            if parent_class_str:
                out_f.write(f"*Inherits from {parent_class_str}*\n\n")
            out_f.write(f"{module.__doc__ or ' '}\n")
            out_f.write("## Methods\n")
            for method in methods:
                if method in properties:
                    continue
                method_docstr: str = getattr(module, method).__doc__
                method_signature: inspect.Signature = inspect.signature(
                    getattr(module, method)
                )
                doc = create_markdown(
                    name=method,
                    docstring=method_docstr,
                    signature=method_signature,
                    is_property=False,
                )
                out_f.write(doc)
                out_f.write("----\n")
            if properties:
                out_f.write("## Properties\n")
            for prop in properties:
                getter_docstring: str = getattr(module, prop).fget.__doc__
                getter_signature: inspect.signature = inspect.signature(
                    getattr(module, prop).fget
                )
                doc = create_markdown(
                    name=prop,
                    docstring=getter_docstring,
                    signature=getter_signature,
                    is_property=True,
                )
                out_f.write(doc)
                out_f.write("----\n")
    mkdocs_nav.append({"Low Level API": mkdocs_ll_nav})
    mkdocs_data["nav"].append({"Reference": mkdocs_nav})
    with mkdocs_cfg_file.open("w") as out_f:
        yaml.dump(mkdocs_data, out_f, Dumper=yaml.Dumper)


if __name__ in "__main__":
    create_client_docs()
