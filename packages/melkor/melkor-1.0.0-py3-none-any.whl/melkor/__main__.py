import argparse
import sys
import os
import importlib.metadata as metadata
import traceback


from gamuLogger import Logger, LEVELS

from .settings import Settings
from .engine import importFiles
from .customTypes import TestList
from .output.junit import Report as JunitReport

Logger.setModule("melkor")

def logPackageVersion():
    Logger.debug(f"Python version: {sys.version}")
    Logger.debug(f"gamuLogger version: {metadata.version('gamuLogger')}")
    Logger.debug(f"melkor version: {metadata.version('melkor')}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("configFile", help="Path to the configuration file")
    parser.add_argument("--debug", help="Enable debug mode", action="store_true")
    args = parser.parse_args()
    
    if args.debug:
        Logger.setLevel('stdout', LEVELS.DEBUG)
        
    logPackageVersion()
    
    Settings.setFilePath(args.configFile)
        
    testDir = Settings().get("testDir")
    if not os.path.exists(testDir):
        Logger.error(f"Test directory '{testDir}' not found")
        sys.exit(1)

    TestList.new(Settings().get("name"))

    files = [os.path.join(testDir, file) for file in os.listdir(testDir) if file.endswith(".py")]
    Logger.info(f"Found {len(files)} test files, loading them")
    modules = importFiles(files)
    
    Logger.info("Running tests")
    TestList.getInstance().run()
    
    Logger.info("Generating JUnit report")
    junitReport = JunitReport(TestList.getInstance())
    junitReport.save(Settings().get("outFile"))
    Logger.info(f"Report generated to {Settings().get('outFile')}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        Logger.debug(traceback.format_exc())
        Logger.critical(f"An exception occurred: {e}")
