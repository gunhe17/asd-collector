from pathlib import Path
import os

from ASDcollector.config import DBConfig
from ASDcollector.repository.solutions import SolutionGet

db_config=DBConfig()


"""Command"""

"""Query"""

def get_by_id(
    video_id: str,
    db=Path(db_config.DB_PATH),
) -> dict:
    
    solution = SolutionGet.get_by_id(
        db, 
        id=video_id
    )
    if solution is None:
        raise
    
    return solution

def get_video_by_id(
    video_id: str,
    db=Path(db_config.DB_PATH),
) -> str:
    
    solution = get_by_id(
        video_id=video_id
    )
    if solution is None:
        raise ValueError()

    path = solution.get("path", None)
    if path is None:
        raise ValueError()

    if not os.path.exists(path):
        raise ValueError()
    
    if os.path.getsize(path) == 0:
        raise ValueError()
    
    return path

def get_all(
    db=Path(db_config.DB_PATH),
) -> list[dict]:
    
    solutions = SolutionGet.get_all(
        db,
    )
    if solutions is None:
        raise ValueError()

    return solutions