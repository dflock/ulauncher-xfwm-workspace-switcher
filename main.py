from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction

import subprocess
from os import path
import re


class WorkspaceExtension(Extension):
    def __init__(self):
        # Check that wmctrl is installed
        import shutil

        # Check that we have wmctrl before continuing
        if shutil.which("wmctrl"):
            # We have wmctrl, hook up extension
            super(WorkspaceExtension, self).__init__()
            self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        else:
            # No wmctrl, so bail
            import logging

            logger = logging.getLogger(__name__)
            logger.error("Missing Dependency: wmctrl not found on $PATH")
            import sys

            sys.exit()


class KeywordQueryEventListener(EventListener):
    def __init__(self):
        self.curr_ws = [None, None]
        self.lws = "$HOME/.lws"
        self.ws_list = None

        self.get_current_ws()
        self.init_lws()
        self.get_ws_list()

    def get_current_ws(self):
        """Get current workspace ID & name: [id, name]"""

        # Get the current workspace line from wmctrl
        tmp = subprocess.run(
            ["wmctrl -d | grep -F ' * DG:'"], capture_output=True, shell=True, text=True
        ).stdout.strip()
        # Extract the workspace id
        id = tmp.split()[0]
        # Extract the workspace name
        name = ""
        m = re.search("^.*WA: (N/A|.,. \d+x\d+) *", tmp)
        if m and m.span():
            name = tmp[m.span()[1] :]

        self.curr_ws = [id, name]

    def lws_save(self):
        """Return shell command to save the current workspace

        This is done like this, so that it can be run (sort of) atomically
        in the same shell command that changes the workspace.
        """
        return 'echo -n "{}    {}" > "{}"'.format(
            self.curr_ws[0], self.curr_ws[1], self.lws
        )

    def init_lws(self):
        """If no "$HOME/.lws", then create & populate"""
        with open(path.expandvars(self.lws), "a+") as f:
            f.write("{}    {}".format(self.curr_ws[0], self.curr_ws[1]))

    def get_last_ws(self):
        """Read the last workspace into self.last_ws & return it"""
        ws = None
        with open(path.expandvars(self.lws), "r") as file:
            ws = file.read()
        return ws.split(maxsplit=1)

    def get_ws_list(self):
        """Get list of all workspaces"""
        result = subprocess.run(
            [
                "wmctrl -d | sed -n -E -e 's/^.*WA: (N\/A|.,. [[:digit:]]+x[[:digit:]]+)  //p'"
            ],
            capture_output=True,
            shell=True,
            text=True,
        ).stdout
        self.ws_list = [y for y in (x.strip() for x in result.splitlines()) if y]

    def on_event(self, event, extension):
        keyword = event.get_keyword()
        search = str(event.get_argument() or "").lower().strip()

        items = []

        self.get_current_ws()

        if search == "":
            # No search so far, just keyword.
            # Get updated list of workspaces, before user starts searching
            self.get_ws_list()

        if search.isdigit():
            # If search is a number, then shortcut to that workspace.
            action = "wmctrl -s {} && {}".format(abs(int(search) - 1), self.lws_save())
            items.append(
                ExtensionResultItem(
                    icon="images/workspace-switcher-top-left.svg",
                    name="Workspace {}".format(search),
                    description="Go to workspce {}".format(search),
                    on_enter=RunScriptAction(action),
                )
            )
        elif search == "-":
            # Shortcut to return to your previous workspace, like `cd -` does.
            lws = self.get_last_ws()
            action = 'wmctrl -s "{}" && {}'.format(lws[0], self.lws_save())
            items.append(
                ExtensionResultItem(
                    icon="images/workspace-switcher-top-left.svg",
                    name="Go back to last used workspace",
                    description="Workspace Name: {}, Workspace Id: {}".format(
                        lws[1], int(lws[0]) + 1
                    ),
                    on_enter=RunScriptAction(action),
                )
            )
        else:
            # Otherwise, match on workspace names
            for ws_idx, ws_name in enumerate(self.ws_list):
                if search == "" or search in ws_name.lower():
                    action = "wmctrl -s {} && {}".format(ws_idx, self.lws_save())
                    items.append(
                        ExtensionResultItem(
                            icon="images/workspace-switcher-top-left.svg",
                            # Workaround for https://github.com/Ulauncher/Ulauncher/issues/587
                            name=ws_name.replace("&", "&amp;") if search else ws_name,
                            description="Workspace Name: {}, Workspace Id: {}".format(
                                ws_name, int(ws_idx) + 1
                            ),
                            on_enter=RunScriptAction(action),
                        )
                    )

        return RenderResultListAction(items)


if __name__ == "__main__":
    WorkspaceExtension().run()
