import libtorrent as lt

import os
import time
import threading

from constants import FILES_DIR, TORRENTS_DIR, MAX_SEED_TIME

session = lt.session()
session.listen_on(6881, 6891)

seeded_torrents = []


class TorrentClient:
    def __init__(self):
        self.session = session

    def create_torrent(self, payload: str) -> str:
        payload_path = os.path.abspath(f"../{FILES_DIR}/{payload}")

        fs = lt.file_storage()
        lt.add_files(fs, payload_path)
        
        if fs.num_files() == 0:
            raise RuntimeError("No files found for torrent creation")

        t = lt.create_torrent(fs)
        t.set_creator("Document Transfer System")
        t.set_comment("Document transfer using libtorrent")

        lt.set_piece_hashes(t, os.path.dirname(payload_path))

        torrent_name = payload.split(".")[0] + ".torrent"

        torrent_file = os.path.abspath(f"../{TORRENTS_DIR}/{torrent_name}")

        with open(torrent_file, "wb") as f:
            f.write(lt.bencode(t.generate()))
        
        return torrent_file
    
    def seed_torrent_blocking(self, torrent_file_path: str) -> None:
        
        print("Starting torrent seeding...")
        print("Torrent file path: " + str(torrent_file_path))

        info = lt.torrent_info(torrent_file_path)
        params = {
            'save_path': os.path.abspath(f"../{FILES_DIR}"),
            'ti': info
        }

        handle = session.add_torrent(params)
        print(f"🚀 Seeding: {handle.name()}")

        start_time = time.time()

        while True:
            elapsed_time = time.time() - start_time
            if elapsed_time > MAX_SEED_TIME:
                print(f"⏳ Czas seedowania zakończony: {MAX_SEED_TIME} sekund.")
                break 

            status = handle.status()
            print(f"🌍 Peers: {status.num_peers} | ⬆️ Upload: {status.upload_rate / 1000:.2f} kB/s")
            time.sleep(1)

        session.remove_torrent(handle)

    def seed_torrent(self, torrent_file_path: str) -> None:
        """Funkcja nieblokująca uruchamiająca seedowanie w oddzielnym wątku"""
        seed_thread = threading.Thread(target=self.seed_torrent_blocking, args=(torrent_file_path,))
        seed_thread.daemon = True 

        seeded_torrents.append(seed_thread)

        seed_thread.start()

