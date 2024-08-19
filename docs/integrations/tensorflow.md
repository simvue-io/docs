# TensorVue Callback

TensorFlow is an open-source machine learning library developed by Google, which allows you to design and create custom Machine Learning algorithms. These algorithms can take a long time to train, with accuracy and loss statistics reported after each epoch. To make it easy to keep track of these statistics as the training progresses, a Keras Callback has been created to upload information about the training of any Tensorflow Keras model to Simvue.

!!! further-docs
    To view a detailed example of monitoring the training of a Tensorflow ML algorithm using the TensorVue callback, [^^see the example here.^^](/examples/tensorflow)

## What is tracked

By default, the `TensorVue` callback will create a `Simulation` run, which represents the training of the entire model and contains statistics collected after each training epoch, and a series of `Epoch` runs, which contains statistics for a specific epoch collected after each training batch (this can be disabled if desired). If you have a separate validation session using `model.evaluate`, then an `Evaluation` run will also be created. The following things are tracked by the `TensorVue` callback:

- Uploads the Python script creating the model as a `Code` Artifact
- Uploads the model config as an `Input` Artifact
- Uploads parameters about the model as Metadata
- Uploads the Training Accuracy and Loss after each batch to an Epoch run
- Uploads the Training and Validation Accuracy and Loss after each Epoch to the Simulation run
- Uploads model checkpoints after each Epoch to the corresponding Epoch run as `Output` Artifacts(if enabled by the user)
- Uploads the final model to the Simulation run as an `Output` Artifact

## Usage

To use the `TensorVue` class, you must have the `simvue_integrations` repository installed. Create a virtual environment if you haven't already:
```
python -m venv venv
source venv/bin/activate
```
Then install the repository using `pip`:
```
pip install git+https://github.com/simvue-io/integrations.git@main#egg=simvue-integrations[tensorflow]
```

Before beginning training for your Tensorflow model, you need to create an instance of the TensorVue class. This class can take the following arguments:

   - `run_name`: Name of the Simvue run to create
   - `run_folder`: Name of the folder to store the run in, will create a folder with the same name as the run if not specified
   - `run_description`: Description of the run, optional
   - `run_tags`: List of tags associated with the run, optional
   - `run_mode`: Whether Simvue should run in Online or Offline mode, by default Online
   - `alert_definitions`: Definitions of any alerts to add to the run as a dictionary of key/value pairs, optional
   - `manifest_alerts`: If using the Optimisation framework, which of the alerts defined above to add to the manifest run, by default None
   - `simulation_alerts`: Which of the alerts defined above to add to the simulation run, by default None
   - `epoch_alerts`: Which of the alerts defined above to add to the epoch runs, by default None
   - `evaluation_alerts`: Which of the alerts defined above to add to the evaluation runs, by default None
   - `start_alerts_from_epoch`: The number of the epoch which you would like to begin setting alerts for, by default 0
   - `script_filepath`: Path of the file to upload as Code to the simulation run, by default uses the file where the callback was instantiated
   - `model_checkpoint_filepath`: If using the ModelCheckpoint callback, the path where the checkpoint files are saved after each epoch, optional
   - `model_final_filepath`: The location where the final model should be stored after training is complete, by default `/tmp/simvue/final_model.keras`
   - `evaluation_parameter`: The parameter to check the value of after each Epoch, either 'accuracy', 'loss', 'val_accuracy', or 'val_loss', optional
   - `evaluation_target`: The target value of the parameter, which will cause the training to stop if satisfied, optional
   - `evaluation_condition`: How you wish to compare the latest value of the parameter to the target value, either '<', '>', '<=', '>=', '==', optional
   - `create_epoch_runs`: bool, Whether to create runs for the training data for each Epoch individually, by default True
   - `optimisation_framework`: Whether to use the Simvue ML Optimisation framework, by default False
   - `simulation_run`: If using the ML Opt framework and this callback is being called within the simulation function, the 'data' run which has been created by the framework for this trial, by default None
   - `evaluation_run`: If using the ML Opt framework and this callback is being called within the evaluation function, the 'eval' run which has been created by the framework for this trial, by default None

Your Python script may look something like this:
```py
from tensorflow import keras
from simvue_integrations.connectors.tensorflow import TensorVue

# Define your model
model = keras.Sequential()
model.add(keras.layers.Flatten(input_shape=(28, 28)))
model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.01),
            loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            metrics=['accuracy'])

# Load your training data        
img_train, label_train, img_test, label_test = keras.datasets.fashion_mnist.load_data()

# Initialise your callback - minimum required is the Simvue run name, but can include any other details described above
tensorvue = sv_tf.TensorVue("recognising_clothes")

# Fit the model, using the tensorvue callback
model.fit(
    img_train,
    label_train,
    epochs=10,
    validation_split=0.2,
    callbacks=[tensorvue,]
)

# Evaluate the model, again using the tensorvue callback
results = model.evaluate(
    img_test,
    label_test,
    callbacks=[tensorvue,]
)
```

## Adding Functionality
If you wish to store more data than the default TensorVue callback provides, you can create your own callback class which inherits from TensorVue. For detailed information on creating your own custom callbacks, [^^see this guide^^](https://www.tensorflow.org/guide/keras/writing_your_own_callbacks).

For example, say you wanted the callback to upload the final accuracy and loss measurements as metadata to the Simvue run. To do this we will inherit from TensorVue, but override the `on_train_end()` method to add our new functionality:

```py
class MyTensorVue(sv_tf.TensorVue):
    # This method will be called whenever a training session ends
    def on_train_end(self, logs):

        # Accuracy and Loss measurements are stored in `logs`:
        final_measurements = {
            "final_accuracy": logs.get("accuracy"),
            "final_loss": logs.get("loss")
        }

        # You can then access the Simulation run to upload these values to through `self.simulation_run`
        # Any of the methods available in the standard `simvue.Run` class are available here
        self.simulation_run.update_metadata(final_measurements)

        # Don't forget to then call the base TensorVue method!
        super().on_train_end(logs)
```
