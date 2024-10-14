from typing import TYPE_CHECKING, Any, Dict, List, Union

if TYPE_CHECKING:
    import builtins
    EllipsisType = builtins.ellipsis
else:
    EllipsisType = Any


def contains(params: Dict[str, str]) -> List[Union[List[str], EllipsisType]]:
    """
    Converts a dictionary into a list of its key-value pairs, each as a sublist.
    Includes ellipses at the start and end of the list.

    :param params: The dictionary to be converted.
    :return: A list containing the key-value pairs as sublists, with ellipses at both ends.
    """
    if len(params) == 0:
        raise ValueError("dictionary cannot be empty")
    return [...] + [[key, val] for key, val in params.items()] + [...]


__all__ = ("contains",)
