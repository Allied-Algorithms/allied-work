# Sensor stream protocol

The hub program `hardware/sensor_stream.py` prints one line every 100 ms:

```
S,ms,heading,pitch,roll,yaw_rate,batt_mv,
  A_angle,A_speed,A_load, B_..., E_..., F_...,
  color,reflection,ambient,hue,sat,val
```

- 25 comma-separated fields. `-` means that device isn't plugged in.
- Heading: degrees, 0 at program start, clockwise positive (Pybricks). Pitch/roll: degrees. Yaw rate: deg/s.
- Motor angle: degrees, speed: deg/s, load: percent.
- Color: name (RED, WHITE, ... or NONE), reflection/ambient: 0-100, hue 0-359, sat/val 0-100.
- Any other line (normal `print()`, partial line) is ignored by `work/pc/protocol.py`.
