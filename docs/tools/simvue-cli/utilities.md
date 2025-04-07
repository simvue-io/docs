# Utilities and Extras

The following are a set of commands which do not fall into any specific category but provide useful functionality.

## Checking Server Connection
The command:

```sh
simvue ping
```

will attempt to contact the Simvue server returning the time taken to request the current server version (the simplest request)
and the address of the target server.

## User Check
To obtain information on the current user run:

```sh
simvue whoami
```

this will return the current user and the tenant associated with that user.

## Removing Local Data
To completely remove all locally cached Simvue data, including any offline runs run the command:

```sh
simvue purge
```

this will remove the local `.simvue` cache directory.
