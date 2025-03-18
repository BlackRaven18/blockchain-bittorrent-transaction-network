import libtorrent as lt

import time
import os
import base64

from args import args

def save_torrent(torrent_file: str) -> str:
    torrent_name = torrent_file.split("::")[0]
    decoded_torrent = base64.b64decode(torrent_file.split("::")[1])

    save_path = os.path.abspath(f"downloaded/{args.id}/{torrent_name}")

    with open(save_path, "wb") as f:
        f.write(decoded_torrent)

    return save_path

def download_torrent(torrent_url: str, download_dir: str) -> None:
    session = lt.session()
    session.listen_on(6881, 6891)

    info = lt.torrent_info(torrent_url)
    params = {
        'save_path': download_dir,
        'ti': info
    }

    handle = session.add_torrent(params)
    print(f"📥 Pobieranie: {handle.name()}")

    while not handle.status().is_seeding:
        status = handle.status()
        print(f"📊 {status.progress * 100:.2f}% | ⬇️ Download: {status.download_rate / 1000:.2f} kB/s")
        time.sleep(2)

    session.remove_torrent(handle)

    print("✅ Pobieranie zakończone!")