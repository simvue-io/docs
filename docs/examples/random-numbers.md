# Basic Example of Simvue

This example demonstrates using Simvue to track a simple Python code, adding in different features on a step by step basis. The ordering of topics introduced in this example matches that of the documentation in the 'Tracking and Monitoring' and 'Analysis' sections. For first time users, it is recommended that you follow along with this example step by step, to get a good understanding of what each command does.

## Setup

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

### Configuring Simvue

The next step is to specify the URL of the Simvue server and provide an access token used to authenticate to the server.

Login to the web UI, go to the **Runs** page and click **Create new run**. Create a file called `simvue.ini` containing
the contents as provided.
The file should look something like:
```
[server]
url = https://app.simvue.io
token = eyJ0eXAi...
```

## Creating a Program to Monitor

Next we need to create our initial program which we may want to monitor with Simvue. In our case, we will make a simple script which generates a random integer between 0 and 10 each second for 10 seconds. Create a file called `test.py` which contains the following code:

```  py
import random
import time

if __name__ == "__main__":

    # Generate 10 random numbers, one per second
    for count in range(0, 10):
        random_number = random.randint(0, 10)
        print(random_number)
        time.sleep(1)
```

If you run this file using the command `python3 test.py` in the console, you should see it print an integer every second for 10 seconds.

## Creating a Simvue Run

### Initialising the Run

To create a Run which we can see in the Simvue UI, we first need to import the `Run()` object from the `simvue` module. We then call the `run.init()` method to set up the run:

```  py
import random
import time
from simvue import Run

if __name__ == "__main__":

    with Run() as run:
        # Initialise the run
        run.init(name='random-numbers-%d' % time.time(),
                description='Monitoring of the generation of random integers between 0 and 10.'
                tags=['random-numbers', 'WIP'],
                folder='/rand_nums')


        # Generate 10 random numbers, one per second
        for count in range(0, 10):
            random_number = random.randint(0, 10)
            print(random_number)
            time.sleep(1)
```

In our case above, we have specified the name of this run and the folder to store it in. We have also given it a couple of tags, including `random-numbers` to reflect the script which the run is monitoring, and `WIP` to show that the run is still a work in progress. If you run this code and then log into the Simvue UI, you should be able to see that in the `Runs` tab a new run has appeared. Clicking on this run will show you some information about the run, such as the time at which it was ran, the time it took to execute, information about the system which it was ran on and the description of the run which we supplied above.

### Configuring the Run

Next, we can use the `config` method to change some configuration options about the run. This must be set before the run is initialised. For example, we could set `suppress_errors` to `True` so that if we setup part of our run incorrectly, the script will fail instead of continuing to run:

```  py
import random
import time
from simvue import Run

if __name__ == "__main__":

    with Run() as run:
        # Configure the run
        run.config(suppress_errors=True)

        # Initialise the run
        run.init(name='random-numbers-%d' % time.time(),
                description='Monitoring of the generation of random integers between 0 and 10.',
                tags=['random-numbers', 'WIP'],
                folder='/rand_nums')

        # Generate 10 random numbers, one per second
        for count in range(0, 10):
            random_number = random.randint(0, 10)
            print(random_number)
            time.sleep(1)
```

### Add Information for Folders
Since in our `init` method we created a new folder called `/rand_nums` to store all of our runs in, we can see this in the `Folders` tab of the Simvue UI. However folders can also have metadata, tags and descriptions which can be seen in the UI, that we can set in our run using the `run.set_folder_details` method:

```  py
import random
import time
from simvue import Run

if __name__ == "__main__":

    with Run() as run:
        # Configure the run
        run.config(suppress_errors=True)

        # Initialise the run
        run.init(name='random-numbers-%d' % time.time(),
                description='Monitoring of the generation of random integers between 0 and 10.',
                tags=['random-numbers', 'WIP'],
                folder='/rand_nums')

        # Set details about the folder which we have created to store our runs:
        run.set_folder_details('/rand_nums',
                       metadata={'environment': 'testing'},
                        tags=['random-numbers',],
                       description='Stores all runs which monitor the function to create random integers between 0 and 10.')

        # Generate 10 random numbers, one per second
        for count in range(0, 10):
            random_number = random.randint(0, 10)
            print(random_number)
            time.sleep(1)
```
Running the script again and checking the `Folders` tab of the Simvue UI should show this information has correctly updated. 

## Creating Metrics

### Random Numbers
Next, we need to create our metrics. These are measures of the performance or results of the code which we can monitor in the UI in real time. To do this, we use the `log_metrics` method, which we call at the point in the code at which we want to evaluate the metric. For example, let us create a metric which simply records the random number which is generated on each iteration of the loop. To do this, we simply pass in a dictionary which contains the metric name as the key, and the argument to store as the value:

```  py
import random
import time
from simvue import Run

if __name__ == "__main__":

    with Run() as run:
        # Configure the run
        run.config(suppress_errors=True)

        # Initialise the run
        run.init(name='random-numbers-%d' % time.time(),
                description='Monitoring of the generation of random integers between 0 and 10.',
                tags=['random-numbers', 'WIP'],
                folder='/rand_nums')

        # Set details about the folder which we have created to store our runs:
        run.set_folder_details('/rand_nums',
                       metadata={'environment': 'testing'},
                        tags=['random-numbers',],
                       description='Stores all runs which monitor the function to create random integers between 0 and 10.')

        # Generate 10 random numbers, one per second
        for count in range(0, 10):
            random_number = random.randint(0, 10)
            print(random_number)

            # Log the metrics, so that they can be seen in the Simvue UI in real time
            run.log_metrics({'random_number': random_number})
            time.sleep(1)
```
When we run this code again, we should now see that under the `Metrics` tab of the run in the UI, a line graph is updated in real time as the code runs, showing the random number generated with each iteration of the code. You should see that the numbers plotted on this line graph match those being printed to the console. The `step` parameter along the x axis corresponds to the iteration at which that number was generated.

### Averages
Next, let us add some more metrics which calcuate the averages of the random numbers generated so far after each iteration. To do this, we will create a `numpy` array and append the random number generated to it after each iteration. We will then use the `nnumpy.average()` function to calculate the mean, the `numpy.median()` function to calculate the median, and `numpy.bincount().argmax()` to calculate the mode.

Firstly, ensure that `numpy` is installed with your python installation. If it is not, add it using:
```
pip install numpy
```
Then change your script to calculate these averages like so:
``` py
        # Initialise an empty array which expects integers
        all_numbers = numpy.array([], dtype=numpy.int64)        

        # Generate 10 random numbers, one per second
        for count in range(0, 10):
            random_number = random.randint(0, 10)
            all_numbers = numpy.append(all_numbers, random_number)

            # Calculate averages
            mean = float(numpy.average(all_numbers))
            median = int(numpy.median(all_numbers))
            mode = int(numpy.bincount(all_numbers).argmax())
```

Finally, we want to log each of these metrics. Again we call the `log_metrics` method, passing in a dictionary of the three names of the metrics and their values. However so that they all plot on the same graph in the UI for easier comparison, we will give them names in dot notation (`averages.mean`, `averages.median`, `averages.mode`):
```  py
import random
import time
import numpy
from simvue import Run

if __name__ == "__main__":

    with Run() as run:
        # Configure the run
        run.config(suppress_errors=True)

        # Initialise the run
        run.init(name='random-numbers-%d' % time.time(),
                description='Monitoring of the generation of random integers between 0 and 10.',
                tags=['random-numbers', 'WIP'],
                folder='/rand_nums')

        # Set details about the folder which we have created to store our runs:
        run.set_folder_details('/rand_nums',
                       metadata={'environment': 'testing'},
                        tags=['random-numbers',],
                       description='Stores all runs which monitor the function to create random integers between 0 and 10.')

        # Initialise an empty array which expects integers
        all_numbers = numpy.array([], dtype=numpy.int64)        

        # Generate 10 random numbers, one per second
        for count in range(0, 10):
            random_number = random.randint(0, 10)
            all_numbers = numpy.append(all_numbers, random_number)
            mean = float(numpy.average(all_numbers))
            median = int(numpy.median(all_numbers))
            mode = int(numpy.bincount(all_numbers).argmax())

            # Log the metrics, so that they can be seen in the Simvue UI in real time
            run.log_metrics({'random_number': random_number})

            run.log_metrics({
                'averages.mean': mean,
                'averages.median': median,
                'averages.mode': mode
            })
            time.sleep(1)
```
Upon running the script again and checking the UI, you should now see a new graph in the `Metrics` tab which shows three lines, one for each metric. However you may have spotted something weird is happening - whereas before the `step` parameter on the x axis corresponded to the iteration at which the metric was sampled, the x axis now goes up to 20 instead of 10! This is because we have called `log_metrics` twice in the above code, and so each time it is called it adds one to the value of `step`. We could fix this by evaluating all of the metrics in the same call, ie:
```
run.log_metrics({
    'random_number': random_number
    'averages.mean': mean,
    'averages.median': median,
    'averages.mode': mode
})
```
In a situation where this was not possible, you could instead manually define what the `step` parameter should be. In our case, we could set it equal to the value of `count` for this iteration of the loop:
```
run.log_metrics({'random_number': random_number}, step=count)

run.log_metrics({
    'averages.mean': mean,
    'averages.median': median,
    'averages.mode': mode
}, step=count)
```
Rerunning the code with either of these solutions should show the the two graphs of the metrics in the UI go back to using the number of the iteration for the `step` parameter on the x axis.

### Resource Usage Metrics
Resource usage metrics are collected automatically from the Python client, and displayed under the `Resources` tab of the run in the UI. So far we have not been able to see them, since they are collected every thirty seconds be default, and our program has only ran for 10 seconds at a time. To fix this, we will update our run config to sample the resource metrics every 10 seconds using the `resources_metrics_interval` argument, and we will increase our number of iterations in the loop to 30:

```  py
import random
import time
import numpy
from simvue import Run

if __name__ == "__main__":

    with Run() as run:
        # Configure the run
        run.config(suppress_errors=True,
            resources_metrics_interval=10)

        # Initialise the run
        run.init(name='random-numbers-%d' % time.time(),
                description='Monitoring of the generation of random integers between 0 and 10.',
                tags=['random-numbers', 'WIP'],
                folder='/rand_nums')

        # Set details about the folder which we have created to store our runs:
        run.set_folder_details('/rand_nums',
                       metadata={'environment': 'testing'},
                        tags=['random-numbers',],
                       description='Stores all runs which monitor the function to create random integers between 0 and 10.')

        # Initialise an empty array which expects integers
        all_numbers = numpy.array([], dtype=numpy.int64)        

        # Generate 10 random numbers, one per second
        for count in range(0, 30):
            random_number = random.randint(0, 10)
            all_numbers = numpy.append(all_numbers, random_number)
            mean = float(numpy.average(all_numbers))
            median = int(numpy.median(all_numbers))
            mode = int(numpy.bincount(all_numbers).argmax())

            # Log the metrics, so that they can be seen in the Simvue UI in real time
            run.log_metrics({'random_number': random_number}, step=count)

            run.log_metrics({
                'averages.mean': mean,
                'averages.median': median,
                'averages.mode': mode
            }, step=count)
            time.sleep(1)
```
Rerunning the script should now allow you to see your computer's CPU and RAM usage over time as it runs the script in the `Resources` tab in the UI.

## Events
### Logging
During a run, any arbitrary text can be logged using the `log_event` method, and will show up in the `Events` tab of the run in the UI. For example, let's say that we simply want to add a log of the time at which the code began running, and when all of the iterations completed. To do this, we just need to add the following line before the for loop:
```
run.log_event('Random number generation started!')
```
And the following line after the for loop:
```
run.log_event('Random number generation completed!')
```
If we then rerun the code and look in the `Events` tab of the run, we should see these two timestamped log entries, which are roughly 30 seconds apart.
### Catching Exceptions
We can also use the `log_event` method to catch Exceptions which are thrown during code execution. For example, let's say that we want to calculate a new metric, which gives us the value of the mean divided by the difference between the median and the mode. To calculate and log this metric, we will add the following into the for loop:
```
new_stat = mean / abs(median - mode)
run.log_metrics({
    'new_stat': new_stat
}, step=count)
```
However, the issue with this code is that in the case where the median is equal to the mode, we will get a division by zero error. To prevent this, we can wrap these lines inside a try/except block. However we may want to know when we encounter this error, so we will also add a message to the Events logger. The full code may look something like this:
```  py
import random
import time
import numpy
from simvue import Run

if __name__ == "__main__":

    with Run() as run:
        # Configure the run
        run.config(suppress_errors=True,
            resources_metrics_interval=10)

        # Initialise the run
        run.init(name='random-numbers-%d' % time.time(),
                description='Monitoring of the generation of random integers between 0 and 10.',
                tags=['random-numbers', 'WIP'],
                folder='/rand_nums')

        # Set details about the folder which we have created to store our runs:
        run.set_folder_details('/rand_nums',
                       metadata={'environment': 'testing'},
                        tags=['random-numbers',],
                       description='Stores all runs which monitor the function to create random integers between 0 and 10.')

        # Initialise an empty array which expects integers
        all_numbers = numpy.array([], dtype=numpy.int64)        

        run.log_event("Random Number Generation Started!")
        # Generate 10 random numbers, one per second
        for count in range(0, 30):
            random_number = random.randint(0, 10)
            all_numbers = numpy.append(all_numbers, random_number)
            mean = float(numpy.average(all_numbers))
            median = int(numpy.median(all_numbers))
            mode = int(numpy.bincount(all_numbers).argmax())

            # Log the metrics, so that they can be seen in the Simvue UI in real time
            run.log_metrics({'random_number': random_number}, step=count)

            run.log_metrics({
                'averages.mean': mean,
                'averages.median': median,
                'averages.mode': mode
            }, step=count)

            # Catch any Exception throws from this calculation:
            try:
                # Calculate and log our new metric
                new_stat = mean / abs(median - mode)
                run.log_metric({'new_stat': new_stat}, step=count)
            # Log event if divide by zero encountered during calculation
            except ZeroDivisionError:
                run.log_event(f"Division by Zero Error encountered in calculation of new_stat on iteration {count}") 

            time.sleep(1)

        run.log_event("Random Number Generation Completed!")
```
Running this script should now show at least one entry in the Events log, corresponding to the first iteration where the median must be equal to the mode. However you should see that the logging of our new metric will still continue as we expect for subsequent iterations, just missing data points where a divide by zero was encountered.

## Artifacts
### Saving Files
Files can be saved as artifacts and viewed in the UI by using the `save` method. Any files can be saved - for example, we could save our whole script. Firstly import the `os` module, and then add the following line at any point after the run is initialised:
```
run.save(os.path.basename(__file__), 'code')
```
We could also save the final values of each of the averages in a dictionary and store them in a JSON file, and then upload that JSON file as an artifact. Firstly import the `json` and `pathlib` modules (installing it using pip if it is not in your python package already). Then after the for loop is complete, add the following code:
```
averages_out = {
    'mean': mean,
    'median': median,
    'mode': mode
}
with open(os.path.join(pathlib.Path(__file__).parent, "averages_out.json"), "w") as out_file:
    json.dump(averages_out, out_file)

run.save(os.path.join(pathlib.Path(__file__).parent, "averages_out.json"), 'output')
```
Running the code with these additions should mean that in the `Artifacts` tab of the run in the UI, the full script is saved under the `Code` tab, and the JSON file containing the final values of the averages is saved under the `Outputs` tab.

### Saving Python Objects
It is not only files which can be saved - Python objects, such as Numpy arrays, Pandas dataframes, or Matplotlib figures can also be saved directly as artifacts. For example, say that we want to also save our Numpy array of all of the random numbers which we generated. We can easily do this by adding this line of code after the for loop:
```
run.save(all_numbers, 'output', name='all_random_numbers')
```
Similarly to the files saved above, this array should now be visible in the `Outputs` section of the `Artifacts` tab of the run. The full code to save these artifacts can be seen here:
```  py
import random
import time
import numpy
import os
import pathlib
import json
from simvue import Run

if __name__ == "__main__":

    with Run() as run:
        # Configure the run
        run.config(suppress_errors=True,
            resources_metrics_interval=10)

        # Initialise the run
        run.init(name='random-numbers-%d' % time.time(),
                description='Monitoring of the generation of random integers between 0 and 10.',
                tags=['random-numbers', 'WIP'],
                folder='/rand_nums')

        # Save the code as an artifact
        run.save(os.path.basename(__file__), 'code')

        # Set details about the folder which we have created to store our runs:
        run.set_folder_details('/rand_nums',
                       metadata={'environment': 'testing'},
                        tags=['random-numbers',],
                       description='Stores all runs which monitor the function to create random integers between 0 and 10.')

        # Initialise an empty array which expects integers
        all_numbers = numpy.array([], dtype=numpy.int64)        

        run.log_event("Random Number Generation Started!")
        # Generate 10 random numbers, one per second
        for count in range(0, 30):
            random_number = random.randint(0, 10)
            all_numbers = numpy.append(all_numbers, random_number)
            mean = float(numpy.average(all_numbers))
            median = int(numpy.median(all_numbers))
            mode = int(numpy.bincount(all_numbers).argmax())

            # Log the metrics, so that they can be seen in the Simvue UI in real time
            run.log_metrics({'random_number': random_number}, step=count)

            run.log_metrics({
                'averages.mean': mean,
                'averages.median': median,
                'averages.mode': mode
            }, step=count)

            # Catch any Exception throws from this calculation:
            try:
                # Calculate and log our new metric
                new_stat = mean / abs(median - mode)
                run.log_metric({'new_stat': new_stat}, step=count)
            # Log event if divide by zero encountered during calculation
            except ZeroDivisionError:
                run.log_event(f"Division by Zero Error encountered in calculation of new_stat on iteration {count}") 

            time.sleep(1)

        run.log_event("Random Number Generation Completed!")

        # Save the final values of the averages to a JSON file and store as an artifact
        averages_out = {
            'mean': mean,
            'median': median,
            'mode': mode
        }
        with open(os.path.join(pathlib.Path(__file__).parent, "averages_out.json"), "w") as out_file:
            json.dump(averages_out, out_file)

        run.save(os.path.join(pathlib.Path(__file__).parent, "averages_out.json"), 'output')

        # Store the array of random numbers as an artifact
        run.save(all_numbers, 'output', name='all_random_numbers')
```