#!/usr/bin/env python3
"""
Bluetooth Rofi Widget
Manages Bluetooth devices via bluetoothctl with a Rofi interface.
"""

import subprocess
import re
import sys
import os

# Import local rofi.py from same directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rofi import Rofi

#rofi = Rofi(rofi_args=['-theme', '~/.config/rofi/left_toolbar.rasi'])
rofi = Rofi(rofi_args=[])


def run_cmd(cmd):
    """Run a shell command and return output."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()


def get_bluetooth_status():
    """Check if Bluetooth is powered on."""
    output = run_cmd("bluetoothctl show")
    return "Powered: yes" in output


def get_paired_devices():
    """Get list of paired devices as [(mac, name), ...]."""
    output = run_cmd("bluetoothctl paired-devices")
    devices = []
    for line in output.splitlines():
        match = re.match(r"Device ([0-9A-F:]+) (.+)", line)
        if match:
            devices.append((match.group(1), match.group(2)))
    return devices


def get_connected_devices():
    """Get list of currently connected device MACs."""
    output = run_cmd("bluetoothctl devices Connected")
    connected = []
    for line in output.splitlines():
        match = re.match(r"Device ([0-9A-F:]+)", line)
        if match:
            connected.append(match.group(1))
    return connected


def scan_devices():
    """Scan for available devices (blocking for a few seconds)."""
    # Start scan, wait, then get devices
    run_cmd("timeout 4 bluetoothctl scan on")
    output = run_cmd("bluetoothctl devices")
    devices = []
    for line in output.splitlines():
        match = re.match(r"Device ([0-9A-F:]+) (.+)", line)
        if match:
            devices.append((match.group(1), match.group(2)))
    return devices


def toggle_bluetooth():
    """Toggle Bluetooth power."""
    if get_bluetooth_status():
        run_cmd("bluetoothctl power off")
    else:
        run_cmd("bluetoothctl power on")


def connect_device(mac):
    """Connect to a device."""
    run_cmd(f"bluetoothctl connect {mac}")


def disconnect_device(mac):
    """Disconnect from a device."""
    run_cmd(f"bluetoothctl disconnect {mac}")


def show_device_menu(mac, name, is_connected):
    """Show submenu for a specific device."""
    if is_connected:
        options = [
            f"󰂃 Disconnect {name}",
            "← Back"
        ]
        index, key = rofi.select(f"󰂱 {name}", options)
        if key == -1 or index == 1:
            return
        if index == 0:
            disconnect_device(mac)
    else:
        options = [
            f"󰂱 Connect {name}",
            "← Back"
        ]
        index, key = rofi.select(f"󰂲 {name}", options)
        if key == -1 or index == 1:
            return
        if index == 0:
            connect_device(mac)


def main_menu():
    """Main Bluetooth menu."""
    bt_on = get_bluetooth_status()

    if bt_on:
        status_icon = "󰂯"
        toggle_text = "󰂲 Turn Bluetooth Off"
    else:
        status_icon = "󰂲"
        toggle_text = "󰂯 Turn Bluetooth On"

    options = [toggle_text]

    if bt_on:
        paired = get_paired_devices()
        connected = get_connected_devices()

        if paired:
            options.append("──────────────")  # separator
            for mac, name in paired:
                if mac in connected:
                    options.append(f"󰂱 {name} (connected)")
                else:
                    options.append(f"󰂴 {name}")

        options.append("──────────────")
        options.append("󰂰 Scan for devices")
        options.append("󰒓 Open Blueman")

    index, key = rofi.select(f"{status_icon} Bluetooth", options)

    if key == -1:
        return

    selected = options[index]

    if index == 0:
        toggle_bluetooth()
    elif "Scan for devices" in selected:
        # Scan and show results
        rofi.status("Scanning...")
        devices = scan_devices()
        paired = get_paired_devices()
        paired_macs = [mac for mac, _ in paired]

        # Filter out already paired devices
        new_devices = [(mac, name) for mac, name in devices if mac not in paired_macs]

        if new_devices:
            device_options = [f"󰂴 {name}" for _, name in new_devices]
            device_options.append("← Back")
            idx, k = rofi.select("󰂰 Found devices", device_options)
            if k != -1 and idx < len(new_devices):
                mac, name = new_devices[idx]
                run_cmd(f"bluetoothctl pair {mac}")
                connect_device(mac)
        else:
            rofi.error("No new devices found")
    elif "Open Blueman" in selected:
        subprocess.Popen(["blueman-manager"])
    elif selected.startswith("󰂱") or selected.startswith("󰂴"):
        # Device selected
        paired = get_paired_devices()
        connected = get_connected_devices()

        # Find which device was selected
        for mac, name in paired:
            if name in selected:
                is_connected = mac in connected
                show_device_menu(mac, name, is_connected)
                break


if __name__ == "__main__":
    main_menu()
