import math

__all__ = ['password_entropy']


CONTROL = 0
NUMBER = 1
UPPER = 2
LOWER = 3
PUNCTUATION_1 = 4
PUNCTUATION_2 = 5
OTHER = 6
N_CLASSES = 7

CHAR_CLASSES = [0] * 128  # ASCII table
CLASS_CAPACITIES = [0] * N_CLASSES

def _initialize_char_classes():
    # Initialize the character classes table
    for i in range(128):
        if i < 32 or i == 127:
            c = CONTROL
        elif ord('0') <= i <= ord('9'):
            c = NUMBER
        elif ord('A') <= i <= ord('Z'):
            c = UPPER
        elif ord('a') <= i <= ord('z'):
            c = LOWER
        elif i == 32 or chr(i) in '!@#$%^&*()_+-=/.,':
            # Punctuation marks, which can be typed with first row of keyboard or numpad
            c = PUNCTUATION_1
        else:
            # Other punctuation marks, like []{};'"~
            c = PUNCTUATION_2
        CHAR_CLASSES[i] = c
        CLASS_CAPACITIES[c] += 1

    CLASS_CAPACITIES[OTHER] = 128  # Pretty arbitrary number
    CLASS_CAPACITIES[PUNCTUATION_2] = int(CLASS_CAPACITIES[PUNCTUATION_2] * 1.8)  # Punctuation_2 is less common


_initialize_char_classes()


def password_entropy(password: str) -> int:
    # Calculate the entropy of a password.
    s = str(password)  # we expect a string, but ensure it
    if not s:
        return 0

    eff_len = 0.0  # effective length
    used_classes = [False] * N_CLASSES
    char_counts = {}
    distances = {}
    prev_nc: int = 0  # previous character code

    for i, c in enumerate(s):
        nc = ord(c)
        if nc > 127:
            used_classes[OTHER] = True
        else:
            used_classes[CHAR_CLASSES[nc]] = True

        incr = 1.0  # value to increment effective length
        if i > 0:
            # Not the first character
            d = nc - prev_nc
            if d in distances:
                distances[d] += 1
                incr /= distances[d]
            else:
                distances[d] = 1

        if c in char_counts:
            char_counts[c] += 1
            eff_len += incr / char_counts[c]
        else:
            char_counts[c] = 1
            eff_len += incr

        prev_nc = nc

    # Capacity of the classes used
    pci = 0
    for i in range(N_CLASSES):
        if used_classes[i]:
            pci += CLASS_CAPACITIES[i]

    assert pci != 0
    bits_per_char = math.log2(pci)
    return math.floor(eff_len * bits_per_char)
