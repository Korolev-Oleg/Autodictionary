import string
from time import sleep
import win32api
import win32con
import win32process
import win10toast
import config
from threading import Thread
from multiprocessing import Process
from multiprocessing.process import BaseProcess

from db.models import Word
from utils import StoppableThread

notifier = win10toast.ToastNotifier()


class NotifierController(win10toast.ToastNotifier):
    def _word_notify(self, title, word):
        notification_thread = Thread(
            target=self.show_toast, kwargs=dict(
                title=title,
                msg=word.translation,
                duration=4,
                threaded=True,
                # icon_path='',
            )
        )

        notification_thread.start()

    def simple_notify(self, title='', msg='', duration=1):
        Thread(
            target=self.show_toast, kwargs=dict(
                title=title,
                msg=msg,
                duration=duration,
                threaded=False)
        ).start()

    def show_notify(self, word: Word):
        title = f'{word.heading}'
        if word.requested_count == 0:
            title += f' 🆕'
        elif word.requested_count in range(1, 3):
            title += f' 🟨'
        elif word.requested_count in range(4, 6):
            title += f' 🟩 {word.requested_count}'
        elif word.requested_count > 5:
            title += f' →  🧠 {word.requested_count}'

        self._word_notify(title, word)


if __name__ == '__main__':
    word = Word()
    word.heading = 'test'
    word.translation = 'тест'
    word.requested_count = 6
    notifier = NotifierController()
    notifier.show_notify(word)
