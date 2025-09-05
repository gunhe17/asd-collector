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