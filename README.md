# FLL Robot Sensor Dashboard

Live page showing the gyro, all 4 motors (angle / speed / load), the color sensor and the battery.
Works offline (no internet needed). Needs Python 3.10+ (Windows, Mac or Linux).

## Setup (once, after forking)

**Mac / Linux**
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows (PowerShell)**
```
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

That installs the `pybricks` library too, so your editor can autocomplete and check the
hub code in `hardware/` right away (`pyrightconfig.json` tells the editor where our modules are).

## Run
(with the venv activated)
- With the robot (hub on, Pybricks firmware): `python -m work.pc.server`
  (add `--hub "Allied"` to pick a hub by Bluetooth name)
- Without a robot (simulator): `python -m work.pc.server --sim`

The browser opens at http://localhost:8000. If the hub disconnects the page says so and
reconnects by itself. **Freeze** holds the numbers so you can read them.

## Write and run a mission
1. Copy `hardware/missions/_template.py` to `hardware/missions/run1.py`.
2. Code with the simple commands from `alliedwork.py` (`drive`, `turn`, `drive_to`, `attachment`, ...). The first line is always `from alliedwork import *`.
3. Try it without the robot: `python run.py run1 --sim`
4. Run it on the robot (hub on): `python run.py run1`  (add `-n NAME` to pick a hub)

`python run.py` lists the missions. `python run.py test` drives a 24 in square.
All robot settings (ports, wheel size, PID gains) are at the top of `hardware/alliedwork.py`.

## Layout
- `hardware/` runs on the hub: `alliedwork.py` (the library), `missions/` (your runs), `sensor_stream.py` (dashboard readings).
- `run.py` uploads a mission to the hub.
- `work/` runs on the computer (`pc/` server, `dashboard/` page, `field/`, `docs/`, `tests/`).

Tests: `python -m pytest`
