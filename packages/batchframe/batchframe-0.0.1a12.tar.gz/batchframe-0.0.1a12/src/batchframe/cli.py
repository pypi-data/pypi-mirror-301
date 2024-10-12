"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
``[options.entry_points]`` section in ``setup.cfg``::

    console_scripts =
         fibonacci = batchframe.skeleton:run

Then run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command ``fibonacci`` inside your current environment.

Besides console scripts, the header (i.e. until ``_logger``...) of this file can
also be used as template for Python modules.

Note:
    This file can be renamed depending on your needs or safely removed if not needed.

References:
    - https://setuptools.pypa.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""

import argparse
import logging
import sys
import os.path
import importlib.util
import asyncio
from types import ModuleType
import nest_asyncio

from kink import di
from batchframe import __version__
from batchframe.executor import AsyncExecutor
from batchframe.models.batchframe_param import init_all_params
from batchframe.models.configuration import Configuration
from batchframe.visuals import SPLASH_LOGO
from batchframe import helpers
from rich.logging import RichHandler
from datetime import datetime
from typing import Optional
from kink import inject
import pathlib

_logger = logging.getLogger(__name__)
nest_asyncio.apply()

executor: AsyncExecutor

def _import_module_from_path(module_name: str, path: str):
    module_spec = importlib.util.spec_from_file_location(module_name, path, submodule_search_locations=[])
    if module_spec is None or module_spec.loader is None:
        raise ValueError("Module spec could not be created from " + path)
    else:
        module = importlib.util.module_from_spec(module_spec)
        sys.modules[module_name] = module
        module_spec.loader.exec_module(module)

# TODO: Maybe outsource this to kink: https://github.com/kodemore/kink/issues/62
# TODO: Exclude stdlib classes like ABC and Generic
def alias_unavailable_parent_classes():
    new_aliases: dict[type, type] = {}
    for service in di._services.keys():
        if type(service) is not str:
            for parent in service.__mro__[1:-1]: # type: ignore
                if not (parent in di._services or parent in di._aliases or parent in new_aliases):
                    new_aliases[parent] = service # type: ignore
    
    for parent, service in new_aliases.items():
        _logger.debug(f'Adding {service} as alias for {parent}.')
        inject(service, alias=parent)

def exec(args: argparse.Namespace):
    print(SPLASH_LOGO + f' {helpers.get_version()}\n')
    global executor
    path: str = args.script_or_folder
    config_module: Optional[ModuleType] = None
    if os.path.isfile(path):
        _logger.debug(f"Loading file {path} as a module...")
        module_name = f'batch_script_file'
        _import_module_from_path(module_name, path)
    elif os.path.isdir(path):
        _logger.debug(f"Loading directory {path} as a module...")
        module_name = f'batch_script_directory'
        path = os.path.join(path, '__init__.py')
        _import_module_from_path(module_name, path)
    if args.configuration is not None:
        stripped_config_name = str(args.configuration).replace(".py", "")
        config_module_name = f"{module_name}.config.{stripped_config_name}"
        _logger.debug(f"Loading configuration {config_module_name}...")
        config_module = importlib.import_module(config_module_name)

    found_configurations = helpers.get_all_inheritors(Configuration)
    found_configurations = [clazz for clazz in found_configurations if clazz in di]
    if config_module is not None:
        found_configurations = [clazz for clazz in found_configurations if clazz.__module__ == config_module_name]
    if len(found_configurations) > 1:
        raise RuntimeError("Too many injectable configuration classes found! Please only provide one.")
    elif len(found_configurations) != 0:
        inject(found_configurations.pop())

    alias_unavailable_parent_classes()

    if hasattr(args, 'params') and args.params is not None:
        parsed_param_args = _parse_batchframe_param_args(args.params)
        init_all_params(parsed_param_args)
    else:
        init_all_params({})

    executor = di[AsyncExecutor]
    asyncio.run(executor.execute())



def _parse_batchframe_param_args(args: list[str]) -> dict[str, str]:
    """Parses a list of KEY=VALUE strings into a corresponding dict.
    Args:
        args (list[str]): List like ["k1=val1", "k2=val2"]

    Raises:
        ValueError: If one of the strings does not contain an equals sign.

    Returns:
        dict[str, str]: See summary.
    """
    res: dict[str, str] = {}

    for arg in args:
        if "=" not in arg:
            raise ValueError(f"Parameter argument {arg} has no '=' sign to differentiate name and value!")
        else:
            split_arg = arg.split("=")
            key = split_arg[0].strip()
            value = split_arg[1].strip()
            if len(split_arg) > 1:
                value = "=".join(split_arg[1:])
            res[key] = value
    
    return res


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def parse_args(args: list[str]) -> argparse.Namespace:
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    main_parser = argparse.ArgumentParser(description="A cli tool for easy local execution of batch jobs.")
    main_parser.add_argument(
        "--version",
        action="version",
        version=f"batchframe {__version__}",
    )
    main_parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    main_parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    main_parser.add_argument(
        "-d",
        "--output-dir",
        dest="output_dir",
        help="output directory for all run-related files, including logs.",
        default="./batchframe_outputs"
    )

    subparsers = main_parser.add_subparsers(title="Command")

    execute_parser = subparsers.add_parser("exec")
    execute_parser.add_argument("script_or_folder")
    execute_parser.set_defaults(func=exec)

    execute_parser.add_argument(
        "-p",
        "--param",
        dest="params",
        metavar="NAME=VALUE",
        action='append',
        help="A batchframe parameter denoted by the BathframeParam type annotation."
    )

    execute_parser.add_argument(
        "-c",
        "--configuration",
        dest="configuration",
        help="Name of the python file holding the desired configuration. Applicable only for directory-based modules.",
        required=False
    )

    version_parser = subparsers.add_parser("--version")
    version_parser.set_defaults(func=helpers.get_version)

    parsed, extras = main_parser.parse_known_args(args)

    return parsed 

def inject_static_parameters(args: argparse.Namespace):
    """Make some common arguments available to the DI container.
    These are usually needed before the job-specific parameters are initialized.
    """
    run_start_time = datetime.now()

    # TODO: Try getting the names of these properties programmatically 
    di["_output_directory"] = args.output_dir
    di["_current_run_start"] = run_start_time
    di["_current_run_output_dir"] = os.path.join(args.output_dir, run_start_time.isoformat())

def setup_logging(loglevel, log_directory):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    pathlib.Path(log_directory).mkdir(parents=True, exist_ok=True)
    log_file_path = os.path.join(log_directory, "logs.txt")

    logging.basicConfig(
        level=loglevel,
        format=logformat,
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[RichHandler(rich_tracebacks=True), logging.FileHandler(log_file_path)]
    )


def main(args: list[str]):
    """Wrapper allowing :func:`fib` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`fib`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    parsed_args = parse_args(args)
    inject_static_parameters(parsed_args)
    setup_logging(parsed_args.loglevel, di["_current_run_output_dir"])
    parsed_args.func(parsed_args)


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m batchframe.skeleton 42
    #
    run()
