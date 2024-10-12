import numpy as np
from numpy.typing import NDArray

class FastaMapping:
    """
    Holds character level mappings from FASTA characters to integer values.
    Passed to parsing methods for FASTAs.
    """
    def __init__(self, mapping: dict[str, int], default_value: int):
        ...
    def __str__(self) -> str:
        ...
    def __repr__(self) -> str:
        ...

def parse_fasta(path: str, mapping: FastaMapping) -> tuple[NDArray[np.uint8], NDArray[np.int64], NDArray[np.int64]]:
    """
    Parses input fasta file, specified with **path** according to the **mapping**. Function executes on parallel threads.

    Function returns a tuple of data, sequence descriptors and taxon ids.
    """
    ...

def concatenate_numpy(arrays: list[NDArray]) -> tuple[NDArray[np.uint8], NDArray[np.int64]]:
    """
    Concatenates a given list of numpy arrays into a data and sequence descriptor arrays. Function executes on parallel threads.
    """
    ...

def concatenate_awkward(awkwards: list[tuple[NDArray, NDArray[np.int64]]]) -> tuple[NDArray[np.uint8], NDArray[np.int64]]:
    """
    Concatenates a given list of awkward arrays into a single awkward array. Function executes on parallel threads.
    """
    ...
    
def awkward_from_list_of_numpy(arrays: list[NDArray]) -> tuple[NDArray[np.uint8], NDArray[np.int64]]:
    """
    Constructs awkward arrays form a list of numpy arrays. Function executes on parallel threads.
    """
    ...

def parse_cluster_member_fasta(path: str, mapping: FastaMapping) -> tuple[NDArray[np.uint8], NDArray[np.int64], NDArray[np.uint32], NDArray[np.uint32]]:
    """
    Parses input fasta file with sub cluster headers, specified with **path** according to the **mapping**. Function executes on parallel threads.

    Function returns a tuple of data, sequence descriptors and taxon ids.
    """
    ...

def find_boundaries_u32(arr: NDArray[np.uint32]) -> NDArray[np.int64]:
    """
    Looks for boundaries in the given array and returns them in a numpy array.
    """
    ...

def find_chunk_boundaries(sequence_lengths: NDArray[np.int64], chunk_tokens: int) -> NDArray[np.int64]:
    """
    Looks for boundaries in the given array that are shorter than **chunk_tokens** and returns them in a numpy array.
    """
    ...
