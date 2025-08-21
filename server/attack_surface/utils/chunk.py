import random


def to_chunk(items, size, shuffle=False):
    # convert a list into chunks
    # If size is 0, set it to the length of items so we ignore chunking
    if size == 0:
        size = len(items)
    if shuffle is True:
        random.shuffle(list(items))
    return [items[i:i + size] for i in range(0, len(items), size)]

