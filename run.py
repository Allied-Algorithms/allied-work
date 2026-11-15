"""Run a mission on the robot (or in the simulator).

    python run.py                 list missions
    python run.py test            upload hardware/missions/test.py to the hub and run it
    python run.py test --sim      run it on the fake robot (no hub needed)
    python run.py test -n NAME    pick a hub by Bluetooth name

Press the hub's center button (or Ctrl+C here) to stop.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.abspath(__file__))
HARDWARE = os.path.join(ROOT, "hardware")
MISSIONS = os.path.join(HARDWARE, "missions")


def list_missions():
    return sorted(f[:-3] for f in os.listdir(MISSIONS) if f.endswith(".py") and not f.startswith("_"))


def run_on_hub(path, name):
    # pybricksdev bundles local imports that sit next to the script, so put
    # alliedwork.py + the mission (as main.py) in a temp folder and upload that.
    with tempfile.TemporaryDirectory() as tmp:
        shutil.copy(os.path.join(HARDWARE, "alliedwork.py"), tmp)
        shutil.copy(path, os.path.join(tmp, "main.py"))
        cmd = [sys.executable, "-u", "-m", "pybricksdev", "run", "ble"]
        if name:
            cmd += ["-n", name]
        cmd.append(os.path.join(tmp, "main.py"))
        return subprocess.call(cmd)


def run_in_sim(path):
    sys.path[:0] = [ROOT, HARDWARE]
    from work.pc.simulator import SimConfig, SimWorld
    src = open(path).read()
    m = re.search(r"set_pose\(\s*(?:x\s*=\s*)?(-?[\d.]+)\s*,\s*(?:y\s*=\s*)?(-?[\d.]+)"
                  r"(?:\s*,\s*(?:heading\s*=\s*)?(-?[\d.]+))?", src)
    x, y, h = (float(v) if v else 0.0 for v in m.groups()) if m else (12.0, 12.0, 0.0)
    world = SimWorld(SimConfig(start_x_in=x, start_y_in=y, start_heading_deg=h)).install()
    try:
        exec(compile(src, path, "exec"), {"__name__": "__main__"})
    finally:
        px, py, ph = world.pose
        print("\nSimulator finished after %.1f s. True pose: x=%.2f y=%.2f heading=%.1f"
              % (world.t_ms / 1000, px, py, ph))
        world.uninstall()
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("mission", nargs="?", help="file name in hardware/missions/, without .py")
    ap.add_argument("--sim", action="store_true", help="run on the fake robot")
    ap.add_argument("-n", "--name", help="hub Bluetooth name")
    args = ap.parse_args()
    if not args.mission:
        print("Missions:", ", ".join(list_missions()) or "(none)")
        print("Run one:  python run.py <name>   (add --sim to try without the robot)")
        return 0
    path = os.path.join(MISSIONS, args.mission + ".py")
    if not os.path.exists(path):
        print("No mission called '%s'. Available: %s" % (args.mission, ", ".join(list_missions())))
        return 1
    return run_in_sim(path) if args.sim else run_on_hub(path, args.name)


if __name__ == "__main__":
    sys.exit(main())
