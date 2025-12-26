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

        #try:
        proc = subprocess.run(
            ["recollq", "-a", "-b", "-n", "50", query],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=1
        )
        log.debug("Ici")
        
        temp = []
        for line in proc.stdout.splitlines():
            score = 0
            for word in query.split(' '):
                word = word.lower()
                log.debug(f'word = {word}')
                if word in line.split('/')[-1].lower():
                    # Le mot est dans le nom du fichier.
                    log.debug(f'{word} est dans le nom')
                    score += 3
                elif word in '/'.join(line.split('/')[0:-1]).lower():
                    # Le mot est dans le chemin du fichier.
                    log.debug(f'{word} est dans le chemin')
                    score += 1
            temp.append({'line': line, 'score': score})
        
        def tri(element):
            return element['score']
        
        temp.sort(key=tri, reverse=True)
        results = []
        for couple in temp:
            line = couple['line']
            log.debug(f'{couple['score']} - {line}')
            results.append(
                ExtensionResultItem(
                    icon='images/icon.png',
                    name=line.split('/')[-1],
                    description=line,
                    on_enter=OpenAction(line)
                )
            )

        return RenderResultListAction(results)

if __name__ == '__main__':
    DemoExtension().run()
