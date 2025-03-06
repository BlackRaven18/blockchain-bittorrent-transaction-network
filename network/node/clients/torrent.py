import libtorrent as lt

import os

from constants import FILES_DIR, TORRENTS_DIR

session = lt.session()
session.listen_on(6881, 6891)

class TorrentClient:
    def __init__(self):
        self.session = session

    def create_torrent(self, payload):
        payload_path = os.path.abspath(f"../{FILES_DIR}/{payload}.txt")

        print("Payload path: " + str(payload_path))

        fs = lt.file_storage()
        lt.add_files(fs, payload_path)
        
        if fs.num_files() == 0:
            raise RuntimeError("No files found for torrent creation")

        t = lt.create_torrent(fs)
        t.set_creator("Document Transfer System")
        t.set_comment("Document transfer using libtorrent")

        lt.set_piece_hashes(t, os.path.dirname(payload_path))

        torrent_file = os.path.join(f"../{TORRENTS_DIR}", f"{payload}.torrent")

        with open(torrent_file, "wb") as f:
            f.write(lt.bencode(t.generate()))
        
        return torrent_file
