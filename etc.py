from datetime import datetime
import hashlib


def get_iso_date() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()

def get_hash(ts: datetime) -> str:
    return hashlib.sha256(str(ts).encode()).hexdigest()