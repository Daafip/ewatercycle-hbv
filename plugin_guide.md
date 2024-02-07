# Add your model to eWaterCycle

To add a model to eWaterCycle, you will need to start with a model that has the Basic Model Interface implemented.
For an example of that, there is the (Python) [leakybucket-bmi](https://github.com/eWaterCycle/leakybucket-bmi).

Next you have to follow these steps:

1. Package your model in a container with grpc4bmi
2. Wrap your model in the eWaterCycle interface 
3. Register your model as an eWaterCycle plugin
4. Put your plugin on PyPI

## Container with grpc4bmi
In eWaterCycle models are stored in (Docker) container images, which can be shared through the Github Container Registry or DockerHub.

Besides the model code, the container image should install the grpc4bmi server as an entrypoint to enable communication with the model from outside of the container.
We use standardized image names including a unique version number for the model.

Concretely, these are the steps you should follow:
 - Create Docker container image named `ewatercycle/<model>-grpc4bmi:<version>` with grpc4bmi server running as entrypoint. For detailed instructions and examples, please see the [grpc4bmi docs](https://grpc4bmi.readthedocs.io/en/latest/container/building.html).
 - Host Docker container image on the [Github registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry).

Again, for an example see the [leakybucket-bmi](https://github.com/eWaterCycle/leakybucket-bmi) repository, which includes a Dockerfile.

> Note: if you have a Python BMI, you can use the model without a container for testing purposes, more info is available [down below](#local-python-model-no-container).

## Wrapping your model in the eWaterCycle interface

To be able to interface your model in eWaterCycle, you need to wrap it in an eWaterCycle model class.
The eWaterCycle wrapper adds some additional BMI utilities that are relevant for hydrological models, and it can also combine the 'bare' BMI model with forcing data and parameter sets. It is modelled after [PyMT](https://csdms.colorado.edu/wiki/PyMT), but additionally it can run BMI models inside containers.

This model class will have to handle the forcing and/or parameter set input, as well as the model configuration file.

It is stuctured like the following:

```py
from ewatercycle.base.model import ContainerizedModel, eWaterCycleModel

# This "methods" class implements the eWaterCycle interface, and can be reused.
class MyPluginMethods(eWaterCycleModel):
    forcing: GenericLumpedForcing  # Models usually require forcing.

    parameter_set: ParameterSet  # If the model has a parameter set

    _config: dict = {  # _config holds model configuration settings:
        "forcing_file": "",
        "model_setting_1": 0.05,
    }

    @model_validator(mode="after")
    def _update_config(self):
        ... # Update the config, e.g., by adding the forcing directory.
        return self

    def _make_cfg_file(self, **kwargs) -> Path:
        """Write model configuration file."""
        ... # Write the config to a file to pass it to your model BMI.

class MyModel(ContainerizedModel, MyPluginMethods):
    # The local model uses a local BMI class
    bmi_image: ContainerImage = ContainerImage(
        "ghcr.io/organization/model:v0.0.1"
    )
```

The LeakyBucket implementation can be found [here](src/ewatercycle_leakybucket/model.py).
This is a good starting point to build upon.

### eWaterCycle Forcing

For generating and loading model forcing, eWaterCycle makes use of a Forcing class.
When generating forcing, ESMValTool recipes are used. This allows for standardized and reproducible forcing.

If you are making a new model, you can use the GenericForcing, which has a lumped and a gridded version available.

Otherwise you will have to make your own custom forcing class. For more info on this, see [the eWaterCycle documentation on forcing.](https://ewatercycle.readthedocs.io/en/latest/user_guide.html#Forcing-data).


## eWaterCycle plugin entry-point:
Finally, the model can be registered as a plugin so that eWaterCycle can find it.
This is done in the `pyproject.toml` file:

```toml
# This registers the plugin such that it is discoverable by eWaterCycle
[project.entry-points."ewatercycle.models"]
MyModel = "mymodel.ewatercycle_model:MyModel"
```

Here you would replace the leaky bucket names with the correct model and class name of your own model.

Now you can do:

```py
from ewatercycle.models import MyModel
```

And run the model in eWaterCycle! 🚀


## Putting your plugin on PyPI

After finishing the previous steps, you should upload the finished package to pypi.org.
For information on packaging your project, see [the Python documentation](https://packaging.python.org/en/latest/tutorials/packaging-projects/).

This will allow others to install it into their eWaterCycle installation using (for example):
```sh
pip install ewatercycle-mymodel
```

If you have developed a plugin for eWaterCycle, get your model listed on the [eWatercycle plugins page](https://ewatercycle.readthedocs.io/en/latest/plugins.html) by making a [Pull request](https://github.com/eWaterCycle/ewatercycle/edit/main/docs/plugins.rst).

# Tips & tricks

### Local Python model (no container)
For testing purposes you can directly use a Python model's BMI in eWaterCycle.
For this you need to combine the eWaterCycle class methods with the eWaterCycle LocalModel as such:

```py
from ewatercycle.base.model import LocalMode
from leakybucket import LeakyBucketBmi
from ewatercycle_leakybucket.model import LeakyBucketMethods

class LocalModelLeakyBucket(LocalModel, LeakyBucketMethods):
    """The LeakyBucket eWaterCycle model, with the local BMI."""
    bmi_class: Type[Bmi] = LeakyBucketBmi
```

Where LeakyBucketBmi is your local model's BMI class.
