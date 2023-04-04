# Events

A method is available in the `Client` class for retrieving events. In the examples below
an instance of the `Client` class needs to be created first, i.e
```
from simvue import Client
client = Client()
```

## All events
To obtain all events associated with a run:
```
events = client.get_events(run)
```
where `run` is the run name. The output is in the form of a list of dictionaries of the form:
```
{"timestamp": "YYYY-MM-DD HH:MM:SS.ZZZZZZ", "message": "..."}
```

## Pagination
To retrive `n` events starting from position `m`, use:
```
events = client.get_events(run, start=n, num=m)
```

## Filtering
To retrieve all events from a run containing the word `Exception`, use:
```
events = client.get_events(run, filter='Exception')
```
