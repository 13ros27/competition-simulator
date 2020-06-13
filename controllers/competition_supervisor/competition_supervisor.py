import sys
import contextlib
from typing import Iterator
from pathlib import Path

# Webots specific library
from controller import Supervisor  # isort:skip

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

sys.path.append(str(REPO_ROOT / 'controllers/sr_controller'))

sr_controller = __import__('sr_controller')

TIME_STEP = 32
GAME_DURATION_SECONDS = 10


@contextlib.contextmanager
def record_animation(supervisor: Supervisor, file_path: Path) -> Iterator[None]:
    file_path.parent.mkdir(parents=True)
    print("Saving animation to {}".format(file_path))
    supervisor.animationStartRecording(str(file_path))
    yield
    supervisor.animationStopRecording()


def quit_if_development_mode() -> None:
    if sr_controller.get_robot_mode() != 'comp':
        print("Development mode, exiting competition supervisor")
        exit()


def prepare(supervisor: Supervisor) -> None:
    supervisor.simulationSetMode(Supervisor.SIMULATION_MODE_PAUSE)
    supervisor.simulationReset()


def remove_unused_robots(supervisor: Supervisor) -> None:
    for webots_id_str, zone_id in sr_controller.ROBOT_IDS_TO_CORNERS.items():
        if sr_controller.get_zone_robot_file_path(zone_id).exists():
            continue

        # Remove the robot
        robot = supervisor.getFromId(int(webots_id_str))
        if robot is None:
            msg = "Failed to get Webots node for zone {} (id: {})".format(
                zone_id,
                webots_id_str,
            )
            print(msg)
            raise ValueError(msg)

        robot.remove()


def run_match(supervisor: Supervisor) -> None:
    print("===========")
    print("Match start")
    print("===========")

    supervisor.simulationSetMode(Supervisor.SIMULATION_MODE_REAL_TIME)

    duration_ms = TIME_STEP * int(1000 * GAME_DURATION_SECONDS // TIME_STEP)
    supervisor.step(duration_ms)

    print("==================")
    print("Game over, pausing")
    print("==================")

    supervisor.simulationSetMode(Supervisor.SIMULATION_MODE_PAUSE)


def main() -> None:
    quit_if_development_mode()

    supervisor = Supervisor()

    prepare(supervisor)

    remove_unused_robots(supervisor)

    # TODO: where should these actually go? Do we configure an understanding of
    # the match currently running?
    with record_animation(supervisor, REPO_ROOT / 'recordings' / 'demo.html'):
        run_match(supervisor)


if __name__ == '__main__':
    main()
