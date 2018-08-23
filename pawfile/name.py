import random
import emoji

EMOJIS = list(filter(
    lambda codepoints: len(codepoints) == 1,
    emoji.EMOJI_UNICODE.values(),
))


def random_emoji() -> str:
    """Return a random emoji."""
    return random.choice(EMOJIS)


def generate_name(length: int) -> str:
    """Return a string of n random emojis."""
    emojis = [random_emoji() for _ in range(length)]
    return ''.join(emojis)
