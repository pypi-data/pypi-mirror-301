import functools
import os
import subprocess
import torch
import torch.distributed as dist
import torch.multiprocessing as mp
from typing import Optional, Tuple


def init_dist(launcher: str, backend: str = 'nccl', **kwargs) -> None:
    """Initialize the distributed training environment.

    Args:
        launcher (str): The type of launcher, either 'pytorch' or 'slurm'.
        backend (str): The backend to use for distributed training. Default is 'nccl'.
        **kwargs: Additional arguments for initializing the process group.
    
    Raises:
        ValueError: If an invalid launcher type is provided.
    """
    if mp.get_start_method(allow_none=True) is None:
        mp.set_start_method('spawn')

    if launcher == 'pytorch':
        _init_dist_pytorch(backend, **kwargs)
    elif launcher == 'slurm':
        _init_dist_slurm(backend, **kwargs)
    else:
        raise ValueError(f'Invalid launcher type: {launcher}')


def _init_dist_pytorch(backend: str, **kwargs) -> None:
    """Initialize distributed training using PyTorch native launcher.

    Args:
        backend (str): Backend to use for torch.distributed.
        **kwargs: Additional arguments for initializing the process group.
    """
    rank = int(os.environ['RANK'])
    num_gpus = torch.cuda.device_count()
    torch.cuda.set_device(rank % num_gpus)
    dist.init_process_group(backend=backend, **kwargs)


def _init_dist_slurm(backend: str, port: Optional[int] = None) -> None:
    """Initialize distributed training using SLURM.

    Args:
        backend (str): Backend to use for torch.distributed.
        port (int, optional): Master port. Defaults to None.
            If not provided, the environment variable `MASTER_PORT` is used. If this
            is not set, the default port `29500` is used.
    """
    proc_id = int(os.environ['SLURM_PROCID'])
    ntasks = int(os.environ['SLURM_NTASKS'])
    node_list = os.environ['SLURM_NODELIST']
    num_gpus = torch.cuda.device_count()
    torch.cuda.set_device(proc_id % num_gpus)

    # Retrieve the address of the master node
    addr = subprocess.getoutput(f'scontrol show hostname {node_list} | head -n1')
    
    # Set master port
    if port:
        os.environ['MASTER_PORT'] = str(port)
    elif 'MASTER_PORT' not in os.environ:
        os.environ['MASTER_PORT'] = '29500'

    # Set environment variables for distributed training
    os.environ['MASTER_ADDR'] = addr
    os.environ['WORLD_SIZE'] = str(ntasks)
    os.environ['LOCAL_RANK'] = str(proc_id % num_gpus)
    os.environ['RANK'] = str(proc_id)

    dist.init_process_group(backend=backend)


def get_dist_info() -> Tuple[int, int]:
    """Get the rank and world size for the current distributed process.

    Returns:
        Tuple[int, int]: The rank of the current process and the world size.
            If distributed training is not initialized, returns (0, 1).
    """
    if dist.is_available() and dist.is_initialized():
        rank = dist.get_rank()
        world_size = dist.get_world_size()
    else:
        rank, world_size = 0, 1
    return rank, world_size


def master_only(func):
    """Decorator to ensure that a function is executed only on the master process."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        rank, _ = get_dist_info()
        if rank == 0:
            return func(*args, **kwargs)

    return wrapper
