import re
import cv2
from pathlib import Path

from ASDcollector.config import DBConfig
from ASDcollector.repository.solutions import (
    SolutionCreate,
    Solution
)

db_config=DBConfig()


def natural_sort_key(path):
    return [
        int(text) if text.isdigit() else text.lower() 
        for text in re.split(r'(\d+)', str(path))
    ]

def create(
    db=Path(db_config.DB_PATH)
) -> list[dict]:

    video_index = 0
    solutions = []

    # 자연 정렬 적용
    video_files = sorted(
        Path(db_config.SOLUTION_PATH).rglob("*.mp4"),
        key=natural_sort_key
    )
    
    for v in video_files:
        video_index += 1
        video_path = str(v)
        video_duration, video_frame_count = _detail(str(video_path))
        solutions.append(
            Solution.from_dict({
                "id": video_index,
                "path": video_path,
                "duration": video_duration,
                "frames": video_frame_count,
            })
        )
    
    created = SolutionCreate.multi(
        db,
        solutions=solutions
    )
    
    return created


"""private"""

def _detail(video_path: str) -> tuple:
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None, None
    
    frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = frames / fps if fps > 0 else None
    
    cap.release()

    return duration, frames


"""CLI"""

def main():
    create()

if __name__ == "__main__":
    main()