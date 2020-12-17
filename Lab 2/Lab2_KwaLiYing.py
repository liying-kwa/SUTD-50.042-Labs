#!/usr/bin/python3
# -*- coding: utf-8 -*-
# DA+Nils 2018
# Andrei + Z.TANG + Bowen, 2019
# SUTD 50.042 FCS Lab 2: Cipher Breaking
# Student: Kwa Li Ying (1003833)

"""
Lab2: Breaking Ciphers

Pwntool client for python3

Install: see install.sh

Documentation: https://python3-pwntools.readthedocs.io/en/latest/
"""


from pwn import remote

# pass two bytestrings to this function
def XOR(a, b):
    r = b''
    for x, y in zip(a, b):
        r += (x ^ y).to_bytes(1, 'big')
    return r


def sol1():
    conn.send("1")  # select challenge 1
    challenge = conn.recv()
    print("Question 1:\n")
    print(challenge)
    
    # decrypt the challenge here
    plaintext = "it was clear that there was already an understanding " + \
        "between them and that they had met by appointment. " + \
        "they were walking slowly along in deep conversation, " + \
        "and i saw her making quick little movements of her hands " + \
        "as if she were very earnest in what she was saying, " + \
        "while he listened intently, and once or twice shook his head " + \
        "in strong dissent. i stood among the rocks watching them, " + \
        "very much puzzled as to what i should do next. to follow them " + \
        "and break into their intimate conversation seemed to be an outrage, " + \
        "and yet my clear duty was never for an instant to let him " + \
        "out of my sight. to act the spy upon a friend was a hateful task. " + \
        "still, i could see no better course than to observe him from the hill, " + \
        "and to clear my conscience by confessing to him afterwards " + \
        "what i had done. it is true that if any sudden danger had threatened him " + \
        "i was too far away to be of use, and yet i am sure that you will agree " + \
        "with me that the position was very difficult, and that there was " + \
        "nothing more which i could do."
    plaintext = plaintext.upper()
    solution = str.encode(plaintext)
    
    conn.send(solution)
    message = conn.recv()
    if b'Congratulations' in message:
        print(message)


def sol2():
    conn.send("2")  # select challenge 2
    challenge = conn.recv()
    print("Question 2:\n")
    challenge = challenge.decode("UTF-8")
    print(challenge)
    challenge = bytearray.fromhex(challenge)
    
    # some all zero mask.
    # TODO: find the magic mask!
    original_plaintext_bytes = bytearray(b'Student ID 1000000 gets 0 points')
    edited_plaintext_bytes = bytearray(b'Student ID 1003833 gets 4 points')
    mask = XOR(original_plaintext_bytes, edited_plaintext_bytes)
    
    message = XOR(challenge, mask)
    conn.send(message)
    message = conn.recv()
    if b'points' in message:
        print(message)


if __name__ == "__main__":

    # NOTE: UPPERCASE names for constants is a (nice) Python convention
    URL = "35.198.199.82"
    PORT = 4455

    conn = remote(URL, PORT)
    receive1 = conn.recv()
    print(receive1.decode("UTF-8"))

    sol1()
    sol2()
    conn.close()
