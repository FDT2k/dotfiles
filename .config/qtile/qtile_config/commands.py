# commands.py - Key modifiers and command paths

import os

# Key modifiers
mod = "mod4"
alt = "mod1"
ctrl = "control"
shft = "shift"

# Current screen for toggle
curr_screen = 0


class command:
    autostart = os.path.join(os.path.dirname(__file__), '../bin/autostart')
    lock = os.path.join(os.path.dirname(__file__), '../bin/lock')
    suspend = os.path.join(os.path.dirname(__file__), '../bin/suspend')
    hibernate = os.path.join(os.path.dirname(__file__), '../bin/hibernate')
    home_screen_layout = os.path.join(os.path.dirname(
        __file__), '../bin/monitor_layout/home-layout.sh')
    work_screen_layout = os.path.join(os.path.dirname(
        __file__), '../bin/monitor_layout/vertical_layout.sh')
    samsung_screen_layout = os.path.join(os.path.dirname(
        __file__), '../bin/monitor_layout/samsung-uwide-no-edp.sh')
    samsung_screen_dual_layout = os.path.join(os.path.dirname(
        __file__), '../bin/monitor_layout/samsung-uwide-with-edp.sh')
    terminal = "terminator -b"
    volume_up = os.path.join(os.path.dirname(__file__), '../bin/raisevolume')
    volume_down = os.path.join(os.path.dirname(__file__), '../bin/lowervolume')
    volume_mute = os.path.join(os.path.dirname(__file__), '../bin/mutevolume')
    shoot = os.path.join(os.path.dirname(__file__), '../bin/shot.sh')
    record = os.path.join(os.path.dirname(__file__), '../bin/record.sh')
    browser = os.path.join(os.path.dirname(__file__),
                           '../bin/run.sh browser.d Browser')
    app_menu = os.path.join(os.path.dirname(__file__), '../bin/run.sh run.d App')
    configure = os.path.join(os.path.dirname(
        __file__), '../bin/run.sh configure.d Configure')
    run = os.path.join(os.path.dirname(__file__), '../bin/run')
    pacman = os.path.join(os.path.dirname(__file__),
                          '../bin/run.sh pacman.d Pacman')
    barrier = os.path.join(os.path.dirname(__file__),
                           '../bin/run.sh barrier.d Barrier')
    power = os.path.join(os.path.dirname(__file__), '../bin/run.sh power.d Power')
    virt = os.path.join(os.path.dirname(__file__), '../bin/run.sh osx.d Virt')
    worklayout = os.path.join(os.path.dirname(__file__), '../bin/run.sh worklayout.d WorkLayout')
    middle_screen_brightness = os.path.join(
        os.path.dirname(__file__), '../bin/brightness.sh HDMI-A-1')
    right_screen_brightness = os.path.join(
        os.path.dirname(__file__), '../bin/brightness.sh DVI-I-1')
    left_screen_brightness = os.path.join(
        os.path.dirname(__file__), '../bin/brightness.sh HDMI-A-1-0')
    sound = os.path.join(os.path.dirname(__file__),
                         '../bin/pulsaudio/sound-output.sh')
    theme = os.path.join(os.path.dirname(__file__), '../bin/theme/pick ')
    screen_layout = os.path.join(os.path.dirname(
        __file__), '../bin/run.sh screenlayout.d "Monitor Layout"'),
    copyq = os.path.join(os.path.dirname(
        __file__), '../bin/copyq.sh'),
    bluetooth = os.path.join(os.path.dirname(
        __file__), '../widgets/bluetooth_widget.py')
