import enum
from typing import List, Tuple, Optional, Sequence


class Device:
    def getModel(self) -> str: ...


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


class Camera(Device):
    GENERIC, INFRA_RED, SONAR, LASER = range(4)

    def enable(self, samplingPeriod: int) -> None: ...
    def disable(self) -> None: ...
    def getSamplingPeriod(self) -> int: ...

    def getType(self) -> int: ...

    def getFov(self) -> float: ...
    def getMinFov(self) -> float: ...
    def getMaxFov(self) -> float: ...
    def setFov(self, fov: float) -> None: ...

    def getFocalLength(self) -> float: ...
    def getFocalDistance(self) -> float: ...
    def getMaxFocalDistance(self) -> float: ...
    def getMinFocalDistance(self) -> float: ...
    def setFocalDistance(self, focalDistance: float) -> None: ...

    def getWidth(self) -> int: ...
    def getHeight(self) -> int: ...

    def getNear(self) -> float: ...

    def getImage(self) -> bytes: ...

    @staticmethod
    def imageGetRed(image: bytes, width: int, x: int, y: int) -> int: ...
    @staticmethod
    def imageGetGreen(image: bytes, width: int, x: int, y: int) -> int: ...
    @staticmethod
    def imageGetBlue(image: bytes, width: int, x: int, y: int) -> int: ...
    @staticmethod
    def imageGetGray(image: bytes, width: int, x: int, y: int) -> int: ...
    @staticmethod
    def pixelGetRed(pixel: int) -> int: ...
    @staticmethod
    def pixelGetGreen(pixel: int) -> int: ...
    @staticmethod
    def pixelGetBlue(pixel: int) -> int: ...
    @staticmethod
    def pixelGetGray(pixel: int) -> int: ...

    def hasRecognition(self) -> bool: ...
    def recognitionEnable(self, samplingPeriod: int) -> None: ...
    def recognitionDisable(self) -> None: ...
    def getRecognitionSamplingPeriod(self) -> int: ...
    def getRecognitionNumberOfObjects(self) -> int: ...
    def getRecognitionObjects(self) -> List[CameraRecognitionObject]: ...


class DistanceSensor(Device):
    GENERIC, INFRA_RED, SONAR, LASER = range(4)

    def enable(self, samplingPeriod: int) -> None: ...
    def disable(self) -> None: ...
    def getSamplingPeriod(self) -> int: ...
    def getValue(self) -> float: ...

    def getType(self) -> int: ...

    def getMaxValue(self) -> float: ...
    def getMinValue(self) -> float: ...
    def getAperture(self) -> float: ...


class Motor(Device):
    def setPosition(self, position: float) -> None: ...
    def setVelocity(self, velocity: float) -> None: ...
    def setAcceleration(self, acceleration: float) -> None: ...
    def setAvailableForce(self, force: float) -> None: ...
    def setAvailableTorque(self, torque: float) -> None: ...
    def setControlPID(self, p: float, i: float, d: float) -> None: ...
    def getTargetPosition(self) -> float: ...
    def getMinPosition(self) -> float: ...
    def getMaxPosition(self) -> float: ...
    def getVelocity(self) -> float: ...
    def getMaxVelocity(self) -> float: ...
    def getAcceleration(self) -> float: ...
    def getAvailableForce(self) -> float: ...
    def getMaxForce(self) -> float: ...
    def getAvailableTorque(self) -> float: ...
    def getMaxTorque(self) -> float: ...


class TouchSensor(Device):
    BUMPER, FORCE, FORCE3D = range(3)

    def enable(self, samplingPeriod: int) -> None: ...
    def disable(self) -> None: ...
    def getSamplingPeriod(self) -> int: ...
    def getValue(self) -> float: ...
    def getValues(self) -> List[float]: ...

    def getType(self) -> int: ...


class Robot:
    def __init__(self) -> None: ...
    def __del__(self) -> None: ...
    def step(self, duration: int) -> int: ...
    def getTime(self) -> float: ...
    def getBasicTimeStep(self) -> float: ...

    def getCamera(self, name: str) -> Camera: ...
    def getDistanceSensor(self, name: str) -> DistanceSensor: ...
    def getMotor(self, name: str) -> Motor: ...
    def getTouchSensor(self, name: str) -> TouchSensor: ...


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

    def animationStartRecording(self, file: str) -> bool: ...
    def animationStopRecording(self) -> bool: ...

    def simulationReset(self) -> None: ...
    def simulationGetMode(self) -> _SimulationMode: ...
    def simulationSetMode(self, mode: _SimulationMode) -> None: ...

    def worldLoad(self, file: str) -> None: ...
    def worldSave(self, file: Optional[str] = None) -> bool: ...
    def worldReload(self) -> None: ...
