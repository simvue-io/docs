# Events

A method is available in the `Client` class for retrieving events. In the examples below
an instance of the `Client` class needs to be created first, i.e
```python
from simvue import Client
client = Client()
```

## All events
To obtain all events associated with a run:
```python
events = client.get_events(run)
```
where `run` is the run name. The output is in the form of a list of dictionaries of the form:
```json
{"timestamp": "YYYY-MM-DD HH:MM:SS.ZZZZZZ", "message": "..."}
```

## Pagination
To retrieve `n` events starting from index `m`, use:
```python
events = client.get_events(run_identifier, count_limit=n, start_index=m)
```

## Filtering
To retrieve all events from a run containing the word `Exception`, use:
```python
events = client.get_events(run_identifier, message_contains='Exception')
```

??? further-docs "Further Documentation"

    - [^^The get_events() method^^](/reference/client#get_events)
    - [^^Example of using the get_events() method in the Tutorial^^](/tutorial_basic/analysis/#retrieving-events)