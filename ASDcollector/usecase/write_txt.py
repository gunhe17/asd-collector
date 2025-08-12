from pathlib import Path

from ASDcollector.config import (
    DBConfig
)
from ASDcollector.repository.users import UserGet

db_config = DBConfig()

"""command"""

def write(
    user_id: str,
    db=Path(db_config.DB_PATH)
) -> bool:
    
    txt_path = Path(
        _output_path(
            user_id=user_id
        )
    )
    txt_path.parent.mkdir(parents=True, exist_ok=True)

    user = UserGet.get_by_id(db, id=user_id)
    if user is None:
            raise
    
    with open(txt_path, 'w', encoding='utf-8') as f:
        for key, value in user.items():
            f.write(f"{key}: {value}\n")

    return True


"""helper"""

def _output_path(user_id: str):
    base = f"{db_config.COLLECTION_PATH}/origin/{user_id}"

    return f"{base}/user.txt"