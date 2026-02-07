# workspaces.py - Workspace and room management

from libqtile.config import Group, ScratchPad, DropDown, Match
from libqtile import widget
from libqtile.log_utils import logger

from .commands import mod, shft

# List of available workspaces.
# Each workspace has its own prefix and hotkey.
workspaces = [
    ('1', 'F1'),
    ('2', 'F2'),
    ('3', 'F3'),
    ('4', 'F4'),
    ('o', 'F5'),
    ('p', 'F6'),
]

# List of available rooms.
# Rooms are identical between workspaces, but they can
# be changed to different ones as well. Minor changes required.
rooms = "asdyxc"

# Global object with information about current workspace.
wsp = {
    'current': workspaces[0][0],  # first workspace is active by default
}


def get_group_name(workspace, room):
    """ Calculate Group name based on (workspace,room) combination.
    """
    return "%s%s" % (room, workspace)


# Initialize active group for each workspace
for w, _ in workspaces:
    wsp[w] = {
        'active_group': get_group_name(w, rooms[0])  # first room is active by default
    }


def get_workspace_groups(workspace):
    """ Get list of Groups that belongs to workspace.
    """
    return [get_group_name(workspace, room) for room in rooms]


def to_workspace(workspace):
    """ Change current workspace to another one.
    """
    def f(qtile):
        global wsp

        logger.error("showing workspace %s", workspace)
        # we need to save current active room(group) somewhere
        # to return to it later
        wsp[wsp['current']]['active_group'] = qtile.current_group.name

        # now we can change current workspace to the new one
        wsp['current'] = workspace

        # dispatch the workspace's groups in order on each screen
        for idx, screen in enumerate(qtile.screens):
            logger.error("changing screen %d", idx)

            g = qtile.groups_map[
                get_group_name(workspace, rooms[idx])
            ]
            logger.error("group %s", g)

            screen.set_group(g)
            logger.error("screen widgets %s", screen.top)
            if screen.top is not None:
                for i, __widget in enumerate(screen.top.widgets):
                    logger.error("screens %s %s", type(__widget) is widget.groupbox.GroupBox, __widget)
                    if type(__widget) is widget.groupbox.GroupBox:
                        __widget.visible_groups = get_workspace_groups(workspace)
                        __widget.draw()

    return f


def to_room(room):
    """ Change active room to another within the current workspace.
    """
    def f(qtile):
        global wsp
        qtile.groups_map[get_group_name(wsp['current'], room)].toscreen(toggle=False)
    return f


def window_to_workspace(workspace, room=rooms[0]):
    """ Move active window to another workspace.
    """
    def f(qtile):
        global wsp
        qtile.current_window.togroup(wsp[workspace]['active_group'])
    return f


def window_to_room(room):
    """ Move active window to another room within the current workspace.
    """
    def f(qtile):
        global wsp
        qtile.current_window.togroup(get_group_name(wsp['current'], room))
    return f


# Create individual Group for each (workspace,room) combination we have
groups = []
for workspace, hotkey in workspaces:
    for room in rooms:
        groups.append(Group(get_group_name(workspace, room)))

# Add ScratchPad
groups.append(ScratchPad(name='scratchpad', dropdowns=[
    DropDown('terminal', 'terminator', width=0.9,
             height=0.9, x=0.05, y=0.05, opacity=0.95, match=Match(wm_class='terminator'), on_focus_lost_hide=False),
    DropDown('spotify', 'spotify', width=0.8,
             height=0.8, x=0.1, y=0.1, opacity=0.8, match=Match(wm_class='spotify'), on_focus_lost_hide=False),
    DropDown('Telegram', 'org.telegram.desktop', width=0.8,
             height=0.8, x=0.1, y=0.1, opacity=1, match=Match(wm_class='TelegramDesktop'), on_focus_lost_hide=False),
    DropDown('mixer', 'pavucontrol', width=0.4,
             height=0.6, x=0.3, y=0.1, opacity=1),
    DropDown('bitwarden', 'bitwarden-desktop',
             width=0.6, height=0.6, x=0.2, y=0.1, opacity=1, match=Match(wm_class='bitwarden-desktop'), on_focus_lost_hide=False),
    DropDown('clickup', 'clickup',
             width=0.8, height=0.8, x=0.1, y=0.1, opacity=1, match=Match(wm_class='clickup'), on_focus_lost_hide=False),
    DropDown('thunderbird', 'thunderbird',
             width=0.8, height=0.8, x=0.1, y=0.1, opacity=1, on_focus_lost_hide=False),
    DropDown('blueman', 'blueman-manager',
             width=0.4, height=0.6, x=0.3, y=0.1, opacity=1, on_focus_lost_hide=False),
    DropDown('gittyup', 'gittyup',
             width=0.8, height=0.8, x=0.1, y=0.1, opacity=1, match=Match(wm_class='gittyup'), on_focus_lost_hide=False),
    DropDown('doc', 'google-chrome-stable',
             width=0.8, height=0.8, x=0.1, y=0.1, opacity=1, match=Match(wm_class='google-chrome'), on_focus_lost_hide=False),
    DropDown('discord', 'com.discordapp.Discord',
             width=0.8, height=0.8, x=0.1, y=0.1, opacity=1, match=Match(wm_class='discord'), on_focus_lost_hide=False),
], single=True))
