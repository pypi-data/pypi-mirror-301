"""
# WebVTT Generation for Thumbnail Scrubbing with Support for Encrypted Video Streams

## Table of Contents
1. [Purpose](#purpose)
2. [Features Supported](#features-supported)
3. [Prerequisites](#prerequisites)
    - [Required Tools](#required-tools)
    - [FFmpeg Installation](#ffmpeg-installation)
4. [Installation](#installation)
5. [Command Line Usage](#command-line-usage)
6. [How to Use the Code](#how-to-use-code)
    - [AES Encryption/Decryption Test](#aes-encryptiondecryption-test)
    - [HLS Conversion Test (Without Encryption)](#hls-conversion-test-without-encryption)
    - [HLS Conversion with Encryption](#hls-conversion-with-encryption)
    - [Encrypt an Existing Clear HLS Stream](#encrypt-an-existing-clear-hls-stream)
    - [Decrypt an HLS Stream](#decrypt-an-hls-stream)
    - [WebVTT and Thumbnail Generation for Clear Stream](#webvtt-and-thumbnail-generation-for-clear-stream)
    - [WebVTT and Thumbnail Generation for AES Encrypted Stream](#webvtt-and-thumbnail-generation-for-aes-encrypted-stream)
    - [WebVTT and Thumbnail Generation for HLS Encrypted Stream](#webvtt-and-thumbnail-generation-for-hls-encrypted-stream)
7. [Summary](#summary)

---

## Purpose

This project provides a comprehensive solution for generating WebVTT files and thumbnails to enable video scrubbing.
Allowing users to preview video content efficiently. The primary goal of the tool is to generate WebVTT files for both clear (unencrypted) and encrypted video streams.

In the case of encrypted videos, the tool supports various decryption methods (such as AES and HLS) to facilitate the WebVTT generation process.
It can decrypt encrypted video streams, generate thumbnails at specific intervals, and produce the corresponding WebVTT files to enable seamless thumbnail scrubbing.

Additionally, while the primary purpose of the tool is to assist with WebVTT generation.
It also includes robust features for video encryption and decryption. This ensures that video content remains secure when necessary, and allows users to convert, encrypt, or decrypt video streams as part of the workflow.
This project provides a comprehensive solution for video processing, including:
- **Thumbnail scrubbing** and **WebVTT** generation for both clear and encrypted video streams (AES and HLS).
- **AES-based encryption and decryption** of video files.
- **HLS (HTTP Live Streaming)** video conversion with optional encryption.

---
## Features Supported

* **WebVTT generation and thumbnail scrubbing**: The core feature of this tool is the ability to generate WebVTT files and thumbnails for videos. This enables smooth scrubbing functionality, allowing users to preview video content efficiently as they seek through the video timeline.
* **Support for encrypted and unencrypted streams**: Whether the video is encrypted or not, the tool can handle both. It will decrypt the video (if needed) and then generate WebVTT and thumbnail files for scrubbing.
* **Encryption and decryption** capabilities:
    - AES-based encryption and decryption: The tool can encrypt video files using AES encryption in CBC mode, making the content secure. It also supports decrypting these files for WebVTT generation.
    - HLS (HTTP Live Streaming) encryption: In addition to AES encryption, this tool can handle video streams that are encrypted using HLS encryption. It can decrypt HLS streams and generate WebVTT and thumbnail files accordingly.
* **Flexible video handling**: The tool can process videos from both local files and remote URLs, ensuring flexibility in handling different sources of video content.
* **Automatic directory management**: Output directories are automatically created for storing decrypted files, thumbnails, and WebVTT files, making the workflow efficient and streamlined.
* **Thumbnail merging**: It offers the option to merge thumbnails into a single image or keep them separate, depending on your needs.
* **Seamless video preview**: By providing WebVTT and thumbnail scrubbing, this tool enhances the user's experience by allowing for fast and efficient previewing of video content, especially useful for long video files.

---

## Prerequisites

### *Required Tools*
- **Python 3.8+**
- **FFmpeg**: A powerful multimedia framework used for converting, encrypting, and decrypting video streams.
- **opencv-python**: This package is essential for performing tasks related to computer vision, image, and video processing.
- **Pillow**: This library is used for working with images, such as opening, manipulating, and saving different image formats.
- **pycryptodome**: This package is used for cryptographic operations, including AES encryption and decryption.

### *FFmpeg Installation*

##### For Windows:
1. Download the latest FFmpeg build from [FFmpeg Official Website](https://ffmpeg.org/download.html).
2. Extract the ZIP folder.
3. Add the `bin` folder to your system's environment `PATH` variable:
   - Right-click on **This PC** > **Properties**.
   - Click **Advanced system settings**.
   - Under **System Properties**, go to the **Advanced** tab and click **Environment Variables**.
   - Find the **Path** variable under **System Variables** and click **Edit**.
   - Add the path to the `bin` directory inside the FFmpeg folder.

##### For macOS:
1. Install using Homebrew:
```python
brew install ffmpeg
```
##### For Linux:
1. Install via package manager:
```python
sudo apt update
sudo apt install ffmpeg
```
2. Once FFmpeg is installed and added to the system path, you can verify it by running:
```python
ffmpeg -version
```
---

## Installation

1. **Install required dependencies using pip**
```python
pip install -r requirements.txt
```
If you don't want to install using requirement.txt, do it manually
```python
pip install opencv-python==4.10.0.84  # Install OpenCV for image and video processing
pip install Pillow==10.4.0            # Install Pillow for image manipulation and processing
pip install pycryptodome==3.21.0      # Install PyCryptodome for encryption and decryption functionalities
```

2. **Install ThumbTrail**
```python
pip install thumbtrail
```
**Ensure FFmpeg is installed and available in your system path as described in the Prerequisites section.**

---

## Command Line Usage
ThumbTrail provides a command-line interface (CLI) to handle AES encryption, HLS stream conversion, encryption, and decryption, as well as WebVTT and thumbnail generation for video scrubbing.

###### **AES Key Generation**
* Generates an AES encryption key and initialization vector (IV) for AES encryption. The generated key and IV are saved to specified files.
    - **key_file**: Path to save the AES key e.g. 'keys/aes_key.key'.
    - **iv_file**: Path to save the AES IV e.g. keys/aes_iv.key.

```python
thumbtrail aes-generate-keys <key_file> <iv_file>
```
*Example*: thumbtrail aes-generate-keys keys/aes_key.key keys/aes_iv.key


###### **AES Video Encryption**
* Encrypts a video using AES encryption with the specified key and IV.
    - **input_video**: Path to the input video file to be encrypted e.g. 'samples/input.mp4'.
    - **encrypted_video**: Path to save the AES-encrypted video e.g. 'output/encrypted.mp4'.
    - **key_file**: Path to the AES key file e.g. 'keys/aes_key.key'.
    - **iv_file**: Path to the AES IV file e.g. 'keys/aes_iv.key'.
```python
thumbtrail aes-encrypt <input_video> <encrypted_video> <key_file> <iv_file>
```
*Example*: thumbtrail aes-encrypt samples/input.mp4 output/encrypted.mp4 keys/aes_key.key keys/aes_iv.key

###### **AES Video Decryption**
* Decrypts an AES-encrypted video using the specified key and IV.
    - **encrypted_video**: Path to the AES-encrypted video file e.g. 'output/encrypted.mp4'.
    - **decrypted_video**: Path to save the decrypted video e.g. 'output/decrypted.mp4'.
    - **key_file**: Path to the AES key file e.g. 'keys/aes_key.key'.
    - **iv_file**: Path to the AES IV file e.g. 'keys/aes_iv.key'.
```python
thumbtrail aes-decrypt <encrypted_video> <decrypted_video> <key_file> <iv_file>
```
*Example*: thumbtrail aes-decrypt output/encrypted.mp4 output/decrypted.mp4 keys/aes_key.key keys/aes_iv.key

###### **HLS Conversion (Without Encryption)**
* Converts a video to HLS format (without encryption).
    - **input_video**: Path to the input video file to be converted e.g. 'samples/sample_file.mp4'.
    - **output_dir**: Directory where the converted HLS files will be saved e.g. 'output/hls'.
```python
thumbtrail hls-convert <input_video> <output_dir>
```
*Example*: thumbtrail hls-convert samples/sample_file.mp4 output/hls


###### **HLS Conversion with Encryption**
* Converts a video to HLS format with AES encryption. The HLS stream and the encryption key info file are generated.
    - **input_video**: Path to the input video file to be converted e.g. 'samples/sample_file.mp4'.
    - **output_dir**: Directory where the encrypted HLS files will be saved e.g. 'output/hls_encrypted'.
```python
thumbtrail hls-encrypt-convert <input_video> <output_dir>
```
*Example*: thumbtrail hls-encrypt-convert samples/sample_file.mp4 output/hls_encrypted

###### **Encrypt an Existing HLS Stream**
* Encrypts an existing HLS stream using AES encryption. The playlist and video segments are encrypted.
    - **playlist_file**: Path to the existing HLS playlist file e.g. 'output/hls/output.m3u8'.
    - **output_dir**: Directory where the encrypted HLS files will be saved e.g. 'output/hls_encrypted'.
```python
thumbtrail hls-encrypt-existing <playlist_file> <output_dir>
```
*Example*: thumbtrail hls-encrypt-existing output/hls/output.m3u8 output/hls_encrypted


###### **HLS Decryption**
* Decrypts an AES-encrypted HLS playlist using the provided key and IV.
    - **encrypted_playlist**: Path to the encrypted HLS playlist file e.g. 'output/hls_encrypted/output_encrypted.m3u8'.
    - **decrypted_video**: Path to save the decrypted video e.g. 'output/decrypted.mp4'.
    - **key_file**: Path to the AES key file e.g. 'output/hls_encrypted/hls_key.key'.
    - **iv_file**: Path to the AES IV file e.g. 'output/hls_encrypted/hls_iv.key'.
```python
thumbtrail hls-decrypt <encrypted_playlist> <decrypted_video> <key_file> <iv_file>
```
*Example*: thumbtrail hls-decrypt output/hls_encrypted/output_encrypted.m3u8 output/decrypted.mp4 output/hls_encrypted/hls_key.key output/hls_encrypted/hls_iv.key


###### **WebVTT Generation for Clear Video**
* Generates WebVTT and thumbnails for a clear video stream.
    - **input_video**: Path to the input video file e.g. 'samples/sample_file.mp4'.
    - **output_dir**: Directory where the WebVTT and thumbnails will be saved e.g. 'output/webvtt'.
    - **interval**: Time interval between thumbnails (in seconds) e.g. 2.
    - **thumbnail_width**: Width of each thumbnail e.g. 160.
    - **thumbnail_height**: Height of each thumbnail e.g. 90.

```python
thumbtrail webvtt-clear <input_video> <output_dir> --interval <interval> --thumbnail-width <thumbnail_width> --thumbnail-height <thumbnail_height>
```
*Example*: thumbtrail webvtt-clear samples/sample_file.mp4 output/webvtt --interval 2 --thumbnail-width 160 --thumbnail-height 90

###### **WebVTT Generation for AES-encrypted Video**
* Generates WebVTT and thumbnails for an AES-encrypted video stream.
	- **encrypted_video**: Path to the AES-encrypted video file e.g. 'output/encrypted.mp4'.
	- **output_dir**: Directory where the WebVTT and thumbnails will be saved e.g. 'output/webvtt_aes'.
	- **key_file**: Path to the AES key file e.g. 'keys/aes_key.key'.
	- **iv_file**: Path to the AES IV file e.g. 'keys/aes_iv.key'.
	- **interval**: Time interval between thumbnails (in seconds) e.g. 2.
	- **thumbnail_width**: Width of each thumbnail e.g. 160.
	- **thumbnail_height**: Height of each thumbnail e.g. 90.

```python
thumbtrail webvtt-aes <encrypted_video> <output_dir> <key_file> <iv_file> --interval <interval> --thumbnail-width <thumbnail_width> --thumbnail-height <thumbnail_height>
```
*Example*: thumbtrail webvtt-aes output/encrypted.mp4 output/webvtt_aes keys/aes_key.key keys/aes_iv.key --interval 2 --thumbnail-width 160 --thumbnail-height 90


###### **WebVTT Generation for HLS-encrypted Video**
* Generates WebVTT and thumbnails for an HLS-encrypted video stream.
	- **encrypted_playlist**: Path to the encrypted HLS playlist file e.g. 'output/hls_encrypted/output_encrypted.m3u8'.
	- **output_dir**: Directory where the WebVTT and thumbnails will be saved e.g. 'output/webvtt_hls'.
	- **key_file**: Path to the AES key file e.g. 'keys/hls_key.key'.
	- **interval**: Time interval between thumbnails (in seconds) e.g. 2.
	- **thumbnail_width**: Width of each thumbnail e.g. 160.
	- **thumbnail_height**: Height of each thumbnail e.g. 90.

```python
thumbtrail webvtt-hls <encrypted_playlist> <output_dir> <key_file> --interval <interval> --thumbnail-width <thumbnail_width> --thumbnail-height <thumbnail_height>
```

*Example*: thumbtrail webvtt-hls output/hls_encrypted/output_encrypted.m3u8 output/webvtt_hls keys/hls_key.key --interval 2 --thumbnail-width 160 --thumbnail-height 90

###### **Thumbtrail Command Line HELP**
* Running this command displays a list of all available commands and their usage.

```python
thumbtrail --help
```

* How to use specific command and know its required arguments.
```python
thumbtrail webvtt-hls --help
```

---

## How to Use Code
This is direct and clear, making it easy for users to understand that the following examples show how to use the code.

###### **AES Encryption/Decryption Test**
* The following test encrypts and decrypts a video file using AES encryption.

```python
from thumbtrail.cryptomanager import CryptoManager

crypto_manager = CryptoManager()

# File paths for testing
input_video = 'samples/sample_file.mp4'
encrypted_video = 'output/aes/encrypted_video.mp4'
decrypted_video = 'output/aes/decrypted_video.mp4'
key_file = 'output/aes/aes_key.key'
iv_file = 'output/aes/aes_iv.key'

# Generate AES key and IV
crypto_manager.generate_aes_key_iv()

# Optionally, save the generated key and IV to files for later use
crypto_manager.save_aes_key_iv(key_file, iv_file)

# Encrypt the video
crypto_manager.encrypt_video_aes(input_video, encrypted_video)

# Decrypt the video
crypto_manager.decrypt_video_aes(encrypted_video, decrypted_video)

# Alternatively, load the AES key and IV from files for decryption
crypto_manager.load_aes_key_iv(key_file, iv_file)
crypto_manager.decrypt_video_aes(encrypted_video, decrypted_video)
```


###### **HLS Conversion Test (Without Encryption)**
* Convert a video file to HLS format without encryption.
```python
# Import the CryptoManager class from the thumbtrail.cryptomanager module
from thumbtrail.cryptomanager import CryptoManager

# Create an instance of CryptoManager to handle video encryption, decryption, and conversions
crypto_manager = CryptoManager()

# Define the input video file path. This is the video that will be converted to HLS format.
input_video = 'samples/sample_file.mp4'

# Define the output directory where the converted HLS files (playlist and segments) will be saved.
output_dir = 'output/test1'

# Call the convert_video_to_hls method to convert the input video to HLS format without encryption.
crypto_manager.convert_video_to_hls(input_video, output_dir)
```


###### **HLS Conversion with Encryption**
* Convert a video file to HLS format with AES encryption.
```python
from thumbtrail.cryptomanager import CryptoManager  # Import the CryptoManager class from the thumbtrail.cryptomanager module

# Create an instance of CryptoManager to handle video encryption, decryption, and conversions
crypto_manager = CryptoManager()

# Define the input video file path. This is the video that will be converted to HLS format with encryption.
input_video = 'samples/sample_file.mp4'

# Define the output directory where the encrypted HLS files (playlist, segments, and encryption keys) will be saved.
output_dir = 'output/test2'

# Generate HLS encryption key information (key file, key info file, and initialization vector).
# This method prepares the necessary encryption parameters for HLS encryption.
key_file, key_info_file, iv_hex = crypto_manager.generate_hls_key_info(output_dir)

# Convert the input video to HLS format with encryption enabled by passing the key_info_file.
# The HLS segments and playlist generated in this step will be encrypted.
crypto_manager.convert_video_to_hls(input_video, output_dir, key_info_file)
```


###### **Encrypt an Existing Clear HLS Stream**
* Encrypt an existing HLS stream (without encryption).
```python
from thumbtrail.cryptomanager import CryptoManager  # Import the CryptoManager class from the thumbtrail.cryptomanager module

# Create an instance of CryptoManager to handle video encryption and decryption
crypto_manager = CryptoManager()

# Define the path to the existing HLS playlist file that needs to be encrypted.
# This playlist file contains references to video segments that are currently not encrypted.
playlist_file = 'output/test1/output.m3u8'

# Define the output directory where the encrypted HLS playlist and segments will be saved.
output_dir = 'output/test3'

# Call the encrypt_existing_hls method to encrypt the existing HLS playlist and segments.
# This will encrypt the video segments referenced in the playlist and create an updated playlist with encryption.
crypto_manager.encrypt_existing_hls(playlist_file, output_dir)
```


###### **Decrypt an HLS Stream**
* Decrypt an AES-encrypted HLS stream.
```python
# Import the CryptoManager class from the thumbtrail.cryptomanager module
from thumbtrail.cryptomanager import CryptoManager

# Create an instance of CryptoManager to handle video decryption
crypto_manager = CryptoManager()

# Define the path to the encrypted HLS playlist file that needs to be decrypted
playlist_file = 'output/test2/output.m3u8'

# Define the path to the decryption key file, which contains the AES key used for encryption
decryption_key_file = 'output/test2/hls_key.key'

# Define the path to the initialization vector (IV) file, if applicable
iv_file = 'output/test2/hls_iv.key'

# Define the output path for the decrypted video file
decrypted_output_file = 'output/test4/output_decrypted.mp4'

# Ensure that the output directory for the decrypted video exists
# This step checks if the directory exists and creates it if not
output_dir = os.path.dirname(decrypted_output_file)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Check if the HLS stream is encrypted by verifying the presence of the decryption key file
if os.path.exists(decryption_key_file):
    print("Encrypted stream detected. Proceeding with decryption...")

    # Open the decryption key file and load the AES key from it
    with open(decryption_key_file, 'rb') as f:
        decryption_key = f.read()

    # Convert the AES key from bytes to a hex string format, which is required for decryption
    decryption_key_hex = decryption_key.hex()

    # Check if an initialization vector (IV) file exists
    if os.path.exists(iv_file):
        # If the IV file exists, load the IV from the file and convert it to hex format
        with open(iv_file, 'rb') as f:
            iv_hex = f.read().hex()
        # Decrypt the HLS video stream using both the decryption key and the IV
        crypto_manager.decrypt_hls_video(playlist_file, decrypted_output_file, decryption_key_hex, iv_hex)
    else:
        # If no IV is needed, decrypt the HLS video using only the decryption key
        crypto_manager.decrypt_hls_video(playlist_file, decrypted_output_file, decryption_key_hex)
else:
    # If no encryption is detected (i.e., no key file is found), skip the decryption process
    print("No encryption detected. Skipping decryption.")
```


###### **WebVTT and Thumbnail Generation for Clear Stream**
* Generate WebVTT and thumbnails for a clear stream (non-encrypted).
```python
# Import the Scrubber class from the thumbtrail.scrubber module
from thumbtrail.scrubber import Scrubber

# Define the path to the video file. This video is a decrypted, clear video stream (no encryption).
video_path = "output/aes/decrypted_video.mp4"

# Define the output directory where the generated thumbnails and WebVTT file will be stored.
output_dir = "output/webvtt_clear"

# Initialize an instance of Scrubber for processing the clear video stream.
# Since this is a clear stream, no decryption is needed.
thumb_scrub = Scrubber(video_path, output_dir)

# Generate thumbnails and WebVTT (used for thumbnail navigation in video players).
thumb_scrub.generate_thumbnails_and_webvtt(
    interval=2,  # Time interval (in seconds) between thumbnails (every 2 seconds)
    thumbnail_size=(160, 90),  # Size of each thumbnail (width x height)
    image_format="jpg",  # Format of the thumbnail images (JPEG in this case)
    should_merge_thumbnails=True,  # Option to merge all thumbnails into a single image
    use_absolute_paths=False  # Use relative paths in the WebVTT file (instead of absolute paths)
)
```


###### **WebVTT and Thumbnail Generation for AES Encrypted Stream**
* Generate WebVTT and thumbnails for an AES-encrypted video.
```python
# Import the Scrubber class from the thumbtrail.scrubber module
from thumbtrail.scrubber import Scrubber

# Define the path to the AES-encrypted video file that will be processed for thumbnail generation.
video_path = "output/aes/encrypted_video.mp4"

# Define the output directory where the generated thumbnails and WebVTT file will be stored.
output_dir = "output/webvtt_aes"

# Define the path to the AES encryption key file. This key is required to decrypt the video.
key_file = "output/aes/aes_key.key"

# Define the path to the initialization vector (IV) file. This is also required for AES decryption.
iv_file = "output/aes/aes_iv.key"

# Initialize an instance of Scrubber for processing the AES-encrypted video stream.
# The decryption method is specified as 'AES', and the key_file and iv_file are passed for decryption.
thumb_scrub = Scrubber(video_path, output_dir, decryption_method='AES', key_file=key_file, iv_file=iv_file)

# Generate thumbnails and WebVTT (used for thumbnail navigation in video players) from the decrypted video.
thumb_scrub.generate_thumbnails_and_webvtt(
    interval=2,  # Time interval (in seconds) between thumbnails (every 2 seconds)
    thumbnail_size=(160, 90),  # Size of each thumbnail (width x height)
    image_format="jpg",  # Format of the thumbnail images (JPEG in this case)
    should_merge_thumbnails=False,  # Do not merge the thumbnails into a single image; keep them separate
    use_absolute_paths=False  # Use relative paths in the WebVTT file (instead of absolute paths)
)
```


###### **WebVTT and Thumbnail Generation for HLS Encrypted Stream**
* Generate WebVTT and thumbnails for an HLS-encrypted video.
```python
# Import the Scrubber class from the thumbtrail.scrubber module
from thumbtrail.scrubber import Scrubber

# Define the path to the HLS playlist file (m3u8) that is encrypted.
# This playlist contains references to encrypted video segments.
video_path = "output/test2/output.m3u8"

# Define the output directory where the generated thumbnails and WebVTT file will be stored.
output_dir = "output/webvtt_hls"

# Define the path to the HLS decryption key file, which contains the AES key used to decrypt the video segments.
key_file = "output/test2/hls_key.key"

# Initialize an instance of Scrubber for processing the HLS-encrypted video stream.
# The decryption method is specified as 'HLS', and the key_file is passed for decrypting the video.
thumb_scrub = Scrubber(video_path, output_dir, decryption_method='HLS', key_file=key_file)

# Generate thumbnails and WebVTT (used for thumbnail navigation in video players) from the decrypted HLS stream.
thumb_scrub.generate_thumbnails_and_webvtt(
    interval=2,  # Time interval (in seconds) between thumbnails (every 2 seconds)
    thumbnail_size=(160, 90),  # Size of each thumbnail (width x height)
    image_format="jpg",  # Format of the thumbnail images (JPEG in this case)
    should_merge_thumbnails=False,  # Do not merge the thumbnails into a single image; keep them separate
    use_absolute_paths=True,  # Use absolute paths in the WebVTT file (necessary for external URLs)
    thumbnail_url="http://www.myscrubber.com"  # Optional URL for thumbnail links (useful for remote video streaming)
)
```

## Summary

1. **GitHub Repository**: The full source code and issue tracking for this project are available on GitHub. You can access the repository at [GitHub Link](https://github.com/Sariya-Ansari/thumbtrail.git). Feel free to contribute, open issues, or report bugs.
2. **Documentation**: Comprehensive documentation for the project is available at [Documentation Link](https://thumbtrail.vercel.app). It includes step-by-step usage guides, configuration examples, and details about each feature.
3. **Widevine DRM**: Widevine DRM is not supported in this release due to licensing and technical complexities. The tool focuses on AES and HLS encryption for secure video streaming, which covers a wide range of use cases.
4. **Supported Platforms**: The tool is compatible with multiple platforms, including Windows, macOS, and Linux. Ensure that you have installed FFmpeg and the required Python dependencies before using the CLI.
5. **Compatibility**: The tool generates WebVTT files, which are widely supported by popular video players (e.g., VLC, JWPlayer, HTML5 Video) for thumbnail scrubbing.
6. **Licensing**: This project is released under the MIT License, which means it is free to use and modify. Contributions and forks are welcome.
7. **Key Features**:
    - AES Encryption/Decryption of video files.
    - HLS Conversion with optional AES encryption for secure streaming.
    - WebVTT and Thumbnail Generation for both clear and encrypted streams.

"""