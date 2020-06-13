import os
import sys
import subprocess
from shutil import copyfile
from pathlib import Path

# Root directory of the SR webots simulator (equivalent to the root of the git repo)
ROOT = Path(__file__).resolve().parent.parent.parent

MODE_FILE = ROOT / "robot_mode.txt"

EXAMPLE_CONTROLLER_FILE = ROOT / "controllers/example_controller/example_controller.py"

ROBOT_IDS_TO_CORNERS = {
    "291": 0,
    "684": 1,
    "1077": 2,
    "1470": 3,
}

STRICT_ZONES = {
    "dev": (1, 2, 3),
    "comp": (0, 1, 2, 3),
}


def get_robot_zone() -> int:
    return ROBOT_IDS_TO_CORNERS[os.environ['WEBOTS_ROBOT_ID']]


def get_zone_robot_file_path(zone_id: int) -> Path:
    """
    Return the path to the robot.py for the given zone, without checking for
    existence.
    """
    return ROOT.parent / "zone-{}".format(zone_id) / "robot.py"


def get_robot_file(zone_id: int, mode: str) -> Path:
    """
    Get the path to the proper robot.py file for zone_id and mode, ensuring that
    it exists or exiting with a suitable error message.

    The logic here is that:
     - it is always an error for both a robot.py in the root and a zone-0 /
       robot.py file to exist
     - in competition mode: we check only for zone-X / robot.py files and error
       if they are missing. We assume that this controller is not run at all for
       zones which should not run.
     - in development mode:
        - zones 1-3 check only check only for zone-X / robot.py files and report
          if they are missing but exit cleanly
        - zone 0 checks for zone-0 / robot.py then a root robot.py. If neither
          are found it copies an example into place (at the root) and uses that.
    """

    robot_file = get_zone_robot_file_path(zone_id)
    fallback_robot_file = ROOT.parent / "robot.py"
    strict_zones = STRICT_ZONES[mode]

    if (
        robot_file.exists() and
        zone_id == 0 and
        fallback_robot_file.exists()
    ):
        exit(
            "Found robot controller in shared location and zone-0 location. "
            "Remove one of the controllers before running the simulation\n"
            "{}\n{}".format(robot_file, fallback_robot_file),
        )

    if zone_id in strict_zones:
        if robot_file.exists():
            return robot_file

        print("No robot controller found for zone {}".format(zone_id))

        # Only in competition mode is it an error for a robot file to be missing.
        missing_file_is_error = mode == "comp"
        exit(1 if missing_file_is_error else 0)

    # For the non-strict zones (i.e: Zone 0 in development mode) we check in the
    # fallback place. If that doesn't exist we copy an example into it.

    assert zone_id == 0 and mode == "dev", \
        "Unexpectedly handling fallback logic for zone {} in {} mode".format(
            zone_id,
            mode,
        )

    if robot_file.exists():
        return robot_file

    if fallback_robot_file.exists():
        return fallback_robot_file

    print("No robot controller found for zone {}, copying example to {}.".format(
        zone_id,
        fallback_robot_file,
    ))
    copyfile(str(EXAMPLE_CONTROLLER_FILE), str(fallback_robot_file))

    return fallback_robot_file


def get_robot_mode() -> str:
    if not MODE_FILE.exists():
        return "dev"
    return MODE_FILE.read_text().strip()


def main():
    robot_mode = get_robot_mode()
    robot_zone = get_robot_zone()
    robot_file = get_robot_file(robot_zone, robot_mode)

    print("Using {} for Zone {}".format(robot_file, robot_zone))

    env = os.environ.copy()
    # Ensure the python path is properly passed down so the `sr` module can be imported
    env['PYTHONPATH'] = os.pathsep.join(sys.path)
    env['SR_ROBOT_ZONE'] = str(robot_zone)
    env['SR_ROBOT_MODE'] = robot_mode
    env['SR_ROBOT_FILE'] = str(robot_file)

    completed_process = subprocess.run(
        [sys.executable, "-u", str(robot_file)],
        env=env,
        cwd=str(robot_file.parent),
    )

    # Exit with the same return code so webots reports it as an error
    sys.exit(completed_process.returncode)


if __name__ == "__main__":
    main()
