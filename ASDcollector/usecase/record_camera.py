from pathlib import Path
import subprocess
import threading
import signal
import re
import os

from ASDcollector.config import (
    DBConfig,
    SystemConfig,
)

db_config = DBConfig()
system_config = SystemConfig()


"""Helper"""

class ProcessManager:
    _processes: dict[str, subprocess.Popen] = {}
    
    @classmethod
    def add_process(cls, user_id: str, process: subprocess.Popen):
        cls._processes[user_id] = process
    
    @classmethod
    def get_process(cls, user_id: str) -> subprocess.Popen | None:
        return cls._processes.get(user_id)

    @classmethod
    def remove_process(cls, user_id: str):
        if user_id in cls._processes:
            del cls._processes[user_id]
    
    @classmethod
    def stop_process(cls, user_id: str) -> bool:
        process = cls.get_process(user_id)
        if not process:
            return False
            
        try:
            print(f"[Stop] Sending SIGINT to process {user_id}...")

            # FastAPI 보호 시작
            original_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
            
            try:
                os.kill(process.pid, signal.CTRL_C_EVENT)

                # 프로세스 종료 대기 (보호 상태 유지)
                try:
                    process.wait(timeout=10)
                    print(f"[Stop] Process {user_id} terminated gracefully")
                except subprocess.TimeoutExpired:
                    print(f"[Stop] Process {user_id} force killing...")
                    process.kill()
                    process.wait()
                    print(f"[Stop] Process {user_id} killed")
            
            finally:
                # 반드시 복원 (예외 발생해도)
                signal.signal(signal.SIGINT, original_handler)
                print(f"[Stop] FastAPI protection restored")

            cls.remove_process(user_id)
            return True

        except Exception as e:
            print(f"[Stop] Error: {e}")
            cls.remove_process(user_id)
            return False
        
        
process_manager = ProcessManager()


##
# Usecase

def record(
    video_id: int, 
    user_id: str,
    db=Path(db_config.DB_PATH),
) -> bool:
    
    print("IS CALLED")
    
    # Skip
    if system_config.OS != "Windows": 
        return True
    
    record_duration: int = (
        5 + # wait(start)
        5 + # wait(end)
        _record_duration(video_id=video_id) 
    )
    print("record duration: ", record_duration)

    output_path = _output_path(
        user_id
    )

    calibration_path = _calibration_path(
        user_id
    )

    process_args = [
        system_config.EXE_CAPTURE,
        "--record_duration", f"{record_duration}",
        "--output_path", f"{output_path}",
    ]
    if calibration_path:
        process_args += ["--calibration_path", calibration_path]
        print("::CALIBRATION")

    process = subprocess.Popen(
        process_args,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )

    _realtime_monitor(
        process
    )

    process_manager.add_process(
        user_id, 
        process
    )

    return True

def stop(user_id: str) -> bool:
    return process_manager.stop_process(user_id)

montitor = {'realsense': 0, 'tobii': 0}
def monitor() -> dict:
    return montitor


"""private"""

def _record_duration(video_id):
    from ASDcollector.repository.solutions import SolutionGet
    solutions = SolutionGet.get_all(
        db=Path(db_config.DB_PATH)
    )
    
    videos = [
        s for s in solutions if s['id'] >= video_id
    ]

    if (video_id < 2):
        videos += [
            {
                "name": "attention index-2", 
                "duration": 5 + 5
            }
        ]

    if (video_id < 9):
        videos += [
            {   
                "name": "attention index-9",
                "duration": 1 + 5
            }
        ]
    
    durations = [
        int(v['duration']) for v in videos
    ]
    
    return sum(durations)

def _output_path(user_id: str):
    base = f"{db_config.COLLECTION_PATH}/origin/{user_id}"

    dir = Path(base)
    if not dir.exists():
        return f"{base}/session_1_"

    indices = [
        int(m.group(1))
        for d in dir.iterdir()
        if d.is_dir() and (m := re.match(r"session_(\d+)_", d.name))
    ]

    return f"{base}/session_{max(indices, default=0) + 1}_"

def _calibration_path(user_id: str):
    path = Path(f"{db_config.COLLECTION_PATH}/origin/{user_id}/calibration_result.bin")
    
    if path.exists():
        return str(path)
    
    return False

def _realtime_monitor(process: subprocess.Popen):
    def _read():
        try:
            while True:
                line = process.stdout.readline() #type: ignore
                if not line: break

                if "LOG|" in line and "|FRAME|SUCCESS" in line:
                    if "REALSENSE" in line:
                        montitor['realsense'] += 1
                    if "TOBII" in line:
                        montitor['tobii'] += 1
        except Exception as e:
            print()
        finally:
            process.stdout.close() #type: ignore

    monitor_thread = threading.Thread(target=_read, daemon=True)
    monitor_thread.start()


"""CLI"""

def get_arguments():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--video_id", type=int, required=False)
    parser.add_argument("--user_id", type=str, required=False)

    args = parser.parse_args()

    return args

def main():
    args = get_arguments()

    record(
        args.video_id,
        args.user_id
    )

if __name__ == "__main__":
    main()