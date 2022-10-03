# Frequently asked questions

## What happens if my code crashes?
The Simvue client sends a heartbeat to the server every minute. A run goes into the **lost** state if there are no heartbeats for over 3 minutes.
