"""
High-level API interface for Yandex Music Downloader.

This module provides a clean, user-friendly interface for downloading tracks, albums,
and playlists from Yandex Music.
"""
import logging
from pathlib import Path
from typing import Optional, Union, List

from yandex_music import Client, Track, Album

from ymd.core import (
    CoreTrackQuality,
    LyricsFormat,
    download_track as core_download_track,
    to_downloadable_track,
)

logger = logging.getLogger(__name__)

class YandexMusicDownloader:
    """Main class for interacting with Yandex Music Downloader.
    
    This class provides methods to download tracks, albums, and playlists
    from Yandex Music with various options for quality and metadata.
    """
    
    def __init__(self, token: str, timeout: int = 10, max_retries: int = 3, retry_delay: int = 5):
        """Initialize the Yandex Music Downloader.
        
        Args:
            token: Yandex Music OAuth token
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
            retry_delay: Delay between retries in seconds
        """
        self.client = Client(token).init()
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.covers_cache = {}  # Cache for album covers to avoid re-downloading
    
    def download_track(
        self,
        track_id: Union[str, int],
        output_dir: Union[str, Path],
        quality: CoreTrackQuality = CoreTrackQuality.NORMAL,
        lyrics_format: LyricsFormat = LyricsFormat.NONE,
        embed_cover: bool = True,
        cover_resolution: int = 800,
        compatibility_level: int = 1,
    ) -> Path:
        """Download a single track by its ID.
        
        Args:
            track_id: Yandex Music track ID or URL
            output_dir: Directory to save the downloaded track
            quality: Audio quality (LOW, NORMAL, LOSSLESS)
            lyrics_format: Format for lyrics (NONE, TEXT, LRC)
            embed_cover: Whether to embed album cover in the file
            cover_resolution: Resolution of the embedded cover art
            compatibility_level: Tag compatibility level (1-3)
            
        Returns:
            Path to the downloaded file
        """
        if isinstance(track_id, str) and not track_id.isdigit():
            # Extract track ID from URL if a URL was provided
            track_id = self._extract_track_id(track_id)
        
        track = self.client.tracks(track_id)[0]
        return self._download_track_impl(
            track=track,
            output_dir=output_dir,
            quality=quality,
            lyrics_format=lyrics_format,
            embed_cover=embed_cover,
            cover_resolution=cover_resolution,
            compatibility_level=compatibility_level,
        )
    
    def download_album(
        self,
        album_id: Union[str, int],
        output_dir: Union[str, Path],
        quality: CoreTrackQuality = CoreTrackQuality.NORMAL,
        lyrics_format: LyricsFormat = LyricsFormat.NONE,
        embed_cover: bool = True,
        cover_resolution: int = 800,
        compatibility_level: int = 1,
    ) -> List[Path]:
        """Download all tracks from an album.
        
        Args:
            album_id: Yandex Music album ID or URL
            output_dir: Base directory to save the downloaded tracks
            quality: Audio quality (LOW, NORMAL, LOSSLESS)
            lyrics_format: Format for lyrics (NONE, TEXT, LRC)
            embed_cover: Whether to embed album cover in the files
            cover_resolution: Resolution of the embedded cover art
            compatibility_level: Tag compatibility level (1-3)
            
        Returns:
            List of paths to downloaded files
        """
        if isinstance(album_id, str) and not album_id.isdigit():
            # Extract album ID from URL if a URL was provided
            album_id = self._extract_album_id(album_id)
        
        album = self.client.albums_with_tracks(album_id)
        
        # Create artist/album directory structure
        safe_artist_name = self._sanitize_filename(album.artists[0].name) if album.artists else "Unknown Artist"
        safe_album_title = self._sanitize_filename(album.title) if album.title else "Unknown Album"
        
        # Create the full output path: output_dir/artist_name/album_name
        album_output_dir = Path(output_dir) / safe_artist_name / safe_album_title
        album_output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Downloading album '{safe_album_title}' by '{safe_artist_name}' to: {album_output_dir}")
        
        output_paths = []
        
        for volume in album.volumes:
            for track in volume:
                if track:
                    track_path = self._download_track_impl(
                        track=track,
                        output_dir=album_output_dir,
                        quality=quality,
                        lyrics_format=lyrics_format,
                        embed_cover=embed_cover,
                        cover_resolution=cover_resolution,
                        compatibility_level=compatibility_level,
                        album=album,
                    )
                    output_paths.append(track_path)
        
        return output_paths

    def _download_track_impl(
        self,
        track: Track,
        output_dir: Union[str, Path],
        quality: CoreTrackQuality,
        lyrics_format: LyricsFormat,
        embed_cover: bool,
        cover_resolution: int,
        compatibility_level: int,
        album: Optional[Album] = None,
    ) -> Path:
        """Internal implementation of track downloading."""

        # Create output directory if it doesn't exist
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Prepare track for downloading
        safe_artist_name = track.artists[0].name if track.artists else "Unknown"
        safe_title = track.title or "Unknown"
        base_path = output_dir / f"{safe_artist_name} - {safe_title}"
        downloadable_track = to_downloadable_track(track, quality, base_path)
        
        # Download the track with shared covers cache
        core_download_track(
            track_info=downloadable_track,
            cover_resolution=cover_resolution,
            lyrics_format=lyrics_format,
            embed_cover=embed_cover,
            covers_cache=self.covers_cache,  # Use instance-level cache
            compatibility_level=compatibility_level,
        )
        
        return downloadable_track.path
    
    def _extract_track_id(self, url: str) -> str:
        """Extract track ID from URL."""
        # Implementation for extracting track ID from URL
        # This is a simplified version - you might want to enhance this
        if "/track/" in url:
            return url.split("/track/")[1].split("/")[0].split("?")[0]
        raise ValueError(f"Could not extract track ID from URL: {url}")
    
    def _extract_album_id(self, url: str) -> str:
        """Extract album ID from URL."""
        if "/album/" in url:
            return url.split("/album/")[1].split("/")[0].split("?")[0]
        raise ValueError(f"Could not extract album ID from URL: {url}")
    
    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename by removing invalid characters."""
        # Replace invalid filename characters with underscores
        invalid_chars = '<>:"/\\|?*\0'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        # Remove leading/trailing whitespace and dots
        filename = filename.strip('. ')
        # Replace multiple spaces with a single space
        filename = ' '.join(filename.split())
        return filename


# For backward compatibility
download_track = YandexMusicDownloader.download_track
download_album = YandexMusicDownloader.download_album
