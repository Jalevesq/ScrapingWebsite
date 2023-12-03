import os

def waitForPage(page):
    try:
        page.wait_for_load_state("networkidle", timeout=10000)
    except Exception as e:
        print(f"Wait_for_load_state error: {e}")
        return False
    return True


def checkTempFolder(file_path):
    temp_folder_path = os.path.join(file_path, "temp")
    if not os.path.exists(temp_folder_path):
        os.makedirs(temp_folder_path)
        print(f"Created 'temp' folder in {file_path}.")
    else:
        print(f"'temp' folder already exists in {file_path}.")
    
def checkUnfilteredFolder(file_path):
    unfiltered_folder_path = os.path.join(file_path, "unfiltered")
    if not os.path.exists(unfiltered_folder_path):
        os.makedirs(unfiltered_folder_path)
        print(f"Created 'unfiltered' folder in {file_path}.")
    else:
        print(f"'unfiltered' folder already exists in {file_path}.")

def checkFilePath(file_path):
    if os.path.exists(file_path) and os.path.isdir(file_path):
        print(f"Path {file_path} exists.")
        checkTempFolder(file_path)
        checkUnfilteredFolder(file_path)
        return True
    else:
        print(f"Path {file_path} does not exist.")
    return False