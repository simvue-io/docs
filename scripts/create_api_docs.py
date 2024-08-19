import pathlib
import jinja2
import re
import inspect
import click

# Import objects we want to document
from simvue import Client, Run


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

    if annotation.__name__ in ("str", "int", "bool", "float"):
        return annotation.__name__

    return f"{annotation}".replace("typing.", "").replace("NoneType", "None")


def parse_numpydoc(
    input_text: str, signature: inspect.Signature | None
) -> dict[str, str | list[str] | dict | None]:
    """Parse the Numpydoc docstring

    Parameters
    ----------
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
    raises: list[str] = []
    params: dict[str, dict[str, str | None]] = {}

    for i, line in enumerate(lines := input_text.splitlines()):
        if "Parameters" in line:
            log_section = "parameters"
            continue
        if "Returns" in line:
            log_section = "returns"
            continue
        if "Raises" in line:
            log_section = "raises"
            continue
        line = re.sub(r"-{3,}", "", line)
        line = line.strip()

        if not line:
            continue

        if log_section == "parameters":
            if re.findall(r".+:\s*.+", line):
                name, type_var = (i.strip() for i in line.split(":"))
                default_str = None
                annotation = None

                if signature:
                    if name not in signature.parameters:
                        if not name.startswith("*"):
                            raise ValueError(f"Unknown parameter '{name}' in docstring")
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
                params[name]["description"] += line
        elif log_section == "returns":
            returns.append(line)
        elif log_section == "raises":
            raises.append(line)
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
    }


def create_markdown(
    name: str, docstring: str, signature: inspect.Signature | None, is_property: bool
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

    Returns
    -------
    str
        documentation in markdown
    """
    template_file = pathlib.Path(__file__).parent.joinpath("code_entry_markdown.jinja")
    template = jinja2.Template(template_file.open().read())
    metadata = parse_numpydoc(docstring, signature)

    return template.render(
        metadata=metadata, function_name=name.replace("_","\\_"), is_property=is_property
    )


@click.command
@click.argument("output_dir", type=click.Path(exists=True))
def create_client_docs(output_dir: str) -> None:
    """Create documentation for Client and Run in the given location

    Parameters
    ----------
    output_dir : str
        directory to place reference docs
    """
    ref_dir = pathlib.Path(output_dir).joinpath("reference")
    ref_dir.mkdir(exist_ok=True)

    print(f"Writing reference to '{ref_dir}'")

    for label, module in zip(("client", "run"), (Client, Run)):
        # Include initialisation method
        methods: list[str] = ["__init__"]
        methods += [i for i in dir(module) if not i.startswith("_")]
        properties = [i for i in methods if isinstance(getattr(module, i), property)]
        output_file = ref_dir.joinpath(f"{label}.md")
        with output_file.open("w") as out_f:
            out_f.write(f"# The {label.title()} class\n")
            if properties:
                out_f.write("## Properties\n")
            for prop in properties:
                prop_docstr: str = getattr(module, prop).__doc__
                doc = create_markdown(
                    name=prop, docstring=prop_docstr, signature=None, is_property=True
                )
                out_f.write(doc)
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

if __name__ in "__main__":
    create_client_docs()