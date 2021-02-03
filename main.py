from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction

import subprocess
from os import path

class WorkspaceExtension(Extension):

    def __init__(self):
        super(WorkspaceExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    def __init__(self):
        self.curr_ws = [None, None]
        self.lws = '$HOME/.lws'
        self.ws_list = None

        self.get_current_ws()
        self.init_lws()
        self.get_ws_list()
    
    def get_current_ws(self):
        # Get current workspace ID & name: [id, name]
        self.curr_ws = subprocess.run(['wmctrl -d | grep -F " * DG:" | awk \'{$2=$3=$4=$5=$6=$7=$8=$9=""; print $0}\''], capture_output=True, shell=True, text=True).stdout.strip().split(maxsplit=1)
    
    def lws_save(self):
        # Return shell command to save the current workspace
        return f'echo -n "{self.curr_ws[0]}    {self.curr_ws[1]}" > "{self.lws}"'

    def init_lws(self):
        # If no "$HOME/.lws", then create & populate 
        subprocess.run([f'if [ ! -f "{self.lws}" ]; then {self.lws_save()}; fi'], shell=True)

    def get_last_ws(self):
        # Read the last workspace into self.last_ws & return it
        ws = None
        with open(path.expandvars(self.lws), 'r') as file:
            ws = file.read()
        return ws.split(maxsplit=1)

    def get_ws_list(self):
        # Get list of all workspaces
        result = subprocess.run(['wmctrl -d | awk \'{$1=$2=$3=$4=$5=$6=$7=$8=$9=""; print $0}\''], capture_output=True, shell=True, text=True).stdout
        self.ws_list = [y for y in (x.strip() for x in result.splitlines()) if y]

    def on_event(self, event, extension):
        keyword = event.get_keyword()
        search = str(event.get_argument() or '').lower().strip()

        items = []

        self.get_current_ws()

        if search.isdigit():
            # If search is a number, then shortcut to that workspace.
            action = f'wmctrl -s {abs(int(search) - 1)} && {self.lws_save()}'
            items.append(ExtensionResultItem(icon='images/workspace-switcher-top-left.svg',
                                            name=f'Workspace {search}',
                                            description=f'Go to workspce {search}',
                                            on_enter=RunScriptAction(action)))
        elif search == '-':
            # Shortcut to return to your previous workspace, like `cd -` does.
            lws = self.get_last_ws()
            action = f'wmctrl -s "{lws[0]}" && {self.lws_save()}'
            items.append(ExtensionResultItem(icon='images/workspace-switcher-top-left.svg',
                                            name=f'Go back to last used workspace',
                                            description=f'Workspace Name: {lws[1]}, Workspace Id: {int(lws[0]) + 1}',
                                            on_enter=RunScriptAction(action)))
        else:
            # Otherwise, match on workspace names
            for ws_idx, ws_name in enumerate(self.ws_list):
                if search == '' or search in ws_name.lower():
                    action = f'wmctrl -s {ws_idx} && {self.lws_save()}'
                    items.append(ExtensionResultItem(icon='images/workspace-switcher-top-left.svg',
                                                    # Workaround for https://github.com/Ulauncher/Ulauncher/issues/587
                                                    name=ws_name.replace('&', '&amp;') if search else ws_name,
                                                    description=f'Workspace Name: {ws_name}, Workspace Id: {int(ws_idx) + 1}',
                                                    on_enter=RunScriptAction(action)))

        return RenderResultListAction(items)

if __name__ == '__main__':
    WorkspaceExtension().run()
