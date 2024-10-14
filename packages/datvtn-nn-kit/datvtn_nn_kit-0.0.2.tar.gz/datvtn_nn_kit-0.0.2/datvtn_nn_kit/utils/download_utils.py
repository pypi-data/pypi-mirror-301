import math
import os
import requests
from torch.hub import download_url_to_file, get_dir
from tqdm import tqdm
from urllib.parse import urlparse

from datvtn_kit.common.misc import format_size


def download_file_from_google_drive(file_id: str, save_path: str) -> None:
    """Download files from Google Drive using the file ID.

    Args:
        file_id (str): File ID from Google Drive.
        save_path (str): Local path to save the downloaded file.
    """
    URL = 'https://docs.google.com/uc?export=download'
    session = requests.Session()
    params = {'id': file_id}

    response = session.get(URL, params=params, stream=True)
    token = _get_confirm_token(response)
    if token:
        params['confirm'] = token
        response = session.get(URL, params=params, stream=True)

    # Retrieve file size if available
    file_size = _get_file_size(session, URL, params)
    _save_response_content(response, save_path, file_size)


def _get_confirm_token(response: requests.Response) -> str:
    """Extract confirmation token from Google Drive response cookies.

    Args:
        response (requests.Response): Initial response from Google Drive.

    Returns:
        str: Confirmation token if found, otherwise None.
    """
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None


def _get_file_size(session: requests.Session, URL: str, params: dict) -> int:
    """Get file size by sending a range request to the server.

    Args:
        session (requests.Session): Current session.
        URL (str): URL for Google Drive download.
        params (dict): Request parameters.

    Returns:
        int: File size in bytes or None if not available.
    """
    response = session.get(URL, params=params, stream=True, headers={'Range': 'bytes=0-2'})
    if 'Content-Range' in response.headers:
        return int(response.headers['Content-Range'].split('/')[1])
    return None


def _save_response_content(response: requests.Response, destination: str, file_size: int = None, chunk_size: int = 32768) -> None:
    """Save the response content to the specified destination.

    Args:
        response (requests.Response): Response containing file content.
        destination (str): File path to save the content.
        file_size (int): Total file size in bytes, if known.
        chunk_size (int): Size of chunks to read from the response. Default is 32KB.
    """
    pbar = None
    if file_size:
        pbar = tqdm(total=math.ceil(file_size / chunk_size), unit='chunk')
        readable_file_size = format_size(file_size)

    with open(destination, 'wb') as f:
        downloaded_size = 0
        for chunk in response.iter_content(chunk_size):
            if chunk:  # Avoid keep-alive chunks
                f.write(chunk)
                downloaded_size += len(chunk)
                if pbar:
                    pbar.update(1)
                    pbar.set_description(f'Download {format_size(downloaded_size)} / {readable_file_size}')

    if pbar:
        pbar.close()


def load_file_from_url(url: str, model_dir: str = None, progress: bool = True, file_name: str = None) -> str:
    """Load a file from a URL, downloading it if necessary.

    Args:
        url (str): URL to download the file from.
        model_dir (str): Directory to save the file. Defaults to the PyTorch hub directory.
        progress (bool): Whether to show download progress. Default is True.
        file_name (str): Custom file name for the downloaded file. If None, the file name from the URL is used.

    Returns:
        str: Absolute path to the downloaded file.
    """
    if model_dir is None:
        hub_dir = get_dir()
        model_dir = os.path.join(hub_dir, 'checkpoints')

    os.makedirs(model_dir, exist_ok=True)

    parts = urlparse(url)
    filename = file_name if file_name else os.path.basename(parts.path)
    cached_file = os.path.abspath(os.path.join(model_dir, filename))

    if not os.path.exists(cached_file):
        print(f'Downloading: "{url}" to {cached_file}\n')
        download_url_to_file(url, cached_file, hash_prefix=None, progress=progress)

    return cached_file
