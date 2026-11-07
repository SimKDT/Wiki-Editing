import urllib.request
import urllib.error

def is_404(url: str) -> bool:
    try:
        with urllib.request.urlopen(url, timeout=10):
            return False
    except urllib.error.HTTPError as e:
        return e.code == 404
