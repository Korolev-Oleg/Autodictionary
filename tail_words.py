from db.models import Word
import os
from time import sleep
from config import DB


def tail_words():
    exp_size = 0
    first_start = True

    while True:
        os.system('cls')
        print('dictionary len:', len(Word.select()))
        fetch_last_30 = Word \
            .select() \
            .order_by(Word.last_requested_date.desc()) \
            .limit(30)

        for word in fetch_last_30:
            if len(word.heading) > exp_size:
                exp_size = len(word.heading)

            heading = word.normalized_heading or word.heading
            print(word.requested_count,
                  f"{heading}".ljust(exp_size),
                  f"{word.translation}")

        if first_start:
            first_start = False
            continue

        sleep(5)


tail_words()
