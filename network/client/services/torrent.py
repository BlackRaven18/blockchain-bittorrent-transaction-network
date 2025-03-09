import libtorrent as lt

import time

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
        print(f"📊 {status.progress * 100:.2f}% | Peers: {status.num_peers} | ⬇️ Download: {status.download_rate / 1000:.2f} kB/s")
        time.sleep(2)

    session.remove_torrent(handle)

    print("✅ Pobieranie zakończone!")