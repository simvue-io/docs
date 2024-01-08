# Metadata

The `get_runs` method of the `Client` class has an optional argument `format` which enables the format of the
data retrieved to be specified. There are two options:

* `dict`: a dictionary (the default),
* `dataframe`: a Pandas dataframe.

The dataframe format makes it easy to create plots using the `plot` method in Pandas or using Matplotlib directly.
`pandas.DataFrame.columns` can be used to get a list of the columns, for example:
```
df = client.get_runs(['/fusion/neutronics/adaptive/run4'],
                     metadata=True,
                     format='dataframe')
print(df.columns)
```
Below we go through some example plots.

## Basic scatter plot from metadata
Here is a simple example of a scatter plot using metadata from multiple runs. We plot `final accuracy` vs
`trial.number` for all runs in the specified folder (`/optuna/tests/binary-model` in this case).
```
df = client.get_runs(['/optuna/tests/binary-model'],
                     metadata=True,
                     format='dataframe')
plot = df.plot(kind='scatter',
               x='metadata.trial.number',
               y='metadata.final accuracy')
```
This results in the following plot:
![A scatter plot which uses metadata from all runs in a given folder. Shows a plot of the trial number on the x axis, versus final accuracy of the simulation on the y axis.](images/scatter-metadata.png)

## Scatter plot with coloured markers
We can easily extend a scatter plot by using the value of another metadata attribute to colour the markers. For example:
```
df = client.get_runs(['/fusion/neutronics/adaptive/run4'],
                     metadata=True,
                     format='dataframe')
plot = df.plot(kind='scatter',
               x='metadata.blanket_breeder_li6_enrichment',
               y='metadata.breeder_percent_in_breeder_plus_multiplier_ratio',
               c='metadata.tbr')
```
gives:
![A scatter plot which uses metadata from all runs in a given folder. Shows a plot of the breeding percentage in a breeder blanket (plus multiplier ratio) on the y axis, versus enrichment of a Lithium breeder blanket on the x axis. Each point is a differnt colour, with a colorbar corresponding to the Tritium Breding Ratio (TBR) on the right of the plot.](images/scatter-metadata-colours.png)

## Bar chart
In this example we create a bar chart showing how many runs are associated with each possible
value of a specified metadata attribute, in this case `optimizer`:
```
df = client.get_runs(['/optuna/tests/binary-model'],
                     metadata=True,
                     format='dataframe')

plot = df.groupby('metadata.optimizer')['name'].nunique().plot(kind='bar', rot=0)
```
This gives:
![A bar chart showing the total number of runs in a folder which use a given optimizer (either AdamW, RMSprop or SGD), based on the value of the metadata attribute 'optimizer' for each run.](images/bar-chart-count.png)

## Box plot
Box and whisker plots can be easily created. In this example we show a metadata attribute `final accuracy`
grouped by another attribute, `n_layers`:
```
df = client.get_runs(['/optuna/tests/binary-model'],
                     metadata=True,
                     format='dataframe')

plot = df.boxplot(column=['metadata.final accuracy'], by=['metadata.n_layers'])
```
This results in the following plot:
![A box and whisker plot showing the distribution of final accuracies for all runs in a folder. The runs are grouped by their number of layers (based on the n_layers metadata attribute) along the x axis, with values of either 1, 2, or 3, while the y axis shows the final accuracy of each run. The plots show the minimum and maximum values of each distribution as 'whiskers', with the first quartile, mean and third quartile values shown as 'boxes'. Outliers are marked as points outside of the whiskers.](images/boxplot-numlayers.png)

## Parallel coordinates plot
While parallel coordinates plots can be made directly from a dataframe
([^^see documentation for how to directly plot parallel coordinates from a Pandas dataframe^^](https://pandas.pydata.org/docs/reference/api/pandas.plotting.parallel_coordinates.html)) this has some
limitations, such as common y-axis limits across all variables. An alternative is to use Plotly where it's possible to have much more control - [^^see documentation for creating a parallel coordinates plot using Plotly^^](https://plotly.com/python/parallel-coordinates-plot/). Handling categorical values requires some additional work ([^^view a solution for handling categorical values here^^](https://stackoverflow.com/a/64146570))
as is illustrated in the example:
```
import plotly.graph_objects as go
import pandas as pd
from simvue import Client

client = Client()
df = client.get_runs(['/optuna/tests/binary-model'],
                     metadata=True,
                     format='dataframe')

group_vars = df['metadata.optimizer'].unique()
dfg = pd.DataFrame({'metadata.optimizer': df['metadata.optimizer'].unique()})
dfg['dummy'] = dfg.index
df = pd.merge(df, dfg, on='metadata.optimizer', how='left')

fig = go.Figure(
    data=go.Parcoords(
        line=dict(
            color=df["metadata.final accuracy"],
            colorscale="Electric",
            showscale=True,
            cmin=0,
            cmax=1,
        ),
        dimensions=list(
            [
                dict(label="lr", values=df["metadata.lr"]),
                dict(
                    label="optimizer",
                    range=[0, df["dummy"].max()],
                    tickvals=df["dummy"],
                    ticktext=dfg["metadata.optimizer"],
                    values=df["dummy"],
                ),
                dict(
                    range=[0, 1],
                    label="final accuracy",
                    values=df["metadata.final accuracy"],
                ),
            ]
        ),
    )
)

fig.write_image("output.png")
```
Which gives:

![A parallel coordinates plot, allowing the comparison of several pieces of metadata for all runs in a folder. On the left of the chart, the linear regression value for the simulation is plotted along the y axis. In the centre of the chart, the type of optimizer used (AdamW, SGD or RMSprop) is plotted along the y axis. On the right of the chart, the final accuracy of the simulation is plotted against the y axis. Lines are drawn through each of the corresponding metadata values for each run. The plot shows that using low values for linear regression (between 0 and 0.01), and either the AdamW or RMSProp optimizer, gives the best results (around 85% accuracy overall). ](images/parallel-coordinates.png)

??? further-docs "Further Documentation"

    - [^^The get_runs() method^^](/reference/client#get_runs)

    - [^^The Pandas dataframe plot() method^^](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.plot.html)
    
    - [^^How to create a parallel coordinates plot using Plotly^^](https://plotly.com/python/parallel-coordinates-plot/)