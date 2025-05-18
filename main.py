import sys
import os
from subprocess import run, check_output
from time import localtime
import psutil

config_dir = os.path.expanduser("~/.config/pdwmbar")
config_file = os.path.join(config_dir, "widgets.conf")

DEFAULT_WIDGET_ORDER = ["time", "cpu", "memory", "battery", "volume"]
SEPARATOR = " | "


def get_volume():
    output = check_output(["amixer", "get", "Master"], shell=True).decode()
    for line in output.split("\n"):
        if "%" in line:
            volume_line = line.strip()
            break
    volume_percent = volume_line.split("[")[1].split("%")[0]
    volume_status = volume_line.split("[")[2].split("]")[0]
    return f"󰕾 {volume_percent}%" if volume_status == "on" else "󰕿 mute"


def get_time():
    now = localtime()
    return f" {now.tm_hour:02}:{now.tm_min:02}:{now.tm_sec:02}"


def cpu_load():
    return f" {psutil.cpu_percent(interval=0.2)}%"


def memory_usage():
    return f" {psutil.virtual_memory().percent}%"


def battery():
    status_battery = {100: "", 80: "", 60: "", 50: "", 40: "", 20: ""}
    battery = psutil.sensors_battery()
    for status in sorted(status_battery, reverse=True):
        if int(battery.percent) >= status:
            return (
                f"Charging {status_battery[status]} {int(battery.percent)}%"
                if battery.power_plugged
                else f"{status_battery[status]} {int(battery.percent)}%"
            )


WIDGET_HANDLERS = {
    "time": get_time,
    "cpu": cpu_load,
    "memory": memory_usage,
    "battery": battery,
    "volume": get_volume,
}


def read_config():
    try:
        with open(config_file, "r") as f:
            widgets = [line.strip() for line in f if line.strip() in WIDGET_HANDLERS]
    except FileNotFoundError:
        widgets = DEFAULT_WIDGET_ORDER.copy()
    return widgets


def write_config(widgets):
    os.makedirs(config_dir, exist_ok=True)
    with open(config_file, "w") as f:
        for widget in widgets:
            f.write(f"{widget}\n")


def metric(widget_order):
    return SEPARATOR.join(
        WIDGET_HANDLERS[widget]()
        for widget in widget_order
        if widget in WIDGET_HANDLERS
    )


def main():
    widget_order = read_config()
    last_mod_time = os.path.getmtime(config_file) if os.path.exists(config_file) else 0

    while True:
        current_mod_time = (
            os.path.getmtime(config_file) if os.path.exists(config_file) else 0
        )
        if current_mod_time > last_mod_time:
            widget_order = read_config()
            last_mod_time = current_mod_time

        run(["xsetroot", "-name", f"{metric(widget_order)}"])


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] in ("add", "del"):
        operation = sys.argv[1]
        widgets = sys.argv[2:]
        valid_widgets = WIDGET_HANDLERS.keys()
        invalid = [w for w in widgets if w not in valid_widgets]
        if invalid:
            print(f"Invalid widgets: {', '.join(invalid)}")
            sys.exit(1)
        current_widgets = read_config()
        if operation == "add":
            for w in widgets:
                if w in current_widgets:
                    current_widgets.remove(w)
                current_widgets.append(w)
        elif operation == "del":
            for w in widgets:
                while w in current_widgets:
                    current_widgets.remove(w)
        write_config(current_widgets)
        print(f"Updated widget order: {' '.join(current_widgets)}")
    else:
        main()
