# Extract the block contents from a disk image.
# Usage: python3 splitdisk.py <disk image> <block count>
# For example, python3 splitdisk.py disk.img 3 will create
# block1.fth, block2.fth, and block3.fth
# Some newlines are added, heuristically. They will get turned back into
# spaces by mkdisk.py anyway. The position of the newlines of the block
# files in the repository has been adjusted manually.

from difflib import SequenceMatcher
from itertools import zip_longest
import re
import sys

def seps(s):
    return re.findall(rb'\s+', s)

def do_split(content, old):
    old_words = old.split()
    new_words = content.split()
    differ = SequenceMatcher(None, old_words, new_words)
    old_seps = seps(old)
    output = b''
    for tag, l, r, L, R in differ.get_opcodes():
        if tag == 'equal':
            for word, sep in zip_longest(old_words[l:r], old_seps[l:r]):
                output += word + (sep or b' ')
        else:
            for word in new_words[L:R]:
                if word.startswith(b':'):
                    output += b'\n'
                else:
                    output += b' '
                output += word
    output = output.strip()
    output += b'\n'
    return output

if __name__ == "__main__":
    _, img, count = sys.argv
    count = int(count)

    with open(img, 'rb') as f:
        data = f.read()

    for i in range(1, count + 1):
        filename = 'block%d.fth' % i
        block = data[1024*i:1024*(i+1)]
        if b'\x00' in block:
            block = block[:block.index(b'\x00')]
        old_content = b''
        try:
            with open(filename, 'rb') as f:
                old_content = f.read().strip()
        except FileNotFoundError:
            pass
        block = do_split(block, old_content)
        with open(filename, 'wb') as f:
            f.write(block)
