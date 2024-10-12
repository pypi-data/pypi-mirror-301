import os
from pathlib import Path
from typing import Optional

from qcloud_cos import CosConfig, CosS3Client

cos_secret_id = os.environ.get("COS_SECRET_ID")
cos_secret_key = os.environ.get("COS_SECRET_KEY")
cos_region = os.environ.get("COS_REGION")
cos_bucket = os.environ.get("COS_BUCKET")
cos_config = CosConfig(Region=cos_region, SecretId=cos_secret_id, SecretKey=cos_secret_key)
cos_client = CosS3Client(cos_config)

cos_local = Path("/cos")


def get_local_path(key: str) -> Path:
    path = cos_local / key
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def download_cos_file(key: str, dest: Path = None) -> Optional[Path]:
    if dest:
        dest.parent.mkdir(parents=True, exist_ok=True)
    else:
        dest = get_local_path(key)
    if key is None:
        return None
    if not dest.exists():
        cos_client.download_file(Bucket=cos_bucket, Key=key, DestFilePath=dest)
    return dest


def upload_cos_file(key: str):
    cos_client.upload_file(Bucket=cos_bucket, Key=key, LocalFilePath=get_local_path(key))
