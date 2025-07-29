"""
Yandex Music Downloader - A Python library for downloading music from Yandex Music.

This package provides a programmatic interface to download tracks, albums, playlists,
and other content from Yandex Music with support for various formats and quality settings.

Example usage:
    ```python
    from ymd import YandexMusicDownloader, CoreTrackQuality, LyricsFormat
    
    # Initialize the downloader with your Yandex Music OAuth token
    downloader = YandexMusicDownloader("your_oauth_token_here")
    
    # Download a single track
    downloader.download_track(
        track_id="12345678",  # or URL like "https://music.yandex.ru/album/12345678/track/7654321"
        output_dir="./downloads",
        quality=CoreTrackQuality.NORMAL,
        lyrics_format=LyricsFormat.TEXT,
        embed_cover=True
    )
    
    # Download an entire album
    downloader.download_album(
        album_id="87654321",  # or URL
        output_dir="./downloads/albums",
        quality=CoreTrackQuality.NORMAL
    )
    ```
"""

from ymd.core import (
    CoreTrackQuality,
    LyricsFormat
)

from ymd.api_interface import YandexMusicDownloader


__version__ = "0.2.0"
__all__ = [
    # Main interface
    'YandexMusicDownloader',
    
    # Core functionality
    'CoreTrackQuality',
    'LyricsFormat',

]
