import base64
import os

from args import args

from constants import FILES_DIR
def decode_and_save_file(file: bytes, sender: str, receiver: str):

    file_name = file.split("::")[0]
    file_content = base64.b64decode(file.split("::")[1])

    full_file_name = f"{sender}_{receiver}_{file_name}"

    if not os.path.exists(f"../{FILES_DIR}/{args.id}"):
        os.makedirs(f"../{FILES_DIR}/{args.id}")

    file_path = os.path.abspath(f"../{FILES_DIR}/{args.id}/{full_file_name}")

    print("File PAAAATH", file_path)

    with open(file_path, "wb") as f:
        f.write(file_content)

    return full_file_name
