# Low Level Python API
Since the move to Simvue server v3 the structure of the Python API has been updated to include an additional layer known as the _low level API_. The purpose of this layer is to provide a direct mapping to the structure present within the RestAPI, i.e. define classes mirroring the endpoints for the various server objects.

The introduction of this layer has the advantage that it provides an interface for the development of integrations and extensions without needing to modify underlying code, with minimal changes to the user facing API.

## The `SimvueObject` base class
For consistency a base class is used from which the various object types are then defined. The `SimvueObject` base class contains methods for connecting to a Simvue server instance, then creating, modifying or retrieving objects through RestAPI requests.

Taking Simvue runs as an example:

```python
class Run(SimvueObject):
  ...
```
!!! warning "`Run` vs `Run`"
    It should be noted here that `Run` in this context is _not_ `simvue.Run` as used by the user, but `simvue.api.objects.Run` matching the above definition.

The class is used one one of two ways, either as a means of retrieving an entry on the server using the relevant identifier:

```
simvue_run = simvue.api.objects.Run(identifier="...")
```

which creates an instance whereby the contents from the server are cached locally, and the object set to `read_only` mode,
or defining an object on the server by creating a new instance:

```python
new_run = simvue.api.objects.Run.new(folder="/")
new_run.name = "my_run"
new_run.metadata = {"x": 2}
new_run.commit()
```

object parameters are always defined using explicit keyword arguments. In general, `new` is defined to only take mandatory arguments,
the minimum required by the server for the definition to pass validation. Additional arguments to the RestAPI `POST` request are then
given via writable properties. Finally confirmation and dispatch to the server is performed using the `commit()` method.


In cases where it is possible to retrieve a set of objects a member function `get` provides a generator returning pairs of identifier and assembled Python objects:

```python
for identifer, run in Run.get():
  print(f"Run {identifier}:")
  print(json.dumps(run.to_dict(), indent=2))
```
