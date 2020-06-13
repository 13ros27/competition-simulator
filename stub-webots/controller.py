import enum
from typing import Tuple, Optional, Sequence


class Robot:
    def __init__(self) -> None: ...
    def __del__(self) -> None: ...
    def step(self, duration: int) -> int: ...
    def getTime(self) -> float: ...


# Note: we don't actually know if webots offers up tuples or lists.

class CameraRecognitionObject:
    def get_id(self) -> int: ...
    def get_position(self) -> Tuple[float, float, float]: ...
    def get_orientation(self) -> Tuple[float, float, float, float]: ...
    def get_size(self) -> Tuple[float, float]: ...
    def get_position_on_image(self) -> Tuple[int, int]: ...
    def get_size_on_image(self) -> Tuple[int, int]: ...
    def get_number_of_colors(self) -> int: ...
    def get_colors(self) -> Sequence[float]: ...
    def get_model(self) -> bytes: ...


class _SimulationMode(enum.Enum):
    # These are probably `int` really, though as the values should be treated
    # only as opaque identifiers that doesn't matter.
    PAUSE = 'pause'
    REAL_TIME = 'real_time'
    RUN = 'run'
    FAST = 'fast'


class Supervisor(Robot):
    SIMULATION_MODE_PAUSE = _SimulationMode.PAUSE
    SIMULATION_MODE_REAL_TIME = _SimulationMode.REAL_TIME
    SIMULATION_MODE_RUN = _SimulationMode.RUN
    SIMULATION_MODE_FAST = _SimulationMode.FAST

    def getRoot(self) -> 'Supervisor': ...
    def getSelf(self) -> 'Supervisor': ...
    def getFromDef(self, name: str) -> 'Supervisor': ...
    def getFromId(self, id: int) -> 'Optional[Supervisor]': ...
    def getSelected(self) -> 'Supervisor': ...

    def remove(self) -> None: ...

    def simulationReset(self) -> None: ...
    def simulationGetMode(self) -> _SimulationMode: ...
    def simulationSetMode(self, mode: _SimulationMode) -> None: ...

    def worldLoad(self, file: str) -> None: ...
    def worldSave(self, file: Optional[str] = None) -> bool: ...
    def worldReload(self) -> None: ...
