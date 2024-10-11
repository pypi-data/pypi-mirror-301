"""MQT DDSim Python Package."""

from __future__ import annotations


# start delvewheel patch
def _delvewheel_patch_1_8_2():
    import os
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'mqt_ddsim.libs'))
    if os.path.isdir(libs_dir):
        os.add_dll_directory(libs_dir)


_delvewheel_patch_1_8_2()
del _delvewheel_patch_1_8_2
# end delvewheel patch

from ._version import version as __version__
from .provider import DDSIMProvider
from .pyddsim import (
    CircuitSimulator,
    ConstructionMode,
    DeterministicNoiseSimulator,
    HybridCircuitSimulator,
    HybridMode,
    PathCircuitSimulator,
    PathSimulatorConfiguration,
    PathSimulatorMode,
    StochasticNoiseSimulator,
    UnitarySimulator,
    dump_tensor_network,
    get_matrix,
)

__all__ = [
    "CircuitSimulator",
    "ConstructionMode",
    "DDSIMProvider",
    "DeterministicNoiseSimulator",
    "HybridCircuitSimulator",
    "HybridMode",
    "PathCircuitSimulator",
    "PathSimulatorConfiguration",
    "PathSimulatorMode",
    "StochasticNoiseSimulator",
    "UnitarySimulator",
    "__version__",
    "dump_tensor_network",
    "get_matrix",
]
