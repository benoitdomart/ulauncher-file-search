import subprocess
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.OpenAction import OpenAction

import logging


log = logging.getLogger(__name__)


class DemoExtension(Extension):

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        query = event.get_argument()
        if not query:
            return
        
        init_path = '/home/ben/Documents/Cours/'
        
        nb_dir = init_path.count('/') - 1
        
        dir_to_hide = '[^/]*/' * nb_dir
        log.debug(f'dir_to_hide = {dir_to_hide}')

        parameters = f"find {init_path} | sed 's|^/" + dir_to_hide + "||' "
        
        log.debug(f'Query = {query}')
        for parameter in query.split(' '):
            parameters += '| '
            parameters += 'grep '
            parameters += '-i '
            parameters += parameter
        
        log.debug(f'parameters = {parameters}')
        
        proc = subprocess.run(
            parameters,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=1
        )
        log.debug(f'Nb lignes = {len(proc.stdout.splitlines())}')
        
        results = []
        cpt = 0
        for line in proc.stdout.splitlines():
            if cpt == 10:
                break
            cpt += 1
            results.append(
                ExtensionResultItem(
                    icon='images/icon.png',
                    name=line.split('/')[-1],
                    description=line,
                    on_enter=OpenAction(init_path + line)
                )
            )
        return RenderResultListAction(results)

if __name__ == '__main__':
    DemoExtension().run()
