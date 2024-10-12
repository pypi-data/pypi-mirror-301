<!-- These are examples of badges you might want to add to your README:
     please update the URLs accordingly

[![Built Status](https://api.cirrus-ci.com/github/<USER>/batchframe.svg?branch=main)](https://cirrus-ci.com/github/<USER>/batchframe)
[![ReadTheDocs](https://readthedocs.org/projects/batchframe/badge/?version=latest)](https://batchframe.readthedocs.io/en/stable/)
[![Coveralls](https://img.shields.io/coveralls/github/<USER>/batchframe/main.svg)](https://coveralls.io/r/<USER>/batchframe)
[![PyPI-Server](https://img.shields.io/pypi/v/batchframe.svg)](https://pypi.org/project/batchframe/)
[![Conda-Forge](https://img.shields.io/conda/vn/conda-forge/batchframe.svg)](https://anaconda.org/conda-forge/batchframe)
[![Monthly Downloads](https://pepy.tech/badge/batchframe/month)](https://pepy.tech/project/batchframe)
[![Twitter](https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter)](https://twitter.com/batchframe)
-->

[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/)
![PyPI - Version](https://img.shields.io/pypi/v/batchframe)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/batchframe)

# ![logo](./assets/Batchframe_Logo_Small.png) Batchframe

> A python framework for decomposable, repetitive tasks.

This CLI tool/framework aims to provide out-of-the-box functionality for many common tasks one might have when building python scripts that do a simple task repeatedly.
It works on the "Don't Call Us, We'll Call You" principle.
You implement a few abstract classes and call the CLI tool on your project.
It runs your code and abstracts away much of the boilerplate you'd need to write.

Features include:
- Automatic capture of logs to files.
- Type-safe capture of CLI parameters.
- Ability to pause execution and inspect objects in the python shell.
- Colorful visualization of progress and similar statistics.
- Retry logic with backoff.
- Dependency injection.
- Pseudo-parallelism with AsyncIO.
- Fully-typed, class-based configuration.
- Saving of failed inputs for future re-execution.

![Execution example](./assets/example_execution.webm)

## Installation
```
pip install batchframe
```

## Features in Depth

### Automatic Capture of Logs to Files
Batchframe will save the logs of the current run under `OUTPUT_DIR/current_datetime/`,
where `OUTPUT_DIR` defaults to `batchframe_outputs`, but can be changed with the `-d` flag.

### Type-safe Capture of CLI Parameters
Usually any non-trivial python program requires some user input, for example, a path to a file that should be read.
Argv alone works for very simple cases, but very quickly one needs to start using [argparse](https://docs.python.org/3/library/argparse.html) to handle the complexity of user input.
The tool is as versatile as it gets, but is often too verbose for workloads batchframe is intended for.

We abstract this complexity away by providing a generic type called `BatchframeParam[T]`, where `T` is the type variable.
All one needs to do is to annotate the desired input with this type inside any constructor, and Batchframe will automatically ask for it when running.
When the required parameters are provided, they will be cast and injected automatically, as long as the class itself has an `@inject` annotation.

For example, let's say you want a `str` and an optional `datetime` parameter in your service.
You'd write the constructor like so:
```python
from batchframe import BatchframeParam, Service, inject
from datetime import datetime

@inject
class MyService(Service):
     def __init__(self, file_path: BatchframeParam[str], search_from: BatchframeParam[datetime] = datetime.now()):
          # Do some stuff here
```
You would then provide these values like so: `... -p file_path=./here.txt -p search_from 2024-01-03`.

This is also useful for overriding values in the `Configuration` class.

Currently, the list of supported injectable types is limited, but we're constantly adding more!

### Ability to Pause Execution and Inspect Objects in the Python Shell
Batchframe features a "pause shell" that allows the user to interrupt execution (Ctrl-C) and access all parts of running system through a fully-featured ipython shell.
This shell is also activated when a fatal error occurs, giving the user a chance to save the execution progress.

Execution can be completely stopped, while saving all failed/unprocessed work items by calling `self.stop()` inside the pause shell.

### Dependency Injection
**Keep in mind that this API is currently experimental and subject to change.**

Batchframe uses [kink](https://github.com/kodemore/kink) under the hood to automatically resolve dependencies between classes and inject configuration parameters.
In order for your class to be included in the DI system, decorate it with the `@inject` decorator like this:
```python
from batchframe import inject
from batchframe.models.service import Service

@inject()
class MyService(Service):
     pass
```
Batchframe automatically "aliases" all parent classes with the decorated class if they are not already set.
This means that `MyService` will be injected where ever `Service` is requested.

This is the same as using the decorator like so: `@inject(alias=Service)` and is sometimes required to be done manually.

### Fully-typed, Class-based Configuration
**Keep in mind that this API is currently experimental and subject to change.**

Instead of plain text files, Batchframe uses typed python dataclasses for configuration.
In theory, this makes configuration easier to work with, avoids duplication and improves flexibility.

Since there are still some kinks to work out with the API,
please refer to the `package_module` directory under `examples` for the latest working implementation of this system.

## Usage

### Writing a Project for Batchframe
Each Batchframe project consists of at least these two parts:
- A `Source` class, which provides the input data.
- A `Service` class, containing the execution logic.

Once you have implemented these two abstract classes provided by Batchframe,
its internal executor iterates through `Source` and gives the output to the `Service`.
This setup is extremely simple for the user and yet allows Batchframe to abstract away all of the repetitive tasks
associated with tools that work through a large number of inputs.

As an example, here's a very simple `Source`, which just emits numbers from one to ten:
```python
from batchframe import Source, inject
import logging

@inject
class TestSource(Source[int]):
    _curr_count = 0

    def __len__(self) -> int:
        return 10
    
    def next(self) -> int:
        self._curr_count += 1
        if self._curr_count <= 10:
            return self._curr_count
        else:
            raise StopIteration()

    def persist_failed(self, failed: list[int]):
        logging.error(f'Oh no! {failed} did not compute!')
```
A `Source` has just three methods that need to be implemented: `__len__`, `next` and `persist_failed`.
With these three functions, you can implement any finite source of task inputs,
for example reading from a database, a filesystem, a dataframe...
You also have the ability to save any inputs that caused issues during processing.

Continuing with the example, here's a very simple `Service` that just takes an input of any `int`,
multiplies it by itself, sleeps to simulate work, and logs the output:
```python
from batchframe import Service, inject
import asyncio
import logging

@inject
class TestService(Service):

    source: Source
    _exceptions_to_retry_for = {ValueError}
    
    @property
    def exceptions_to_retry_for(self) -> set[type[Exception]]:
        return self._exceptions_to_retry_for

    def __init__(self, source: Source) -> None:
        self.source = source

    async def process(self, input: int):
        await asyncio.sleep(0.1)
        logging.info(input*input)
        
    def finish(self):
        logging.info("I could do some cleanup here...")

```
A `Service` also has just three methods to implement: `__init__`, `process` and `finish`,
with the addition of a mandatory property `exceptions_to_retry_for`, written as a method.

Let's focus on the `process` method, as this is where the core of your project lies.
Here, you can implement essentially any processing logic that should be executed on the output of `Source`,
such as calling an API, doing transformations, saving to disk and so on.
As the method is a coroutine, using libraries that utilize `asyncio` is recommended for performance reasons.
The `process` method gets called multiple times "at the same time" in the event loop.

The `finish` method is just there to allow you do to some cleanup, for example closing of output streams.

The `exceptions_to_retry_for` is a list of exceptions that,
when thrown in `process` cause Batchframe to save the causing input and retry calling `process` at a later time.

#### Dependency Injection

You might have noticed the `@inject` annotation on both classes.
This tells Batchframe to include these two classes in its dependency injection process,
meaning that you just need to point the CLI at the right python script or directory,
and everything will be picked up automatically.
This also means that Batchframe will auto-inject any arguments into the constructor.
For example, you could ask the user for the path of a file to be read in `Source` by writing its constructor like so:
```python
from batchframe import Service, inject, BatchframeParam

@inject
class TestSource(Source[int]):

    def __init__(self, file_path: BatchframeParam[str]):
        # Load file here
     
     # Other mandatory methods...
```
Essentially any python class can be injected, meaning you can encapsulate logic into different services and call them
from any other class you want.

For more information on CLI parameter injection, refer to the "Type-safe Capture of CLI Parameters" section above.

### Configuration
Batchframe does away with envfiles and uses Python's  [dataclasses](https://docs.python.org/3/library/dataclasses.html) as vessels for config data.
Let's take a simplified project where we have two environments as an example.
The files on disk would look something like this:
```
my_simple_project/
├─ config/
│  ├─ config_dev.py
│  ├─ config_prod.py
│  ├─ abstract_custom_config.py
├─ source.py
├─ service.py
```

The class in `abstract_custom_config.py` would contain common properties for all implementations in the `config` directory.
For example something like this:
```python
from batchframe import Configuration
from dataclasses import dataclass
from abc import ABCMeta

@dataclass()
class AbstractCustomConfig(Configuration, metaclass=ABCMeta):
    env: str = "PLACEHOLDER"
```

The config implementations would look something this:
```python
from dataclasses import dataclass
from .abstract_custom_config import AbstractCustomConfig
from batchframe import inject

# file: config_dev.py
@inject
@dataclass()
class CustomDevConfig(AbstractCustomConfig):
     env: str = "DEV"

# file: config_prod.py
@inject
@dataclass()
class CustomProdConfig(AbstractCustomConfig):
     env: str = "PROD"
```
You have to point batchframe to which configuration you want to use with the `-c` flag.
For example `batchframe exec -c config_dev ...`.
Keep in mind that batchframe always looks in the `config` directory.
This might be changed in the future. 

Finally, one would use one of these configurations like so:

```python
from .config.abstract_custom_config import AbstractCustomConfig

@inject
class TestSource(Source[int]):

    def __init__(self, config: AbstractCustomConfig):
        # Use config here...
     
     # Other mandatory methods...
```

#### Static Configuration Parameters
The default Batchframe `Configuration` includes so-called static parameters.
These are injected by the runtime and are not meant to be overriden by the caller.
Static parameters are denoted by a leading underscore and include things like `_current_run_output_dir`,
which is built from the current run time and the directory supplied by the `-d` flag (`batchframe_outputs` by default).

We strongly suggest looking at the `examples` directory and calling Bachframe on those projects to see everything in action!

### CLI
Run `batchframe exec PATH_TO_MODULE --params param1=value1...`
where `PATH_TO_MODULE` is one of the following:
- A single python file containing all the necessary classes.
- A single python file in a directory-style project that imports all the necessary classes (usually your service file does this naturally).
- A directory containing an `__init__.py` file that imports all the necessary classes.

If you are using a directory-style project, supply the name of the desired configuration file with the `-c` flag.
This will automatically alias the built-in Batchframe `Configuration` class.
You should not include configuration files in `__init__.py` or the file you're pointing batchframe to. 

See the `examples` directory for inspiration.

<!-- pyscaffold-notes -->

## Development
This project uses [pipenv](https://pipenv.pypa.io/en/latest/) to make the management of dependencies in dev environments easier.
To create a virtual environment with all of the required dependencies, run `pipenv sync -d`.
When adding new runtime dependencies to `setup.cfg`, run `pipenv install && pipenv lock`.
When adding new dev dependencies to `setup.cfg`, you have to also add them to pipenv by running `pipenv install --dev DEPENDENCY`
Activate the virtual environment in your terminal with `pipenv shell`.

## Releasing
This project has dev and prod releases on TestPyPi and PyPi respectively.
Packages are built in the GitLab pipeline.

## Planned features/improvements
- Import entire directories without \_\_init__.py
- Support iterables for BatchframeParam
- Publish via the [trusted publisher workflow](https://docs.pypi.org/trusted-publishers/using-a-publisher/#gitlab-cicd).
- Add reasons for failed work items.
- Extract parameter descriptions from pydoc.
- Auto-generate UI.
- Have an actual multi-threading/multi-processing executor.
- Have default implementation of exceptions_to_retry_for
- Prevent shell autocompletion breaking with parameters
- `batchframe init` - create a template module-based project
- Explore using protocols instead of abstract classes?

### Debugging
You can find some debugging examples in the `.vscode/launch.json` file.
As the name suggests, these work out-of-the-box with Visual Studio Code.

### Known Bugs
- Updating the number of failed items doesn't always work. Looks like a race condition or a bug with the rich library.

## Note

This project has been set up using PyScaffold 4.5. For details and usage
information on PyScaffold see https://pyscaffold.org/.
