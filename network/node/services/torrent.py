import libtorrent as lt
import os

from constants import FILES_DIR, TORRENTS_DIR

def create_torrent(file_path: str) -> str:

    file_destination = os.path.abspath(f"../{FILES_DIR}/{file_path}.txt")

    print("File destination: " + str(file_destination))


    fs = lt.file_storage()
    lt.add_files(fs, file_destination)

    filename = os.path.basename(file_destination).split(".")[0]

    print("Filename: " + str(filename))
    print("Number of files: " + str(fs.num_files()))
    
    if fs.num_files() == 0:
        raise RuntimeError("No files found for torrent creation")

    t = lt.create_torrent(fs)
    t.set_creator("PDF Transfer System")
    t.set_comment("PDF transfer using libtorrent")

    lt.set_piece_hashes(t, os.path.dirname(file_destination))

    torrent_file = os.path.join(f"../{TORRENTS_DIR}", f"{filename}.torrent")
    with open(torrent_file, "wb") as f:
        f.write(lt.bencode(t.generate()))
    
    return torrent_file