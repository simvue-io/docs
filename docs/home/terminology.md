# Terminology
A table of commonly used terminology can be found below.

| Term  | Description |
| ----- | ----------- |
| Simvue |  A generic real-time monitoring and alerting framework with data lineage for any simulation or data processing application. |
| Run | An instance of a simulation or data processing task which is being monitored by Simvue. |
| Folder | A location to store information about a run on the Simvue storage system. |
| Metric | Time series data which is being evaluated and stored as a run is being executed. |
| Artifact | A file or object that is used as an input or output to the simulation which is stored on the Simvue server |
| Event | A timestamped text record which is produced and stored during run execution, to monitor the progress of the run |
| Alert | A warning which can be sent to the user if a Metric or Event is seen to fall outside required parameters during run execution |
| Metadata | A set of key/value pairs which stores key information about the run being executed |
| Tag | A short label which can be added to runs or folders to help with efficient filtering and searching through stored data |
| Status | The current status of the run, automatically updated by Simvue based on it's communication with the simulation |
| Visibility | The users which a given run can be viewed by, either Public (all users), Tenant (group of users), or Private (only the user who created the run)
| Tenant | A group of users who have some shared permissions, and can view runs created by each other |
| Client | A Python class which allows the user to retrieve data stored on the Simvue server for analysis |