# Basic Tensorflow example

This example demonstrates using Simvue to track a simple Python code, in particular:

- Collecting some metadata,
- Saving the Python script,
- Logging some metrics while the training is running,
- Adding some additional metadata containing the final values of the metrics.

The code is based on the dynamic recurrent neural network example from [here](https://github.com/aymericdamien/TensorFlow-Examples/).

## Running the code

To run this example, firstly clone the Simvue client GitHub repository:
```sh
git clone https://github.com/simvue-io/client
cd client/examples
```
Create a virtual environment (Linux):
```sh
python3 -m venv venv
source venv/bin/activate
```
Create a virtual environment (Windows):
```sh
python3 -m venv venv
venv\Scripts\activate
```

Install the required dependencies:
```sh
pip install --upgrade pip
pip install tensorflow simvue
```
Ensure that Simvue is configured properly, for example by creating a `.simvue.ini` file in your home directory. Click on `Create new run`
in the UI for more information.

Change directory to Tensorflow folder (cd Tensorflow) and run the code:
```sh
python3 dynamic_rnn.py
```

## Explanation

To begin with we import the required class:
```python
from simvue import Run
```
We next initialise the run and specify metadata:
``` py
run = Run()
run.init(metadata={'dataset.num_classes': num_classes,
                   'dataset.seq_max_len': seq_max_len,
                   'dataset.seq_min_len': seq_min_len,
                   'dataset.masking_val': masking_val,
                   'training.learning_rate': learning_rate,
                   'training.training_steps': training_steps,
                   'training.batch_size': batch_size,
                   'network.num_units': num_units})
```
The Python code itself is saved:
``` py
run.save('dynamic_rnn.py', 'code')
```
During the part of the code which carries out the training we log metrics:
``` py
run.log_metrics({'loss': float(loss), 'accuracy': float(acc)})
```
Once the training has completed we add some metadata specifying the final values of the metrics:
``` py
run.update_metadata({'loss': float(loss), 'accuracy': float(acc)})
```

Finally we finish the run:
``` py
run.close()
```

## Results

As well as having a record of metadata associated with the training run you can visualize the metrics in real-time,
for example loss:
<figure markdown>
  ![OpenFOAM residuals](images/tensorflow-loss.png){ width="1000" }
</figure>

