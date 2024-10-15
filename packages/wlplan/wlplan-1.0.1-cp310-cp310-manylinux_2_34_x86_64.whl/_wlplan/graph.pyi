from __future__ import annotations
import typing
__all__ = ['Graph']
class Graph:
    """
    WLPlan graph object.
    
    Graphs have integer node colours and edge labels.
    
    Parameters
    ----------
        node_colours : list[int]
            List of node colours, where `node[i]` is the colour of node `i` indexed from 0.
    
        node_values : list[float], optional
            List of node values. Empty if not provided.
    
        node_names : list[str], optional
            List of node names, where `node_names[i]` is the name of node `i` indexed from 0.
    
        edges : list[list[tuple[int, int]]]
            List of labelled edges, where `edges[u] = [(r_1, v_1), ..., (r_k, v_k)]` represents edges from node `u` to nodes `v_1, ..., v_k` with labels `r_1, ..., r_k`, respectively. WLPlan graphs are directed so users must ensure that edges are undirected.
    
    Attributes
    ----------
        node_colours : list[int]
            List of node colours.
    
        node_values : list[float]
            List of node values. Empty if not provided.
    
        edges : list[list[tuple[int, int]]]
            List of labelled edges.
    
    Methods
    -------
        get_node_name(u: int) -> str
            Get the name of node `u`.
    
        dump() -> None
            Print the graph representation.
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, node_colours: list[int], node_values: list[float], node_names: list[str], edges: list[list[tuple[int, int]]]) -> None:
        ...
    @typing.overload
    def __init__(self, node_colours: list[int], node_values: list[float], edges: list[list[tuple[int, int]]]) -> None:
        ...
    @typing.overload
    def __init__(self, node_colours: list[int], node_names: list[str], edges: list[list[tuple[int, int]]]) -> None:
        ...
    @typing.overload
    def __init__(self, node_colours: list[int], edges: list[list[tuple[int, int]]]) -> None:
        ...
    def __repr__(self) -> str:
        """
        :meta private:
        """
    def dump(self) -> None:
        """
        :meta private:
        """
    def get_node_name(self, u: int) -> str:
        """
        :meta private:
        """
    @property
    def edges(self) -> list[list[tuple[int, int]]]:
        """
        :meta private:
        """
    @property
    def node_colours(self) -> list[int]:
        """
        :meta private:
        """
    @property
    def node_values(self) -> list[float]:
        """
        :meta private:
        """
