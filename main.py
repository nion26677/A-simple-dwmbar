from subprocess import run, check_output
from time import localtime

import psutil

# Widget: time, cpu, memory, battery, volume
WIDGET_ORDER = ["time", "cpu", "memory", "battery", "volume"]
SEPARATOR = " | "


def get_volume():
    output = check_output(["amixer", "get", "Master"], shell=True).decode()
    for line in output.split("\n"):
        if "%" in line:
            volume_line = line.strip()
            break
    status = volume_line.split("[")[2].split("]")[0]
    volume_percent = volume_line.split("[")[1].split("%")[0]
    return f"Volume {volume_percent}" if status == "on" else "Mute"


def get_time():  # Time
    now = localtime()
    return f"Time {now.tm_hour:02}:{now.tm_min:02}:{now.tm_sec:02}"


def cpu_load():
    return f"Cpu {psutil.cpu_percent(interval=0.2)}%"


def memory_usage():
    return f"Mem {psutil.virtual_memory().percent}%"


def battery():
    battery = psutil.sensors_battery()
    return (
        f"Charging {battery.percent:0.0f}"
        if battery.power_plugged and battery.power_plugged != 100
        else f"Bat {battery.percent:0.0f}%"
    )


WIDGET_HANDLERS = {
    "time": get_time,
    "cpu": cpu_load,
    "memory": memory_usage,
    "battery": battery,
    "volume": get_volume,
}


def metric():
    return SEPARATOR.join(
        WIDGET_HANDLERS[widget]()
        for widget in WIDGET_ORDER
        if widget in WIDGET_HANDLERS
    )


while True:
    run(["xsetroot", "-name", f"{metric()}"])
