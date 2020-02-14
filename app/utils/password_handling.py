# coding: utf-8
import random


def generate_salt(length=32):
    chars = []
    for i in range(length):
        chars.append(random.choice(ALPHABET))
