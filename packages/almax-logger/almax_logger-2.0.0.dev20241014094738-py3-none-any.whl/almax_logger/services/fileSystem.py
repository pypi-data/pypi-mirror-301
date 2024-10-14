import logging;
import os;
from tools import utils;

class FileSystemLog:
    def __init__(self, programNameLogger: str, details: str = '', genericLogFileName: str = "__0.ExecutionLog.log", addTimeFolder: bool = True, logFormat: str = '%(asctime)s - %(message)s', absoluteLogPath: str = ''):
        self.__LogPath = f"{absoluteLogPath}{programNameLogger}{details}";
       
        #if os.path.exists(self.__LogPath):
        #    raise FileExistsError("Duplicate Executions are Denied!");
        #else:
        if addTimeFolder:
            self.__LogPath += "/" + utils.now().strftime("%Y%m%d_%H%M%S");
        if not (os.path.exists(self.__LogPath)):
            os.makedirs(self.__LogPath);
       
        self.__Istance = logging.getLogger(programNameLogger + details);
        self.file_handler = logging.FileHandler(filename=f"{self.__LogPath}/{genericLogFileName}", mode='a');
        self.formatter = logging.Formatter(logFormat);
        self.file_handler.setFormatter(self.formatter);
        self.__Istance.addHandler(self.file_handler);
        self.__Istance.setLevel(logging.INFO);
       
        self.__CustomTimer = utils.now();
        self.__Timer = utils.now();
   
    def AddLog(self, message):
        self.__Istance.info(message);

    def StartTiming(self, message):
        self.__Istance.info(message);
        self.__CustomTimer = utils.now();

    def EndTiming(self):
        self.__Istance.info(f"\tDuration: {utils.TimeToString(utils.CalculateTimePassed(self.__CustomTimer))}");
   
    def StartGenericTiming(self):
        self.__Timer = utils.now();

    def ForceEnd(self):
        self.__Istance.info(f"Total Duration: {utils.TimeToString(utils.CalculateTimePassed(self.__Timer))}");
        self.__Istance.info(f"FORCED END\n\n");

    def Start(self):
        self.__Istance.info(f"START");

    def End(self):
        self.__Istance.info(f"Total Duration: {utils.TimeToString(utils.CalculateTimePassed(self.__Timer))}");
        self.__Istance.info(f"END\n\n");

    def LogPath(self) -> str:
        return self.__LogPath;