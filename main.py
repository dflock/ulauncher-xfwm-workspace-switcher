from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction

import subprocess

class XfwmWorkspaceExtension(Extension):

    def __init__(self):
        super(XfwmWorkspaceExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        keyword = event.get_keyword()
        search = str(event.get_argument() or '').lower().strip()

        items = []
        result = subprocess.run(['wmctrl -d | awk \'{$1=$2=$3=$4=$5=$6=$7=$8=$9=""; print $0}\''], capture_output=True, shell=True, text=True).stdout
        ws_list = [y for y in (x.strip() for x in result.splitlines()) if y]

        for ws_idx, ws_name in enumerate(ws_list):
            if search == '' or search in ws_name.lower():
                items.append(ExtensionResultItem(icon='images/workspace-switcher-top-left.svg',
                                                # Workaround for https://github.com/Ulauncher/Ulauncher/issues/587
                                                name=ws_name.replace('&', '&amp;') if search else ws_name,
                                                description=f'Workspace Name: {ws_name}, Workspace Id: {ws_idx}',
                                                on_enter=RunScriptAction(f'wmctrl -s {ws_idx}')))

        return RenderResultListAction(items)

if __name__ == '__main__':
    XfwmWorkspaceExtension().run()
