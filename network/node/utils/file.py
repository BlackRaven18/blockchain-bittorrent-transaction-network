import base64
import os

from constants import FILES_DIR
def decode_and_save_file(file: bytes, filename: str):

    file_content = base64.b64decode(file)

    file_path = os.path.abspath(f"../{FILES_DIR}/{filename}.txt")

    with open(file_path, "wb") as f:
        f.write(file_content)
