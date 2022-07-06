from config import LINGVO_API_KEY
from lingvo_dictionary import LingvoAPI, LangMap, NoTranslationFound
from db.models import Word

client = LingvoAPI(LINGVO_API_KEY)
client.auth()


def get_translated_word(text: str, json=False) -> Word | None:
    # TODO switch to async Yandex translate API in future
    if not Word.is_camel_case(text):
        try:
            # TODO detect dstLang before fetch
            requested_word = text.strip().split()[0]
            mini_card = client.minicard(
                text=requested_word,
                srcLang=LangMap.English,
                dstLang=LangMap.Russian) \
                .get('Translation')

            if json:
                return mini_card

            word = Word()
            word.heading = requested_word
            if mini_card.get('Heding') != requested_word:
                word.normalized_heading = mini_card.get('Heading')
            word.translation = mini_card.get('Translation')
            word.sound_name = mini_card.get('SoundName')
            return word
        except NoTranslationFound:
            print(f'no translation found for {text}')
            return None


if __name__ == '__main__':
    print(
        get_translated_word('behaviour', json=True)
    )
