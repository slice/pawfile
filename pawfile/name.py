import random
import emoji

EMOJIS = list(
    filter(
        lambda codepoints: len(codepoints) == 1,
        emoji.EMOJI_UNICODE.values()
    )
)


def random_emoji():
    return random.choice(EMOJIS)


def generate_name(length):
    emojis = [random_emoji() for _ in range(length)]
    return ''.join(emojis)
