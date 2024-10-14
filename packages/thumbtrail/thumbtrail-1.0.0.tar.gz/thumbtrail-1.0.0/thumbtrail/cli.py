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

# """
# CLI Module for ThumbTrail
#
# This module provides command-line functionality for encrypting, decrypting,
# and converting video files, as well as generating WebVTT and thumbnail files
# for video streams. The functionality is designed to be accessed through the
# command-line interface (CLI) and is not part of the public API.
#
# Classes and Functions:
# - _aes_encrypt: Encrypts a video using AES encryption.
# - _aes_decrypt: Decrypts an AES-encrypted video.
# - _aes_generate_keys: Generates AES key and IV and saves them to files.
# - _hls_convert: Converts a video to HLS format.
# - _hls_encrypt_convert: Converts and encrypts a video to HLS format.
# - _hls_encrypt_existing: Encrypts an existing HLS playlist.
# - _hls_decrypt: Decrypts an AES-encrypted HLS playlist.
# - _webvtt_generate_clear: Generates WebVTT and thumbnails for a clear video stream.
# - _webvtt_generate_aes: Generates WebVTT and thumbnails for an AES-encrypted video.
# - _webvtt_generate_hls: Generates WebVTT and thumbnails for an HLS-encrypted video.
#
# Note: These functions are intended to be used with the command-line interface only.
# """
#
# import argparse
# from thumbtrail.cryptomanager import CryptoManager
# from thumbtrail.scrubber import Scrubber
#
# def aes_encrypt(args):
#     """
#     AES encryption of a video file.
#
#     This function encrypts the input video using AES encryption with the specified key and IV files.
#
#     Args:
#         args: The command-line arguments containing:
#             - `input_video`: Path to the input video file.
#             - `encrypted_output`: Path to save the encrypted video.
#             - `key_file`: Path to the AES key file.
#             - `iv_file`: Path to the AES IV file.
#     """
#     crypto_manager = CryptoManager()
#     crypto_manager.load_aes_key_iv(args.key_file, args.iv_file)
#     crypto_manager.encrypt_video_aes(args.input_video, args.encrypted_output)
#     print(f"AES Encrypted video saved at: {args.encrypted_output}")
#
#
# def aes_decrypt(args):
#     """
#     AES decryption of a video file.
#
#     This function decrypts the encrypted video using AES with the provided key and IV.
#
#     Args:
#         args: The command-line arguments containing:
#             - `encrypted_input`: Path to the encrypted video file.
#             - `decrypted_output`: Path to save the decrypted video.
#             - `key_file`: Path to the AES key file.
#             - `iv_file`: Path to the AES IV file.
#     """
#     crypto_manager = CryptoManager()
#     crypto_manager.load_aes_key_iv(args.key_file, args.iv_file)
#     crypto_manager.decrypt_video_aes(args.encrypted_input, args.decrypted_output)
#     print(f"AES Decrypted video saved at: {args.decrypted_output}")
#
#
# def aes_generate_keys(args):
#     """
#     Generate AES key and IV and save them to files.
#
#     This function generates a new AES key and initialization vector (IV) and saves them
#     to the specified files.
#
#     Args:
#         args: The command-line arguments containing:
#             - `key_file`: Path to save the AES key.
#             - `iv_file`: Path to save the AES IV.
#     """
#     crypto_manager = CryptoManager()
#     crypto_manager.generate_aes_key_iv()
#     crypto_manager.save_aes_key_iv(args.key_file, args.iv_file)
#     print(f"AES Key and IV saved at: {args.key_file} and {args.iv_file}")
#
#
# def hls_convert(args):
#     """
#     Convert video to HLS format.
#
#     This function converts the input video to HLS format and saves it to the specified directory.
#
#     Args:
#         args: The command-line arguments containing:
#             - `input_video`: Path to the input video file.
#             - `output_dir`: Directory where the HLS files will be saved.
#     """
#     crypto_manager = CryptoManager()
#     crypto_manager.convert_video_to_hls(args.input_video, args.output_dir)
#     print(f"Video converted to HLS at: {args.output_dir}")
#
#
# def hls_encrypt_convert(args):
#     """
#     Convert and encrypt video to HLS format.
#
#     This function converts the input video to HLS format and applies AES encryption to the HLS stream.
#
#     Args:
#         args: The command-line arguments containing:
#             - `input_video`: Path to the input video file.
#             - `output_dir`: Directory where the encrypted HLS files will be saved.
#     """
#     crypto_manager = CryptoManager()
#     key_file, key_info_file, iv_hex = crypto_manager.generate_hls_key_info(args.output_dir)
#     crypto_manager.convert_video_to_hls(args.input_video, args.output_dir, key_info_file)
#     print(f"Video converted and encrypted to HLS at: {args.output_dir}")
#
#
# def hls_encrypt_existing(args):
#     """
#     Encrypt an existing HLS playlist.
#
#     This function applies AES encryption to an existing HLS playlist.
#
#     Args:
#         args: The command-line arguments containing:
#             - `playlist_file`: Path to the HLS playlist file.
#             - `output_dir`: Directory where the encrypted HLS files will be saved.
#     """
#     crypto_manager = CryptoManager()
#     crypto_manager.encrypt_existing_hls(args.playlist_file, args.output_dir)
#     print(f"Existing HLS stream encrypted at: {args.output_dir}")
#
#
# def hls_decrypt(args):
#     """
#     Decrypt an encrypted HLS playlist.
#
#     This function decrypts an AES-encrypted HLS playlist and saves the decrypted video.
#
#     Args:
#         args: The command-line arguments containing:
#             - `playlist_file`: Path to the encrypted HLS playlist file.
#             - `decrypted_output`: Path to save the decrypted video.
#             - `key_file`: Path to the decryption key file.
#             - `iv_file`: Path to the IV file (optional).
#     """
#     crypto_manager = CryptoManager()
#     crypto_manager.decrypt_hls_video(args.playlist_file, args.decrypted_output, args.key_file, args.iv_file)
#     print(f"Decrypted HLS video saved at: {args.decrypted_output}")
#
#
# def webvtt_generate_clear(args):
#     """
#     Generate WebVTT and thumbnails for a clear video stream.
#
#     This function generates WebVTT and thumbnails for a clear (non-encrypted) video stream.
#
#     Args:
#         args: The command-line arguments containing:
#             - `video_path`: Path to the input video file.
#             - `output_dir`: Directory to save WebVTT and thumbnails.
#             - `interval`: Time interval between thumbnails in seconds.
#             - `thumbnail_width`: Width of the thumbnails.
#             - `thumbnail_height`: Height of the thumbnails.
#             - `image_format`: Image format for the thumbnails.
#             - `should_merge_thumbnails`: Whether to merge all thumbnails into one image.
#             - `use_absolute_paths`: Whether to use absolute paths in the WebVTT file.
#             - `thumbnail_url`: Optional URL base for the thumbnail paths in the WebVTT file.
#     """
#     scrubber = Scrubber(args.video_path, args.output_dir)
#     scrubber.generate_thumbnails_and_webvtt(
#         interval=args.interval,
#         thumbnail_size=(args.thumbnail_width, args.thumbnail_height),
#         image_format=args.image_format,
#         should_merge_thumbnails=args.should_merge_thumbnails,
#         use_absolute_paths=args.use_absolute_paths,
#         thumbnail_url=args.thumbnail_url
#     )
#     print("WebVTT and thumbnails for clear video stream generated successfully.")
#
#
# def webvtt_generate_aes(args):
#     """
#     Generate WebVTT and thumbnails for an AES-encrypted video stream.
#
#     This function generates WebVTT and thumbnails for an AES-encrypted video stream.
#
#     Args:
#         args: The command-line arguments containing:
#             - `video_path`: Path to the AES-encrypted video file.
#             - `output_dir`: Directory to save WebVTT and thumbnails.
#             - `key_file`: Path to the AES key file.
#             - `iv_file`: Path to the AES IV file.
#             - `interval`: Time interval between thumbnails in seconds.
#             - `thumbnail_width`: Width of the thumbnails.
#             - `thumbnail_height`: Height of the thumbnails.
#             - `image_format`: Image format for the thumbnails.
#             - `should_merge_thumbnails`: Whether to merge all thumbnails into one image.
#             - `use_absolute_paths`: Whether to use absolute paths in the WebVTT file.
#     """
#     scrubber = Scrubber(
#         args.video_path, args.output_dir,
#         decryption_method='AES',
#         key_file=args.key_file,
#         iv_file=args.iv_file
#     )
#     scrubber.generate_thumbnails_and_webvtt(
#         interval=args.interval,
#         thumbnail_size=(args.thumbnail_width, args.thumbnail_height),
#         image_format=args.image_format,
#         should_merge_thumbnails=args.should_merge_thumbnails,
#         use_absolute_paths=args.use_absolute_paths
#     )
#     print("WebVTT and thumbnails for AES-encrypted stream generated successfully.")
#
#
# def webvtt_generate_hls(args):
#     """
#     Generate WebVTT and thumbnails for an HLS-encrypted video stream.
#
#     This function generates WebVTT and thumbnails for an HLS-encrypted video stream.
#
#     Args:
#         args: The command-line arguments containing:
#             - `video_path`: Path to the HLS playlist file.
#             - `output_dir`: Directory to save WebVTT and thumbnails.
#             - `key_file`: Path to the AES key file for decryption.
#             - `interval`: Time interval between thumbnails in seconds.
#             - `thumbnail_width`: Width of the thumbnails.
#             - `thumbnail_height`: Height of the thumbnails.
#             - `image_format`: Image format for the thumbnails.
#             - `should_merge_thumbnails`: Whether to merge all thumbnails into one image.
#             - `use_absolute_paths`: Whether to use absolute paths in the WebVTT file.
#             - `thumbnail_url`: Optional URL base for the thumbnail paths in the WebVTT file.
#     """
#     scrubber = Scrubber(
#         args.video_path, args.output_dir,
#         decryption_method='HLS',
#         key_file=args.key_file
#     )
#     scrubber.generate_thumbnails_and_webvtt(
#         interval=args.interval,
#         thumbnail_size=(args.thumbnail_width, args.thumbnail_height),
#         image_format=args.image_format,
#         should_merge_thumbnails=args.should_merge_thumbnails,
#         use_absolute_paths=args.use_absolute_paths,
#         thumbnail_url=args.thumbnail_url
#     )
#     print("WebVTT and thumbnails for HLS-encrypted stream generated successfully.")
#
# def cli_main():
#     # Create the top-level parser
#     parser = argparse.ArgumentParser(
#         description="ThumbTrail CLI: Encryption, decryption, and video conversion tools"
#     )
#     subparsers = parser.add_subparsers(help="Commands")
#
#     # AES encryption command
#     parser_aes_encrypt = subparsers.add_parser(
#         "aes-encrypt", help="Encrypt a video using AES encryption algorithm"
#     )
#     parser_aes_encrypt.add_argument("input_video", help="Path to the input video file")
#     parser_aes_encrypt.add_argument("encrypted_output", help="Path to save the encrypted video file")
#     parser_aes_encrypt.add_argument("key_file", help="Path to the AES key file")
#     parser_aes_encrypt.add_argument("iv_file", help="Path to the AES IV file")
#     parser_aes_encrypt.set_defaults(func=aes_encrypt)
#
#     # AES decryption command
#     parser_aes_decrypt = subparsers.add_parser(
#         "aes-decrypt", help="Decrypt an AES-encrypted video content"
#     )
#     parser_aes_decrypt.add_argument("encrypted_input", help="Path to the encrypted video file")
#     parser_aes_decrypt.add_argument("decrypted_output", help="Path to save the decrypted video file")
#     parser_aes_decrypt.add_argument("key_file", help="Path to the AES key file")
#     parser_aes_decrypt.add_argument("iv_file", help="Path to the AES IV file")
#     parser_aes_decrypt.set_defaults(func=aes_decrypt)
#
#     # AES key generation command
#     parser_aes_generate = subparsers.add_parser(
#         "aes-generate-keys", help="Generate AES key and IV and save them to files"
#     )
#     parser_aes_generate.add_argument("key_file", help="Path to save the AES key file")
#     parser_aes_generate.add_argument("iv_file", help="Path to save the AES IV file")
#     parser_aes_generate.set_defaults(func=aes_generate_keys)
#
#     # HLS conversion command
#     parser_hls_convert = subparsers.add_parser(
#         "hls-convert", help="Convert a video to HLS format"
#     )
#     parser_hls_convert.add_argument("input_video", help="Path to the input video file")
#     parser_hls_convert.add_argument("output_dir", help="Directory to save the HLS output")
#     parser_hls_convert.set_defaults(func=hls_convert)
#
#     # HLS conversion with encryption command
#     parser_hls_encrypt_convert = subparsers.add_parser(
#         "hls-encrypt-convert", help="Convert and encrypt a video to HLS format"
#     )
#     parser_hls_encrypt_convert.add_argument("input_video", help="Path to the input video file")
#     parser_hls_encrypt_convert.add_argument("output_dir", help="Directory to save the encrypted HLS output")
#     parser_hls_encrypt_convert.set_defaults(func=hls_encrypt_convert)
#
#     # Encrypt existing HLS command
#     parser_hls_encrypt_existing = subparsers.add_parser(
#         "hls-encrypt-existing", help="Encrypt an existing HLS playlist"
#     )
#     parser_hls_encrypt_existing.add_argument("playlist_file", help="Path to the HLS playlist file")
#     parser_hls_encrypt_existing.add_argument("output_dir", help="Directory to save the encrypted HLS output")
#     parser_hls_encrypt_existing.set_defaults(func=hls_encrypt_existing)
#
#     # HLS decryption command
#     parser_hls_decrypt = subparsers.add_parser(
#         "hls-decrypt", help="Decrypt an HLS-encrypted video"
#     )
#     parser_hls_decrypt.add_argument("playlist_file", help="Path to the encrypted HLS playlist")
#     parser_hls_decrypt.add_argument("decrypted_output", help="Path to save the decrypted video file")
#     parser_hls_decrypt.add_argument("key_file", help="Path to the decryption key file")
#     parser_hls_decrypt.add_argument("iv_file", help="Path to the IV file (optional)", nargs='?', default=None)
#     parser_hls_decrypt.set_defaults(func=hls_decrypt)
#
#     # WebVTT generation for clear stream
#     webvtt_clear_parser = subparsers.add_parser("webvtt-clear",
#                                                 help="Generate WebVTT and thumbnails for a clear video stream.")
#     webvtt_clear_parser.add_argument("video_path", help="Input video file.")
#     webvtt_clear_parser.add_argument("output_dir", help="Directory to save WebVTT and thumbnails.")
#     webvtt_clear_parser.add_argument("--interval", type=int, default=5,
#                                      help="Time interval between thumbnails in seconds.")
#     webvtt_clear_parser.add_argument("--thumbnail-width", type=int, default=160, help="Thumbnail width.")
#     webvtt_clear_parser.add_argument("--thumbnail-height", type=int, default=90, help="Thumbnail height.")
#     webvtt_clear_parser.add_argument("--image-format", default="jpg",
#                                      help="Image format for thumbnails (e.g., jpg, png).")
#     webvtt_clear_parser.add_argument("--should-merge-thumbnails", action="store_true",
#                                      help="Merge thumbnails into a single image.")
#     webvtt_clear_parser.add_argument("--use-absolute-paths", action="store_true",
#                                      help="Use absolute paths in WebVTT file.")
#     webvtt_clear_parser.add_argument("--thumbnail-url", help="Base URL for thumbnail paths in WebVTT.")
#     webvtt_clear_parser.set_defaults(func=webvtt_generate_clear)
#
#     # WebVTT generation for AES-encrypted stream
#     webvtt_aes_parser = subparsers.add_parser("webvtt-aes",
#                                               help="Generate WebVTT and thumbnails for an AES-encrypted video stream.")
#     webvtt_aes_parser.add_argument("video_path", help="Input encrypted video file.")
#     webvtt_aes_parser.add_argument("output_dir", help="Directory to save WebVTT and thumbnails.")
#     webvtt_aes_parser.add_argument("key_file", help="AES key file.")
#     webvtt_aes_parser.add_argument("iv_file", help="AES IV file.")
#     webvtt_aes_parser.add_argument("--interval", type=int, default=5,
#                                    help="Time interval between thumbnails in seconds.")
#     webvtt_aes_parser.add_argument("--thumbnail-width", type=int, default=160, help="Thumbnail width.")
#     webvtt_aes_parser.add_argument("--thumbnail-height", type=int, default=90, help="Thumbnail height.")
#     webvtt_aes_parser.add_argument("--image-format", default="jpg",
#                                    help="Image format for thumbnails (e.g., jpg, png).")
#     webvtt_aes_parser.add_argument("--should-merge-thumbnails", action="store_true",
#                                    help="Merge thumbnails into a single image.")
#     webvtt_aes_parser.add_argument("--use-absolute-paths", action="store_true",
#                                    help="Use absolute paths in WebVTT file.")
#     webvtt_aes_parser.set_defaults(func=webvtt_generate_aes)
#
#     # WebVTT generation for HLS-encrypted stream
#     webvtt_hls_parser = subparsers.add_parser("webvtt-hls",
#                                               help="Generate WebVTT and thumbnails for an HLS-encrypted video stream.")
#     webvtt_hls_parser.add_argument("video_path", help="Input HLS playlist file.")
#     webvtt_hls_parser.add_argument("output_dir", help="Directory to save WebVTT and thumbnails.")
#     webvtt_hls_parser.add_argument("key_file", help="AES key file for HLS decryption.")
#     webvtt_hls_parser.add_argument("--interval", type=int, default=5,
#                                    help="Time interval between thumbnails in seconds.")
#     webvtt_hls_parser.add_argument("--thumbnail-width", type=int, default=160, help="Thumbnail width.")
#     webvtt_hls_parser.add_argument("--thumbnail-height", type=int, default=90, help="Thumbnail height.")
#     webvtt_hls_parser.add_argument("--image-format", default="jpg",
#                                    help="Image format for thumbnails (e.g., jpg, png).")
#     webvtt_hls_parser.add_argument("--should-merge-thumbnails", action="store_true",
#                                    help="Merge thumbnails into a single image.")
#     webvtt_hls_parser.add_argument("--use-absolute-paths", action="store_true",
#                                    help="Use absolute paths in WebVTT file.")
#     webvtt_hls_parser.add_argument("--thumbnail-url", help="Base URL for thumbnail paths in WebVTT.")
#     webvtt_hls_parser.set_defaults(func=webvtt_generate_hls)
#
#     # Parse the arguments and call the appropriate function
#     args = parser.parse_args()
#     if hasattr(args, 'func'):
#         args.func(args)
#     else:
#         parser.print_help()
#
#
# if __name__ == "__main__":
#     cli_main()

"""
CLI Module for ThumbTrail

This module provides command-line functionality for encrypting, decrypting,
and converting video files, as well as generating WebVTT and thumbnail files
for video streams. The functionality is designed to be accessed through the
command-line interface (CLI) and is not part of the public API.

Classes and Functions:
- _aes_encrypt: Encrypts a video using AES encryption.
- _aes_decrypt: Decrypts an AES-encrypted video.
- _aes_generate_keys: Generates AES key and IV and saves them to files.
- _hls_convert: Converts a video to HLS format.
- _hls_encrypt_convert: Converts and encrypts a video to HLS format.
- _hls_encrypt_existing: Encrypts an existing HLS playlist.
- _hls_decrypt: Decrypts an AES-encrypted HLS playlist.
- _webvtt_generate_clear: Generates WebVTT and thumbnails for a clear video stream.
- _webvtt_generate_aes: Generates WebVTT and thumbnails for an AES-encrypted video.
- _webvtt_generate_hls: Generates WebVTT and thumbnails for an HLS-encrypted video.

Note: These functions are intended to be used with the command-line interface only.
"""

import argparse
from thumbtrail.cryptomanager import CryptoManager
from thumbtrail.scrubber import Scrubber


def _aes_encrypt(args):
    """
    AES encryption of a video file.

    This function encrypts the input video using AES encryption with the specified key and IV files.

    Args:
        args: The command-line arguments containing:
            - `input_video`: Path to the input video file.
            - `encrypted_output`: Path to save the encrypted video.
            - `key_file`: Path to the AES key file.
            - `iv_file`: Path to the AES IV file.
    """
    crypto_manager = CryptoManager()
    crypto_manager.load_aes_key_iv(args.key_file, args.iv_file)
    crypto_manager.encrypt_video_aes(args.input_video, args.encrypted_output)
    print(f"AES Encrypted video saved at: {args.encrypted_output}")


def _aes_decrypt(args):
    """
    AES decryption of a video file.

    This function decrypts the encrypted video using AES with the provided key and IV.

    Args:
        args: The command-line arguments containing:
            - `encrypted_input`: Path to the encrypted video file.
            - `decrypted_output`: Path to save the decrypted video.
            - `key_file`: Path to the AES key file.
            - `iv_file`: Path to the AES IV file.
    """
    crypto_manager = CryptoManager()
    crypto_manager.load_aes_key_iv(args.key_file, args.iv_file)
    crypto_manager.decrypt_video_aes(args.encrypted_input, args.decrypted_output)
    print(f"AES Decrypted video saved at: {args.decrypted_output}")


def _aes_generate_keys(args):
    """
    Generate AES key and IV and save them to files.

    This function generates a new AES key and initialization vector (IV) and saves them
    to the specified files.

    Args:
        args: The command-line arguments containing:
            - `key_file`: Path to save the AES key.
            - `iv_file`: Path to save the AES IV.
    """
    crypto_manager = CryptoManager()
    crypto_manager.generate_aes_key_iv()
    crypto_manager.save_aes_key_iv(args.key_file, args.iv_file)
    print(f"AES Key and IV saved at: {args.key_file} and {args.iv_file}")


def _hls_convert(args):
    """
    Convert video to HLS format.

    This function converts the input video to HLS format and saves it to the specified directory.

    Args:
        args: The command-line arguments containing:
            - `input_video`: Path to the input video file.
            - `output_dir`: Directory where the HLS files will be saved.
    """
    crypto_manager = CryptoManager()
    crypto_manager.convert_video_to_hls(args.input_video, args.output_dir)
    print(f"Video converted to HLS at: {args.output_dir}")


def _hls_encrypt_convert(args):
    """
    Convert and encrypt video to HLS format.

    This function converts the input video to HLS format and applies AES encryption to the HLS stream.

    Args:
        args: The command-line arguments containing:
            - `input_video`: Path to the input video file.
            - `output_dir`: Directory where the encrypted HLS files will be saved.
    """
    crypto_manager = CryptoManager()
    key_file, key_info_file, iv_hex = crypto_manager.generate_hls_key_info(args.output_dir)
    crypto_manager.convert_video_to_hls(args.input_video, args.output_dir, key_info_file)
    print(f"Video converted and encrypted to HLS at: {args.output_dir}")


def _hls_encrypt_existing(args):
    """
    Encrypt an existing HLS playlist.

    This function applies AES encryption to an existing HLS playlist.

    Args:
        args: The command-line arguments containing:
            - `playlist_file`: Path to the HLS playlist file.
            - `output_dir`: Directory where the encrypted HLS files will be saved.
    """
    crypto_manager = CryptoManager()
    crypto_manager.encrypt_existing_hls(args.playlist_file, args.output_dir)
    print(f"Existing HLS stream encrypted at: {args.output_dir}")


def _hls_decrypt(args):
    """
    Decrypt an encrypted HLS playlist.

    This function decrypts an AES-encrypted HLS playlist and saves the decrypted video.

    Args:
        args: The command-line arguments containing:
            - `playlist_file`: Path to the encrypted HLS playlist file.
            - `decrypted_output`: Path to save the decrypted video.
            - `key_file`: Path to the decryption key file.
            - `iv_file`: Path to the IV file (optional).
    """
    crypto_manager = CryptoManager()
    crypto_manager.decrypt_hls_video(args.playlist_file, args.decrypted_output, args.key_file, args.iv_file)
    print(f"Decrypted HLS video saved at: {args.decrypted_output}")


def _webvtt_generate_clear(args):
    """
    Generate WebVTT and thumbnails for a clear video stream.

    This function generates WebVTT and thumbnails for a clear (non-encrypted) video stream.

    Args:
        args: The command-line arguments containing:
            - `video_path`: Path to the input video file.
            - `output_dir`: Directory to save WebVTT and thumbnails.
            - `interval`: Time interval between thumbnails in seconds.
            - `thumbnail_width`: Width of the thumbnails.
            - `thumbnail_height`: Height of the thumbnails.
            - `image_format`: Image format for the thumbnails.
            - `should_merge_thumbnails`: Whether to merge all thumbnails into one image.
            - `use_absolute_paths`: Whether to use absolute paths in the WebVTT file.
            - `thumbnail_url`: Optional URL base for the thumbnail paths in the WebVTT file.
    """
    scrubber = Scrubber(args.video_path, args.output_dir)
    scrubber.generate_thumbnails_and_webvtt(
        interval=args.interval,
        thumbnail_size=(args.thumbnail_width, args.thumbnail_height),
        image_format=args.image_format,
        should_merge_thumbnails=args.should_merge_thumbnails,
        use_absolute_paths=args.use_absolute_paths,
        thumbnail_url=args.thumbnail_url
    )
    print("WebVTT and thumbnails for clear video stream generated successfully.")


def _webvtt_generate_aes(args):
    """
    Generate WebVTT and thumbnails for an AES-encrypted video stream.

    This function generates WebVTT and thumbnails for an AES-encrypted video stream.

    Args:
        args: The command-line arguments containing:
            - `video_path`: Path to the AES-encrypted video file.
            - `output_dir`: Directory to save WebVTT and thumbnails.
            - `key_file`: Path to the AES key file.
            - `iv_file`: Path to the AES IV file.
            - `interval`: Time interval between thumbnails in seconds.
            - `thumbnail_width`: Width of the thumbnails.
            - `thumbnail_height`: Height of the thumbnails.
            - `image_format`: Image format for the thumbnails.
            - `should_merge_thumbnails`: Whether to merge all thumbnails into one image.
            - `use_absolute_paths`: Whether to use absolute paths in the WebVTT file.
    """
    scrubber = Scrubber(
        args.video_path, args.output_dir,
        decryption_method='AES',
        key_file=args.key_file,
        iv_file=args.iv_file
    )
    scrubber.generate_thumbnails_and_webvtt(
        interval=args.interval,
        thumbnail_size=(args.thumbnail_width, args.thumbnail_height),
        image_format=args.image_format,
        should_merge_thumbnails=args.should_merge_thumbnails,
        use_absolute_paths=args.use_absolute_paths
    )
    print("WebVTT and thumbnails for AES-encrypted stream generated successfully.")


def _webvtt_generate_hls(args):
    """
    Generate WebVTT and thumbnails for an HLS-encrypted video stream.

    This function generates WebVTT and thumbnails for an HLS-encrypted video stream.

    Args:
        args: The command-line arguments containing:
            - `video_path`: Path to the HLS playlist file.
            - `output_dir`: Directory to save WebVTT and thumbnails.
            - `key_file`: Path to the AES key file for decryption.
            - `interval`: Time interval between thumbnails in seconds.
            - `thumbnail_width`: Width of the thumbnails.
            - `thumbnail_height`: Height of the thumbnails.
            - `image_format`: Image format for the thumbnails.
            - `should_merge_thumbnails`: Whether to merge all thumbnails into one image.
            - `use_absolute_paths`: Whether to use absolute paths in the WebVTT file.
            - `thumbnail_url`: Optional URL base for the thumbnail paths in the WebVTT file.
    """
    scrubber = Scrubber(
        args.video_path, args.output_dir,
        decryption_method='HLS',
        key_file=args.key_file
    )
    scrubber.generate_thumbnails_and_webvtt(
        interval=args.interval,
        thumbnail_size=(args.thumbnail_width, args.thumbnail_height),
        image_format=args.image_format,
        should_merge_thumbnails=args.should_merge_thumbnails,
        use_absolute_paths=args.use_absolute_paths,
        thumbnail_url=args.thumbnail_url
    )
    print("WebVTT and thumbnails for HLS-encrypted stream generated successfully.")


def main():
    # Create the top-level parser
    parser = argparse.ArgumentParser(
        description="ThumbTrail CLI: Encryption, decryption, and video conversion tools"
    )
    subparsers = parser.add_subparsers(help="Commands")

    # AES encryption command
    parser_aes_encrypt = subparsers.add_parser(
        "aes-encrypt", help="Encrypt a video using AES encryption algorithm"
    )
    parser_aes_encrypt.add_argument("input_video", help="Path to the input video file")
    parser_aes_encrypt.add_argument("encrypted_output", help="Path to save the encrypted video file")
    parser_aes_encrypt.add_argument("key_file", help="Path to the AES key file")
    parser_aes_encrypt.add_argument("iv_file", help="Path to the AES IV file")
    parser_aes_encrypt.set_defaults(func=_aes_encrypt)

    # AES decryption command
    parser_aes_decrypt = subparsers.add_parser(
        "aes-decrypt", help="Decrypt an AES-encrypted video content"
    )
    parser_aes_decrypt.add_argument("encrypted_input", help="Path to the encrypted video file")
    parser_aes_decrypt.add_argument("decrypted_output", help="Path to save the decrypted video file")
    parser_aes_decrypt.add_argument("key_file", help="Path to the AES key file")
    parser_aes_decrypt.add_argument("iv_file", help="Path to the AES IV file")
    parser_aes_decrypt.set_defaults(func=_aes_decrypt)

    # AES key generation command
    parser_aes_generate = subparsers.add_parser(
        "aes-generate-keys", help="Generate AES key and IV and save them to files"
    )
    parser_aes_generate.add_argument("key_file", help="Path to save the AES key file")
    parser_aes_generate.add_argument("iv_file", help="Path to save the AES IV file")
    parser_aes_generate.set_defaults(func=_aes_generate_keys)

    # HLS conversion command
    parser_hls_convert = subparsers.add_parser(
        "hls-convert", help="Convert a video to HLS format"
    )
    parser_hls_convert.add_argument("input_video", help="Path to the input video file")
    parser_hls_convert.add_argument("output_dir", help="Directory to save the HLS output")
    parser_hls_convert.set_defaults(func=_hls_convert)

    # HLS conversion with encryption command
    parser_hls_encrypt_convert = subparsers.add_parser(
        "hls-encrypt-convert", help="Convert and encrypt a video to HLS format"
    )
    parser_hls_encrypt_convert.add_argument("input_video", help="Path to the input video file")
    parser_hls_encrypt_convert.add_argument("output_dir", help="Directory to save the encrypted HLS output")
    parser_hls_encrypt_convert.set_defaults(func=_hls_encrypt_convert)

    # Encrypt existing HLS command
    parser_hls_encrypt_existing = subparsers.add_parser(
        "hls-encrypt-existing", help="Encrypt an existing HLS playlist"
    )
    parser_hls_encrypt_existing.add_argument("playlist_file", help="Path to the HLS playlist file")
    parser_hls_encrypt_existing.add_argument("output_dir", help="Directory to save the encrypted HLS output")
    parser_hls_encrypt_existing.set_defaults(func=_hls_encrypt_existing)

    # HLS decryption command
    parser_hls_decrypt = subparsers.add_parser(
        "hls-decrypt", help="Decrypt an HLS-encrypted video"
    )
    parser_hls_decrypt.add_argument("playlist_file", help="Path to the encrypted HLS playlist")
    parser_hls_decrypt.add_argument("decrypted_output", help="Path to save the decrypted video file")
    parser_hls_decrypt.add_argument("key_file", help="Path to the decryption key file")
    parser_hls_decrypt.add_argument("iv_file", help="Path to the IV file (optional)", nargs='?', default=None)
    parser_hls_decrypt.set_defaults(func=_hls_decrypt)

    # WebVTT generation for clear stream
    webvtt_clear_parser = subparsers.add_parser("webvtt-clear",
                                                help="Generate WebVTT and thumbnails for a clear video stream.")
    webvtt_clear_parser.add_argument("video_path", help="Input video file.")
    webvtt_clear_parser.add_argument("output_dir", help="Directory to save WebVTT and thumbnails.")
    webvtt_clear_parser.add_argument("--interval", type=int, default=5,
                                     help="Time interval between thumbnails in seconds.")
    webvtt_clear_parser.add_argument("--thumbnail-width", type=int, default=160, help="Thumbnail width.")
    webvtt_clear_parser.add_argument("--thumbnail-height", type=int, default=90, help="Thumbnail height.")
    webvtt_clear_parser.add_argument("--image-format", default="jpg",
                                     help="Image format for thumbnails (e.g., jpg, png).")
    webvtt_clear_parser.add_argument("--should-merge-thumbnails", action="store_true",
                                     help="Merge thumbnails into a single image.")
    webvtt_clear_parser.add_argument("--use-absolute-paths", action="store_true",
                                     help="Use absolute paths in WebVTT file.")
    webvtt_clear_parser.add_argument("--thumbnail-url", help="Base URL for thumbnail paths in WebVTT.")
    webvtt_clear_parser.set_defaults(func=_webvtt_generate_clear)

    # WebVTT generation for AES-encrypted stream
    webvtt_aes_parser = subparsers.add_parser("webvtt-aes",
                                              help="Generate WebVTT and thumbnails for an AES-encrypted video stream.")
    webvtt_aes_parser.add_argument("video_path", help="Input encrypted video file.")
    webvtt_aes_parser.add_argument("output_dir", help="Directory to save WebVTT and thumbnails.")
    webvtt_aes_parser.add_argument("key_file", help="AES key file.")
    webvtt_aes_parser.add_argument("iv_file", help="AES IV file.")
    webvtt_aes_parser.add_argument("--interval", type=int, default=5,
                                   help="Time interval between thumbnails in seconds.")
    webvtt_aes_parser.add_argument("--thumbnail-width", type=int, default=160, help="Thumbnail width.")
    webvtt_aes_parser.add_argument("--thumbnail-height", type=int, default=90, help="Thumbnail height.")
    webvtt_aes_parser.add_argument("--image-format", default="jpg",
                                   help="Image format for thumbnails (e.g., jpg, png).")
    webvtt_aes_parser.add_argument("--should-merge-thumbnails", action="store_true",
                                   help="Merge thumbnails into a single image.")
    webvtt_aes_parser.add_argument("--use-absolute-paths", action="store_true",
                                   help="Use absolute paths in WebVTT file.")
    webvtt_aes_parser.set_defaults(func=_webvtt_generate_aes)

    # WebVTT generation for HLS-encrypted stream
    webvtt_hls_parser = subparsers.add_parser("webvtt-hls",
                                              help="Generate WebVTT and thumbnails for an HLS-encrypted video stream.")
    webvtt_hls_parser.add_argument("video_path", help="Input HLS playlist file.")
    webvtt_hls_parser.add_argument("output_dir", help="Directory to save WebVTT and thumbnails.")
    webvtt_hls_parser.add_argument("key_file", help="AES key file for HLS decryption.")
    webvtt_hls_parser.add_argument("--interval", type=int, default=5,
                                   help="Time interval between thumbnails in seconds.")
    webvtt_hls_parser.add_argument("--thumbnail-width", type=int, default=160, help="Thumbnail width.")
    webvtt_hls_parser.add_argument("--thumbnail-height", type=int, default=90, help="Thumbnail height.")
    webvtt_hls_parser.add_argument("--image-format", default="jpg",
                                   help="Image format for thumbnails (e.g., jpg, png).")
    webvtt_hls_parser.add_argument("--should-merge-thumbnails", action="store_true",
                                   help="Merge thumbnails into a single image.")
    webvtt_hls_parser.add_argument("--use-absolute-paths", action="store_true",
                                   help="Use absolute paths in WebVTT file.")
    webvtt_hls_parser.add_argument("--thumbnail-url", help="Base URL for thumbnail paths in WebVTT.")
    webvtt_hls_parser.set_defaults(func=_webvtt_generate_hls)

    # Parse the arguments and call the appropriate function
    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
