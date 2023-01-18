# Frequently asked questions: general

## What happens if my code crashes?
The Simvue client sends a heartbeat to the server every minute. A run goes into the **lost** state if there are no heartbeats for over 3 minutes.

## Interactive plots from artifacts
If Matplotlib and Plotly plots are saved directly as artifacts (rather than saved as files first) they can be opened in the web UI as interactive plots. This makes use of [plotly.js](https://plotly.com/javascript/).

Here is a simple but complete example creating a Matplotlib plot and saving it as an artifact. Note the use of the `gcf()` method to get the current figure, as we need to 
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
        run.save(plt.gcf(), 'output', name='plot')
```
Note that we have provided a name for the artifact using the `name` argument, which is essential when creating artifacts directly from Python objects. This name
is completely arbitrary and up to the user.
