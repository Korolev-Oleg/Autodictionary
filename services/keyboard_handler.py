# TODO In better version - make class from this module without global vars
import os
from datetime import datetime

from time import sleep

import clipboard
from pynput import keyboard
from pynput.keyboard import KeyCode, Key

from db.models import Word
from .notifier import NotifierController
from .translate import get_translated_word

kctrl = keyboard.Controller()
pressed_keys = [None] * 3
hot_key = [Key.cmd, Key.alt_l, KeyCode.from_char('c')]
notifier = NotifierController()


def paste_into_chrome_translate_plugin():
    kctrl.press(Key.ctrl_l)
    kctrl.press(KeyCode.from_char('v'))
    kctrl.release(Key.ctrl_l)

    kctrl.press(Key.enter)
    kctrl.release(Key.enter)


def copy_selected_text() -> str:
    previews_buffer = clipboard.paste()
    for key in hot_key:
        kctrl.release(key)

    kctrl.press(Key.ctrl_l)
    kctrl.press(KeyCode.from_char('c'))
    kctrl.release(Key.ctrl_l)

    repeats = 6
    current_buffer = clipboard.paste()
    while current_buffer == previews_buffer and repeats >= 0:
        current_buffer = clipboard.paste()
        sleep(.05)
        repeats -= 1

    text = clipboard.paste()
    return text if text else ''


def on_press(key: KeyCode | Key | None):
    pressed_keys[0] = pressed_keys[1]
    pressed_keys[1] = pressed_keys[2]
    pressed_keys[2] = key
    if pressed_keys == hot_key:
        clip_text = copy_selected_text()
        if clip_text:
            try:
                clip_text = clip_text.split()[0]
                word = Word.get(heading=clip_text.lower())
                word.update_requested_count()
                word.last_requested_date = datetime.now()
                word.save()
                notifier.show_notify(word)
            except Word.DoesNotExist:
                translated_word = get_translated_word(clip_text)
                if translated_word:
                    notifier.show_notify(translated_word)
                    translated_word.save()
                else:
                    notifier.simple_notify(
                        msg=f'❌ No translation for {clip_text}',
                        duration=2)


def on_release(key: KeyCode | Key | None):
    ...


def join_listener():
    try:
        keyboard_kwargs = dict(on_press=on_press, on_release=on_release)
        with keyboard.Listener(**keyboard_kwargs) as listner:
            keys = ' + '.join([str(k) if isinstance(k, KeyCode) else str(k.name)
                               for k in hot_key])
            print(f"Waiting [ {keys} ] ...")
            listner.join()
    except KeyboardInterrupt:

        exit()
