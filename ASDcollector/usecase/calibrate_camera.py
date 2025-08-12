from pathlib import Path
import subprocess

from ASDcollector.config import (
    DBConfig,
    SystemConfig,
)

db_config = DBConfig()
system_config = SystemConfig()


"""Commnad"""

def calibrate(
    user_id: str,
    db=Path(db_config.DB_PATH)
) -> bool:
    
    # Skip
    if system_config.OS != "Windows": 
        return True
    
    output_path = _output_path(
        user_id
    )
    
    process = subprocess.Popen(
        [
            system_config.EXE_CALIBRATE,
            "--output_path", f"{output_path}",
        ],
        stdin=subprocess.PIPE,
        # stdout=subprocess.PIPE,
        # stderr=subprocess.PIPE,
        text=True,
    )

    return True


def delete(
    user_id: str
) -> bool:

    # Skip
    if system_config.OS != "Windows": 
        return True
    
    output_path = _output_path(
        user_id
    )
    
    calibration_log = Path(output_path) / "calibration_log.txt"
    if calibration_log.exists(): calibration_log.unlink()
        
    calibration_result = Path(output_path) / "calibration_result.bin"
    if calibration_result.exists(): calibration_result.unlink()

    return True


def calibrate_test(
    user_id: str
) -> bool:
    
    # Skip
    if system_config.OS != "Windows": 
        return True

    calibration_path = _calibration_path(
        user_id
    )

    process_args = [
        system_config.EXE_TEST,
        "--calibration_path", calibration_path
    ]
    
    process = subprocess.Popen(
        process_args,
        stdin=subprocess.PIPE,
        # stdout=subprocess.PIPE,
        # stderr=subprocess.PIPE,
        text=True,
    )

    return True


"""private"""

def _output_path(user_id: str):
    base = f"{db_config.COLLECTION_PATH}/origin/{user_id}"

    dir = Path(base)
    
    if not dir.exists():
        dir.mkdir(parents=True)

    return f"{base}"

def _calibration_path(user_id: str):
    path = Path(f"{db_config.COLLECTION_PATH}/origin/{user_id}/calibration_result.bin")
    
    if path.exists():
        return str(path)
    
    return False