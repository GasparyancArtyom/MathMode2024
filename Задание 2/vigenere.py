def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    keyword += keyword * (len(plaintext)//len(keyword)-1)
    for i in keyword:
        if len(keyword) == len(plaintext):
            break
        keyword += i

    upper_ints = {i-65: chr(i) for i in range(65, 91)}
    lover_ints = {i-97: chr(i) for i in range(97, 123)}

    for i in range(len(plaintext)):
        if plaintext[i] in upper_ints.values():
            ciphertext += upper_ints[(ord(plaintext[i]) + ord(keyword[i]) - 130) % 26]
        elif plaintext[i] in lover_ints.values():
            ciphertext += lover_ints[(ord(plaintext[i]) + ord(keyword[i]) - 194) % 26]
        else:
            ciphertext += plaintext[i]
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """

    keyword += keyword * (len(ciphertext) // len(keyword) - 1)
    for i in keyword:
        if len(keyword) == len(ciphertext):
            break
        keyword += i
    plaintext = ""

    upper_ints = {i - 65: chr(i) for i in range(65, 91)}
    lover_ints = {i - 97: chr(i) for i in range(97, 123)}

    for i in range(len(ciphertext)):
        if ciphertext[i] in upper_ints.values():
            plaintext += upper_ints[((ord(ciphertext[i])-65) - (ord(keyword[i])-65) + 26) % 26]
        elif ciphertext[i] in lover_ints.values():
            plaintext += lover_ints[((ord(ciphertext[i])-97) - (ord(keyword[i])-97) + 26) % 26]
        else:
            plaintext += ciphertext[i]
    return plaintext

