import base64

from constants import FILES_DIR
def decode_and_save_file(file: bytes, filename: str):

    file_content = base64.b64decode(file)

    with open(f"../{FILES_DIR}/{filename}.txt", "wb") as f:
        f.write(file_content)
