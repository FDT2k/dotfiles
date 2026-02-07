#!/usr/bin/env python3
"""
Network Rofi Widget
Shows current network configuration via nmcli (filters Docker bridges).
"""

import subprocess
import re
import sys
import os

# Import local rofi.py from same directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rofi import Rofi

# Use sidebar theme from same directory
theme_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sidebar.rasi')
rofi = Rofi(rofi_args=['-theme', theme_path])


def run_cmd(cmd):
    """Run a shell command and return output."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()


def has_wifi_adapter():
    """Check if WiFi hardware is present."""
    output = run_cmd("nmcli -t -f TYPE dev | grep wifi")
    return bool(output)


def get_wifi_status():
    """Get WiFi status and connected SSID."""
    if not has_wifi_adapter():
        return None, None, None  # None = no adapter

    status = run_cmd("nmcli radio wifi")
    if status != "enabled":
        return False, None, None

    # Get connected WiFi
    output = run_cmd("nmcli -t -f active,ssid,signal dev wifi | grep '^yes'")
    if output:
        parts = output.split(':')
        ssid = parts[1] if len(parts) > 1 else "Unknown"
        signal = parts[2] if len(parts) > 2 else "?"
        return True, ssid, signal
    return True, None, None


def get_active_connections():
    """Get active connections (excluding Docker bridges)."""
    output = run_cmd("nmcli -t -f NAME,TYPE,DEVICE con show --active")
    connections = []

    # Patterns to exclude
    exclude_patterns = ['docker', 'br-', 'veth', 'virbr', 'lxc', 'cni', 'flannel', 'cali']

    for line in output.splitlines():
        if not line:
            continue
        parts = line.split(':')
        if len(parts) >= 3:
            name, conn_type, device = parts[0], parts[1], parts[2]

            # Skip Docker/container related interfaces
            if any(pat in name.lower() or pat in device.lower() for pat in exclude_patterns):
                continue

            connections.append({
                'name': name,
                'type': conn_type,
                'device': device
            })

    return connections


def get_device_ip(device):
    """Get IP address for a device."""
    output = run_cmd(f"ip -4 addr show {device} 2>/dev/null | grep -oP 'inet \\K[\\d.]+'")
    return output.split('\n')[0] if output else None


def get_public_ip():
    """Get public IP address."""
    try:
        return run_cmd("curl -s --max-time 2 ifconfig.me")
    except:
        return None


def get_default_gateway():
    """Get default gateway."""
    output = run_cmd("ip route | grep default | awk '{print $3}' | head -1")
    return output if output else None


def get_dns_servers():
    """Get DNS servers."""
    output = run_cmd("grep nameserver /etc/resolv.conf | awk '{print $2}' | head -3")
    return output.split('\n') if output else []


def format_connection_icon(conn_type):
    """Get icon for connection type."""
    icons = {
        '802-11-wireless': '󰤨',
        'wifi': '󰤨',
        '802-3-ethernet': '󰈀',
        'ethernet': '󰈀',
        'vpn': '󰦝',
        'wireguard': '󰦝',
        'bridge': '󰌘',
        'loopback': '󰑔',
    }
    return icons.get(conn_type, '󰛳')


def main_menu():
    """Main network info display."""
    info_lines = []

    # Header
    info_lines.append("󰛳 Network Configuration")
    info_lines.append("─────────────────────────")

    # WiFi Status (only if adapter present)
    wifi_on, ssid, signal = get_wifi_status()
    if wifi_on is not None:  # Has WiFi adapter
        if wifi_on:
            if ssid:
                info_lines.append(f"󰤨 WiFi: {ssid} ({signal}%)")
            else:
                info_lines.append("󰤭 WiFi: Not connected")
        else:
            info_lines.append("󰤮 WiFi: Disabled")
        info_lines.append("")

    # Active Connections
    connections = get_active_connections()
    if connections:
        info_lines.append("󰌘 Active Connections")
        info_lines.append("─────────────────────────")
        for conn in connections:
            icon = format_connection_icon(conn['type'])
            ip = get_device_ip(conn['device'])
            ip_str = f" ({ip})" if ip else ""
            info_lines.append(f"{icon} {conn['name']}{ip_str}")
            info_lines.append(f"   └─ {conn['device']}")

    info_lines.append("")

    # Gateway & DNS
    gateway = get_default_gateway()
    if gateway:
        info_lines.append(f"󰀂 Gateway: {gateway}")

    dns_servers = get_dns_servers()
    if dns_servers:
        info_lines.append(f"󰇖 DNS: {', '.join(dns_servers)}")

    # Public IP
    info_lines.append("")
    public_ip = get_public_ip()
    if public_ip:
        info_lines.append(f"󰩟 Public IP: {public_ip}")
    else:
        info_lines.append("󰩟 Public IP: N/A")

    info_lines.append("")
    info_lines.append("─────────────────────────")

    # Actions
    actions = []
    if wifi_on is not None:  # Has WiFi adapter
        actions.append("󰤨 Toggle WiFi")
    actions.extend([
        "󰒓 Open nmtui",
        "󰖟 Open nm-connection-editor",
        "󰑓 Refresh",
    ])

    all_options = info_lines + actions

    index, key = rofi.select("󰛳 Network", all_options)

    if key == -1:
        return

    selected = all_options[index]

    if "Toggle WiFi" in selected:
        if wifi_on:
            run_cmd("nmcli radio wifi off")
        else:
            run_cmd("nmcli radio wifi on")
        main_menu()
    elif "nmtui" in selected:
        subprocess.Popen(["terminator", "-e", "nmtui"])
    elif "nm-connection-editor" in selected:
        subprocess.Popen(["nm-connection-editor"])
    elif "Refresh" in selected:
        main_menu()


if __name__ == "__main__":
    main_menu()
