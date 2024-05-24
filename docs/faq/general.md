# Frequently asked questions: general

## Why is my run in the **lost** state?
The Simvue client sends a heartbeat to the server every minute. A run goes into the **lost** state if there are no heartbeats for over 3 minutes. Because of this,
it is preferable to use the context manager for the `Run()` object, for example:
```
from simvue import Run

if __name__ == "__main__":
    with Run() as run:
        run.init()
        ...
```
If the user's code exits with an exception the state of the run will be set to `failed` and an event will be created with details about this exception. Without the
context manager, i.e.
```
from simvue import Run

if __name__ == "__main__":
    run = Run()
    run.init()
    ...
```
the run automatically be set to the `lost` state if there is an exception and no information is available as to what happened.

## Interactive plots from artifacts
If Matplotlib and Plotly plots are saved directly as artifacts (rather than saved as files first) they can be opened in the web UI as interactive plots. This makes use of `plotly.js` - [^^see here for documentation for plotly.js^^](https://plotly.com/javascript/).

Here is a simple but complete example creating a Matplotlib plot ([^^based on an example from the Matplotlib documentation, seen here^^](https://matplotlib.org/stable/tutorial_basics/introductory/pyplot.html)) and saving it as an artifact. Note the use of the `gcf()` method to get the current figure, as we need to 
pass a `matplotlib.figure.Figure` instance to Simvue.
```
import numpy as np
import matplotlib.pyplot as plt
from simvue import Run

def f(t):
    return np.exp(-t) * np.cos(2*np.pi*t)

if __name__ == "__main__":
    t1 = np.arange(0.0, 5.0, 0.1)
    t2 = np.arange(0.0, 5.0, 0.02)

    plt.figure()
    plt.subplot(211)
    plt.plot(t1, f(t1), 'bo', t2, f(t2), 'k')

    plt.subplot(212)
    plt.plot(t2, np.cos(2*np.pi*t2), 'r--')

    with Run() as run:
        run.init()
        run.save_object(plt.gcf(), 'output', name='plot')
```
Note that we have provided a name for the artifact using the `name` argument, which is essential when creating artifacts directly from Python objects. This name
is completely arbitrary and up to the user.

If you get an error like:
```
Aw. Snap! You're gonna have to hold off on the selfies for now. Plotly can't import images from matplotlib yet!
```
or:
```
AttributeError: 'PathCollection' object has no attribute 'get_offset_position
```
it means that your plot is not compatible with the Plotly conversion function ([^^see documentation for the Plotly conversion function^^](https://plotly.github.io/plotly.py-docs/generated/plotly.html#plotly.tools.mpl_to_plotly)). In this situation the only option currently is to try using Plotly  rather than Matplotlib to create the plot. If you are unfamiliar with this, [^^view the full Plotly documentation^^](https://plotly.com/python/).
