# Integrations
To allow for easy tracking and monitoring of different simulation software, the Simvue Integrations repository has been created which can automatically track several key metrics from any generic simulation performed in selected simulation codes. These are divided into two groups: 

- **Plugins**, for integrating with Python based simulation codes
- **Connectors**, for integrating with Non-Python based simulation codes

## Plugins
Plugins are created for monitoring Python based simulation codes (or Non-Python simulation codes which have a Python interface). They may take a range of different forms, depending on whether the Python module being tracked has explicit support for third party modules. Currently, plugins have been created for:

- [Tensorflow](/integrations/tensorflow)

## Connectors
Connectors are created for monitoring Non-Python based simulation codes. These work by reading output files created by the simulations in real time, parsing them to exract key information and uploading this as metrics and events to the Simvue run. These all have a common form, and should be built on top of the generic `WrappedRun` class. Currently, connectors have been created for:

- [MOOSE](/integrations/moose)
- [Fire Dynamics Simulator](/integrations/fds)
- [OpenFOAM](/integrations/openfoam)

## Requesting new integrations
If you have a commonly used simulation which you think would benefit from Simvue integration, you can [^^raise an issue on the connectors-generic Github repo^^](https://github.com/simvue-io/connectors-generic/issues), and add the 'integration request' label.