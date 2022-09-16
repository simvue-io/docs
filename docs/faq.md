# Frequently asked questions

## What happens if my code crashes?
The Simvue client sends a heartbeat to the server every minute. If there are no heartbeats for at least 3 minutes a run goes into the **lost** state. If a Python code is killed by control-c or SIGINT the state will change to **terminated**.
