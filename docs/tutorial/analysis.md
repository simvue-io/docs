# Analysis
This section of the tutorial introduces how Simvue can be used to retrieve information about a run such as metadata, metrics or artifacts, and use these to perform more in depth data analysis or create plots of important data. The topics covered in this section (and more) are described in the [Analysis](/analysis/retrieving-runs/) section of the documentation, so it may be useful to have that section of the docs open alongside this part of the tutorial.

## Simvue Client
Results and artifacts from runs can be collected using the Simvue Client for further analysis. We will demonstrate this in a new file, called `analysis.py`. Create this new file in the same location as your `test.py` script above, and create an instance of the `Client` class:
``` py
from simvue import Client

client = Client()
```
For the next part of the tutorial to make sense, make sure that you have ran the full code example given in the `Tracking & Monitoring` section of the tutorial at least once.

## Retrieving Runs
To retrieve a single run which we know the name of, we can use the method `get_run()` of the Client class. If you log into the UI and choose one of your recent runs, and simply run `client.get_run(<name of run>)`, you will see that you get a dictionary of information returned to you such as the name, status, folder, and the timestamps of when it was created, started and completed. You can also enable the optional parameters `tags=True` or `metadata=True` to retrieve the tags and metadata asociated with the run.

However, what if we don't know the exact name of our run, or we want to retrieve multiple runs at once? We can instead use the `get_runs()` method, which allows us to specify filters to use to find our set of runs. In our case, we will want to look for any runs stored in the `/rand_nums` folder, which have the tags `completed` and `v1`:

``` py
from simvue import Client

client = Client()
my_runs = client.get_runs(['/rand_nums', 'completed', 'v1'], metadata=True, tags=True)
print(my_runs)
```
If you then run the analysis script using `python3 analysis.py` on the command line, you should hopefully see a list of dictionaries printed, similar to the following:
```
[
    {
        'name': 'random-numbers-1696963675', 
        'status': 'completed', 
        'folder': '/rand_nums', 
        'created': '2023-10-10 18:47:55.694680', 
        'description': 'Monitoring of the generation of random integers between 0 and 10.', 
        'ended': '2023-10-10 18:53:02.034911', 
        'started': '2023-10-10 18:47:55.694680', 
        'tags': ['random-numbers', 'v1', 'completed'], 
        'metadata': {'mean': 4.993333333333333, 'number_of_iterations': 300, 'result_converged': 'True'}
    },
    ...,
]
```
This should show you a list of all of the runs which you have ran using the final code in the section above. You can check that it is correct by going to the 'Runs' tab on the UI, adding filters to the top by pressing the `Folder` and `Tags` buttons and selecting the correct values, and checking that the runs listed in the UI match those in the list of dictionaries printed to the command line.

We will store the name of the first run which fits our criteria in a variable, for use in the rest of the code:
``` py
from simvue import Client

client = Client()
# Get data about all of the runs which fit our filters
my_runs = client.get_runs(['/rand_nums', 'completed', 'v1'], metadata=True, tags=True)

# Save the name of the first run in the list
run_name = my_runs[0]['name']

```
## Retrieving Metrics

You can retrieve the names of all of the metrics for a given run using the `get_metrics_names()` method, and some simple statistics about each metric using the `get_metrics_summaries()` method. To test these functions, we will perform the following:
``` py
from simvue import Client

client = Client()
# Get data about all of the runs which fit our filters
my_runs = client.get_runs(['/rand_nums', 'completed', 'v1'], metadata=True, tags=True)

# Save the name of the first run in the list
run_name = my_runs[0]['name']

# Get metric names and summaries for the run selected above
metrics_names = client.get_metrics_names(run_name)
for metric_name in metrics_names:
    print(f"Summary of {metric_name}: \n {client.get_metrics_summaries(metric_name)}")
```

You can also directly plot different metrics. Firstly import `matplotlib.pyplot` to be able to display the plot (installing the module using `pip install matplotlib` if it is not installed already). You can then use the `.plot_metrics()` method to plot any matrics as a line graph. For example, if we wanted to plot `averages.mean` metric:
``` py
# Plot a line graph of the averages.mean metric
mean_plot = client.plot_metrics([run_name,], ['averages.mean',], 'step')
plt.show()
```
We should see that this plot matches the one seen in the UI for this metric. Note that `plot_metrics()` can be used on multiple runs and/or metrics at a time, so expects lists as inputs to the `runs` and `metrics` parameters. Simvue can also output the data from the metric as a Pandas dataframe, which allows us to do more advanced analysis. For example, lets say we want to get our random numbers back from the metric as a dataframe:
``` py
rand_nums_df = client.get_metrics(run_name, 'random_number', 'step', format='dataframe')
```
We can then group our data based on the value in the `random_number` column for each step using `.groupby()`, and collect the number of steps at which each possible random number was present using `.nunique()`. Finally we can plot this data as a bar graph to see how many of each random number we got over the course of the run using `.plot()`:
``` py
rand_nums_bar_plot = rand_nums_df.groupby('random_number').nunique().plot(kind='bar', rot=0)
plt.show()
```
We should then see a bar graph of the number of occurances of each random number - it should be a roughly even distribution between each of the random numbers. The full code so far can be seen below:
``` py
import matplotlib.pyplot as plt
from simvue import Client

client = Client()
# Get data about all of the runs which fit our filters
my_runs = client.get_runs(['/rand_nums', 'completed', 'v1'], metadata=True, tags=True)

# Save the name of the first run in the list
run_name = my_runs[0]['name']

# Get metric names and summaries for the run selected above
metrics_names = client.get_metrics_names(run_name)
for metric_name in metrics_names:
    print(f"Summary of {metric_name}: \n {client.get_metrics_summaries(metric_name)}")

# Plot a line graph of the averages.mean metric
mean_plot = client.plot_metrics(run_name, 'averages.mean', 'step')

# Plot a bar graph of the number of occrances of each random number
rand_nums_df = client.get_metrics(run_name, 'random_number', 'step', format='dataframe')
rand_nums_bar_plot = rand_nums_df.groupby('random_number').nunique().plot(kind='bar', rot=0)
rand_nums_bar_plot.set_ylabel("Number of instances")

# Show the plots in window
plt.show()
```

## Retrieving Events
We can also retrieve Events from the log using the method `get_events()`, which will return a list of dictionaries which each give the timestamp and message of an event. This allows us to either retrieve the whole events log, a select number of events from a given line using the `start` and `num` arguments, or to filter events which contain a specific word or phrase using the `filter` argument. For example, say we want to find the number of division by zero errors we encountered during a run when calculating our `mean / (median - mode)` value. To do this, we will retrieve all events which contain the string 'Division by Zero Error':

``` py
num_div_by_zeros = len(client.get_events(run_name, filter='Division by Zero Error'))
print("Number of Division by Zero Errors encountered during execution:", num_div_by_zeros)
```

## Retrieving Artifacts
Finally named artifacts can be retrieved from the run using the `get_artifact()` method. This will download the artifact, and return its contents. For example, if we wanted to retrieve our artifact of the array of percentage changes of the mean between each iteration, we can do:

``` py
percentage_changes_in_mean = client.get_artifact(run_name, 'percentage_changes_in_mean')
```

We may then want to create a plot of this, showing how the percentage change to the mean progressed across all of the iterations. To do this, we will need to create an array of x data, which is the iteration number. We will create this by retrieving the number of iterations from the metadata and using `numpy.arange()` to create our array. Firstly import `numpy` at the top of your script, and then do:
``` py
# Create an array of iteration values, by retrieving the total number of iterations from the run's metadata
run_info = client.get_run(run_name, metadata=True)
num_iterations = run_info['metadata']['number_of_iterations']
iterations_arr = numpy.arange(num_iterations)

# Plot the percentage change in the mean at each iteration
fig, ax = plt.subplots()
ax.plot(iterations_arr, percentage_changes_in_mean)
ax.set_xlabel('Iteration')
ax.set_ylabel('Percentage Change in Mean')
```
This graph should look like a kind of damped oscillation - as the number of iterations progresses, each individual random number added to the mean makes less and less impact, and so the line should begin to flatten and remain at around zero after a large number of iterations.

You can also retrieve artifacts as files and save them to your local system using `get_artifact_as_file()`. Say we want to retrieve our JSON file which contains the final values of our three averages - to do this, we simply pass in the name of the artifact and the path where we would like it to be saved (we will leave the path blank, as it will save the file to our current working directory by default):

``` py
client.get_artifact_as_file(run_name, 'averages_out.json')
```
You should then see this file be saved in your working directory, and opening it should show the dictionary of the three averages which we expect.

## Full Code

That completes our tutorial of how to use the Analysis functionality in Simvue! The full code is below:

``` py
import matplotlib.pyplot as plt
import numpy
from simvue import Client

client = Client()

# Get data about all of the runs which fit our filters
my_runs = client.get_runs(['/rand_nums', 'completed', 'v1'], metadata=True, tags=True)

# Save the name of the first run in the list
run_name = my_runs[0]['name']

# Get metric names and summaries for the run selected above
metrics_names = client.get_metrics_names(run_name)
for metric_name in metrics_names:
    print(f"Summary of {metric_name}: \n {client.get_metrics_summaries(metric_name)}")

# Plot a line graph of the averages.mean metric
mean_plot = client.plot_metrics([run_name,], ['averages.mean',], 'step')

# Plot a bar graph of the number of occrances of each random number
rand_nums_df = client.get_metrics(run_name, 'random_number', 'step', format='dataframe')
rand_nums_bar_plot = rand_nums_df.groupby('random_number').nunique().plot(kind='bar', rot=0)
rand_nums_bar_plot.set_ylabel("Number of instances")

# Find and print the total number of Division by Zero events in the log:
num_div_by_zeros = len(client.get_events(run_name, filter='Division by Zero Error'))
print("Number of Division by Zero Errors encountered during execution:", num_div_by_zeros)

# Retrieve the artifact containing a Numpy array of the percentage changes in the mean for each iteration
percentage_changes_in_mean = client.get_artifact(run_name, 'percentage_changes_in_mean')

# Create an array of iteration values, by retrieving the total number of iterations from the run's metadata
run_info = client.get_run(run_name, metadata=True)
num_iterations = run_info['metadata']['number_of_iterations']
iterations_arr = numpy.arange(num_iterations)

# Plot the percentage change in the mean at each iteration
fig, ax = plt.subplots()
ax.plot(iterations_arr, percentage_changes_in_mean)
ax.set_xlabel('Iteration')
ax.set_ylabel('Percentage Change in Mean')

# Retrieve and save the JSON file containing the final values of the three averages
client.get_artifact_as_file(run_name, 'averages_out.json')

# Show the plots in window
plt.show()
```