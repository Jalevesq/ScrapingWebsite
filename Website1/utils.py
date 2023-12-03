import os
from private import temporaryFolder, unfilteredFolder

def waitForPage(page):
    try:
        page.wait_for_load_state("networkidle", timeout=10000)
    except Exception as e:
        print(f"Wait_for_load_state error: {e}")
        return False
    return True


def checkTempFolder(file_path):
    temp_folder_path = os.path.join(file_path, temporaryFolder)
    if not os.path.exists(temp_folder_path):
        os.makedirs(temp_folder_path)
        print(f"Created '{temporaryFolder}' folder in {file_path}.")
    else:
        print(f"'{temporaryFolder}' folder already exists in {file_path}.")
    
def checkUnfilteredFolder(file_path):
    unfiltered_folder_path = os.path.join(file_path, unfilteredFolder)
    if not os.path.exists(unfiltered_folder_path):
        os.makedirs(unfiltered_folder_path)
        print(f"Created '{unfilteredFolder}' folder in {file_path}.")
    else:
        print(f"'{unfilteredFolder}' folder already exists in {file_path}.")

def checkFilePath(file_path):
    if os.path.exists(file_path) and os.path.isdir(file_path):
        print(f"Path {file_path} exists.")
        checkTempFolder(file_path)
        checkUnfilteredFolder(file_path)
        return True
    else:
        print(f"Path {file_path} does not exist.")
    return False