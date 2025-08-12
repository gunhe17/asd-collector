import os
from dotenv import load_dotenv

load_dotenv()


class SystemConfig():
    @property
    def OS(self):
        import platform
        return platform.system()
    
    @property
    def EXE_CALIBRATE(self):
        return os.getenv("EXE_CALIBRATE", "ASDcollector/usecase/bin/calibrator.exe")
    
    @property
    def EXE_CAPTURE(self):
        return os.getenv("EXE_CAPTURE", "ASDcollector/usecase/bin/syncorder.exe")
    
    @property
    def EXE_TEST(self):
        return os.getenv("EXE_TEST", "ASDcollector/usecase/bin/tester.exe")
    
    @property
    def EXE_CONVERT(self):
        return os.getenv("EXE_CONVERT", "C:/Users/insighter/workspace/sdk/realsense/tools/rs-convert.exe")
    

class DBConfig():
    @property
    def DB_PATH(self):
        return os.getenv("DB_PATH", "ASDcollector/db/db.json")
    
    @property
    def SOLUTION_PATH(self):
        return os.getenv("SOLUTION_PATH", "data/solution_videos")
    
    @property
    def COLLECTION_PATH(self):
        return os.getenv("COLLECTION_PATH",  "C:/Users/insighter/workspace/data")

class OpenAIConfig():
    @property
    def OPENAI_KEY(self):
        return os.getenv("OPENAI_KEY", "")
    
    @property
    def OPENAI_ORGANIZATION(self):
        return os.getenv("OPENAI_ORGANIZATION", "")
    
    @property
    def OPENAI_PROJECT(self):
        return os.getenv("OPENAI_PROJECT", "")
    
class CameraConfig():
    @property
    def CAM_COUNT(self):
        return os.getenv("CAM_COUNT", 1)

    @property
    def CAM_NO1_INDEX(self):
        return os.getenv("CAM_NO1_INDEX", 0)

    @property
    def CAM_NO2_INDEX(self):
        return os.getenv("CAM_NO2_INDEX", None)

    @property
    def CAM_NO3_INDEX(self):
        return os.getenv("CAM_NO3_INDEX", None)

    @property
    def CAM_NO4_INDEX(self):
        return os.getenv("CAM_NO4_INDEX", None)

    @property
    def CAM_NO5_INDEX(self):
        return os.getenv("CAM_NO5_INDEX", None)

    @property
    def CAM_NO6_INDEX(self):
        return os.getenv("CAM_NO6_INDEX", None)

    @property
    def INDEX_LIST(self):
        load_dotenv(override=True)

        indices = [
            self.CAM_NO1_INDEX,
            self.CAM_NO2_INDEX,
            self.CAM_NO3_INDEX,
            self.CAM_NO4_INDEX,
            self.CAM_NO5_INDEX,
            self.CAM_NO6_INDEX,
        ]
        return ",".join(
            str(int(i)) for i in indices if i not in (None, '', '-1')
        )