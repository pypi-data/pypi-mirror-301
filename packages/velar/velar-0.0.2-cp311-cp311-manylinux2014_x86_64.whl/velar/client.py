import binascii
import string
from typing import Optional

from .exceptions import KeyTooLong, VelarError


class Velar:
    def __init__(
        self,
        keyword: Optional[str] = None
    ):
        self.keyword = keyword
        self.letters = string.ascii_letters + string.digits

    def encrypt(self, text: str, key: Optional[str] = None):
        """encrypt

        Args:
            text (str): Text to encrypt
            key (`str`, optional): Keyword to use for encryption. Defaults to None.

        Raises:
            VelarError: key or self.keyword is None
            KeyTooLong: Key is too long

        Returns:
            str: String with encrypted text
        """
        if key is None and self.keyword is None:
            raise VelarError('Either keyword or key must be provided')

        useKey = key if key is not None else self.keyword
        lenKey = len(useKey)
        if lenKey > 35:
            raise KeyTooLong(lenKey)

        encrypted = ''
        for chars in text:
            if chars in self.letters:
                num = self.letters.find(chars)
                num += lenKey
                encrypted +=  self.letters[num]

        return self.asciiToHex(encrypted)

    def decrypt(self, text: str, key: Optional[str] = None):
        """decrypt

        Args:
            text (str): Text encrypted to original text.
            key (`str`, optional): Keyword to use for encryption. Defaults to None.

        Raises:
            VelarError: key or self.keyword is None
            KeyTooLong: Key is too long

        Returns:
            str: String with original text
        """
        if key is None and self.keyword is None:
            raise VelarError('Either keyword or key must be provided')

        useKey = key if key is not None else self.keyword
        lenKey = len(useKey)
        if lenKey > 35:
            raise KeyTooLong(lenKey)

        decrypted = ''
        text = self.hexToAscii(text)
        for chars in text:
            if chars in self.letters:
                num = self.letters.find(chars)
                num -= lenKey
                decrypted +=  self.letters[num]

        return decrypted

    def hexToAscii(self, hexString):
        hexBuffer = binascii.unhexlify(hexString)
        return hexBuffer.decode('ascii')

    def asciiToHex(self, asciiString):
        asciiBuffer = asciiString.encode('ascii')
        return binascii.hexlify(asciiBuffer).decode('utf-8')
