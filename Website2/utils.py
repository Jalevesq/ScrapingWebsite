import datetime, os

def getDate() -> str:
    today_date: datetime.date = datetime.date.today()
    return today_date.strftime("%Y-%m-%d")

def waitForPage(page):
    try:
        page.wait_for_load_state("networkidle", timeout=10000)
    except Exception as e:
        print(f"Wait_for_load_state error: {e}")
        return False
    return True


def checkFilePath(file_path):
    if os.path.exists(file_path) and os.path.isdir(file_path):
        print(f"Path {file_path} exists.")
        temp_folder_path = os.path.join(file_path, "temp")
        if not os.path.exists(temp_folder_path):
            os.makedirs(temp_folder_path)
            print(f"Created 'temp' folder in {file_path}.")
        else:
            print(f"'temp' folder already exists in {file_path}.")
        return True
    else:
        print(f"Path {file_path} does not exist.")
    return False