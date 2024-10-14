# MIT License
#
# Copyright (c) 2024 Sariya Ansari
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
AESManager Module

This module provides the `AESManager` class for handling AES encryption and decryption 
operations on video files. It includes methods for generating keys, saving and loading keys, 
and encrypting or decrypting video content using AES in CBC mode.

Author: [Your Name]
"""

import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


class AESManager:
    """
    AESManager handles AES encryption and decryption for video files.

    Attributes:
        key (bytes): The AES encryption key.
        iv (bytes): The AES initialization vector.
    """
    def __init__(self, key=None, iv=None):
        """
        Initialize AESManager with an optional **key** and **iv**.
        If none are provided, they are generated.

        Args:
            **key** (bytes, optional): AES encryption key. Defaults to None.
            **iv** (bytes, optional): AES initialization vector. Defaults to None.
        """
        self.key = key if key else get_random_bytes(16)
        self.iv = iv if iv else get_random_bytes(16)

    def generate_key_iv(self):
        """
        Generate and return AES key and IV.

        Returns:
            tuple: AES key and IV.
        """
        self.key = get_random_bytes(16)
        self.iv = get_random_bytes(16)
        return self.key, self.iv

    def encrypt_video(self, input_file, output_file):
        """
        Encrypt a video file using AES encryption in CBC mode.

        Args:
            **input_file** (str): Path to the input video file.
            **output_file** (str): Path to save the encrypted video.
        """
        output_dir = os.path.dirname(output_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        with open(input_file, 'rb') as f_in:
            plaintext = f_in.read()
        ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
        with open(output_file, 'wb') as f_out:
            f_out.write(ciphertext)
        print(f"Video encrypted and saved to {output_file}")

    def decrypt_video(self, input_file, output_file):
        """
        Decrypt an AES-encrypted video file (CBC mode).

        Args:
            **input_file** (str): Path to the encrypted video file.
            **output_file** (str): Path to save the decrypted video.
        """
        output_dir = os.path.dirname(output_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        with open(input_file, 'rb') as f_in:
            ciphertext = f_in.read()
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        with open(output_file, 'wb') as f_out:
            f_out.write(plaintext)
        print(f"Video decrypted and saved to {output_file}")

    def save_key_iv(self, key_file, iv_file):
        """
        Save the AES key and IV to files for future use.

        Args:
            **key_file** (str): Path to save the AES key.
            **iv_file** (str): Path to save the AES IV.
        """
        key_dir = os.path.dirname(key_file)
        iv_dir = os.path.dirname(iv_file)

        if not os.path.exists(key_dir):
            os.makedirs(key_dir)
        if not os.path.exists(iv_dir):
            os.makedirs(iv_dir)

        with open(key_file, 'wb') as kf:
            kf.write(self.key)
        with open(iv_file, 'wb') as ivf:
            ivf.write(self.iv)
        print(f"Key saved to {key_file} and IV saved to {iv_file}")

    def load_key_iv(self, key_file, iv_file):
        """
        Load the AES key and IV from files.

        Args:
            **key_file** (str): Path to the AES key file.
            **iv_file** (str): Path to the AES IV file.
        """
        with open(key_file, 'rb') as kf:
            self.key = kf.read()
        with open(iv_file, 'rb') as ivf:
            self.iv = ivf.read()
        print(f"Key loaded from {key_file} and IV loaded from {iv_file}")
