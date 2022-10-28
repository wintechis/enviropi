from datetime import datetime
import hashlib
import os

def get_iso_date() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()

def get_hash(ts: datetime) -> str:
    return hashlib.sha256(str(ts).encode()).hexdigest()


##################################################
## Store directory to file path folder as global var
FILES = os.path.join(os.path.dirname(__file__), 'files')
REQUESTS = os.path.join(os.path.dirname(__file__), 'requests')

