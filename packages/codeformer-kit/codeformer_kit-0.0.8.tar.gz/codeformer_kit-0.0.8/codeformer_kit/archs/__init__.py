import importlib
from copy import deepcopy
from os import path as osp
from typing import Dict, Any

from codeformer_kit.utils import get_root_logger, scandir
from codeformer_kit.utils.registry import ARCH_REGISTRY

__all__ = ['build_network']

# Automatically scan and import architecture modules for registry
arch_folder = osp.dirname(osp.abspath(__file__))

# Scan for files ending with '_arch.py' in the 'archs' folder
arch_filenames = [
    osp.splitext(osp.basename(v))[0]
    for v in scandir(arch_folder) if v.endswith('_arch.py')
]

# Import all architecture modules
_arch_modules = [
    importlib.import_module(f'codeformer_kit.archs.{file_name}')
    for file_name in arch_filenames
]


def build_network(opt: Dict[str, Any]) -> Any:
    """Build a network based on the provided options.

    Args:
        opt (dict): A dictionary containing the network options, including its type and other parameters.

    Returns:
        object: The instantiated network object.
    """
    # Create a deep copy of the options to avoid modifying the original
    opt_copy = deepcopy(opt)

    # Pop the 'type' key from the options to determine the network type
    network_type = opt_copy.pop('type')

    # Retrieve and instantiate the network class from the registry
    network_class = ARCH_REGISTRY.get(network_type)
    if network_class is None:
        raise ValueError(f"Network type '{network_type}' is not registered.")

    # Instantiate the network with the remaining options
    net = network_class(**opt_copy)

    # Log the creation of the network
    logger = get_root_logger()
    logger.info(f'Network [{net.__class__.__name__}] is created.')

    return net
