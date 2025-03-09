import base64
import os

from constants import FILES_DIR
def decode_and_save_file(file: bytes, sender: str, receiver: str):

    file_name = file.split("::")[0]
    file_content = base64.b64decode(file.split("::")[1])

    full_file_name = f"{sender}_{receiver}_{file_name}"

    file_path = os.path.abspath(f"../{FILES_DIR}/{full_file_name}")

    with open(file_path, "wb") as f:
        f.write(file_content)

    return full_file_name
