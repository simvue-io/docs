# Introduction

## Basic example

Here we go through a very simple example from scratch which illustrates how to use
the Simvue Python client, in particular demonstrating:

* tags,
* metadata,
* specifying a folder,
* saving the Python code itself,
* logging metrics,
* ending the run.

### Create a virtual environment

Run the following commands to create and activate a new virtual environment:
```
python3 -m venv venv
source ./venv/bin/activate
```

### Install

Install the Python client:
```
pip install simvue
```

### Setup

The next step is to specify the URL of the Simvue server and provide an access token used to authenticate to the server.

Login to the web UI, go to the **Runs** page and click **Create new run**. Create a file called `simvue.ini` containing
the contents as provided.
The file should look something like:
```
[server]
url = https://app.simvue.io
token = eyJ0eXAi...
```

### Running a test

Create a file containing the following code:
```  py
import os
import random
import time
from simvue import Run

if __name__ == "__main__":
    run = Run()

    # Initialisation
    run.init(name='hello-world-%d' % time.time(),
             tags=['test'],
             metadata={'key1': 1, 'key2': 'hello'},
             folder='/tests')

    # Save this script
    run.save(os.path.basename(__file__), 'code')

    # Generate 10 random numbers, one per second
    for count in range(0, 10):
        run.log_metrics({'random_number': 10*random.random()})
        time.sleep(1)

    # Close the run
    run.close()
```

Run the script, for example:
```
python test.py
```

This script should run for 10 seconds and will create a new run visible in the Simvue web dashboard.


## Next steps

Continue on to [Tracking & monitoring](/python-client/getting-started/) in order to learn about using Simvue
in more detail.
