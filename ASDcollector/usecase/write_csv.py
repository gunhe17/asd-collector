from pathlib import Path

from ASDcollector.config import (
    DBConfig
)

db_config = DBConfig()

"""command"""

def write(
    user_id: str,
    time: str,
    type: str,
    video_id: str,
) -> bool:
    
    csv_path = Path(
        _output_path(
            user_id=user_id
        )
    )
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    if not csv_path.exists():
        with csv_path.open("w", encoding="utf-8") as f:
            f.write("user_id,time,type,video_id\n")

    with csv_path.open("a", encoding="utf-8") as f:
        f.write(f"{user_id},{time},{type},{video_id}\n")

    return True


"""helper"""

def _output_path(user_id: str):
    base = f"{db_config.COLLECTION_PATH}/origin/{user_id}"

    return f"{base}/play.csv"