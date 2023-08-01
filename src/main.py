from services.authentication import Authentication
from services.spreadsheet import Spreadsheet
from services.email import send_emails
from services.drive import Drive
from dotenv import load_dotenv
from datetime import datetime
import schedule
import time
import os

load_dotenv()
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
CREDENTIALS_PATH =  './src/credentials/credentials.json'
TOKEN_PATH = './src/credentials/token.json' 

# ===============================================
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
RANGE = "!A1:F20"

# ===============================================
ATA_MAIN_FOLDER_ID = os.getenv("ATA_MAIN_FOLDER_ID")
SENDER_MAIL = os.getenv("SENDER_MAIL")

# ===============================================
drive_service, spread_service = Authentication(TOKEN_PATH, CREDENTIALS_PATH, SCOPES).get_services()
drive = Drive(drive_service)
spreadsheet = Spreadsheet(spread_service, SPREADSHEET_ID, RANGE)

def main():
    print("Release time:", release_time)
    print("Current time:", current_time)
    
    print("Running script!")
    ata_link = drive.copy_weekly_ata(ATA_MAIN_FOLDER_ID)
    students = spreadsheet.get_students()
    # ===============================================
    writer_name = spreadsheet.get_todays_writer()
    send_emails(students, writer_name, ata_link, SENDER_MAIL)
    print('-> All done!')

if __name__ == '__main__':
    # ===============================================s
    release_time = spreadsheet.get_time()
    print("Release time:", release_time)

    # ===============================================
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current time:", current_time)
    
    # ===============================================
    spreadsheet.schedule_job(main)    
    while True:
        schedule.run_pending()
        time.sleep(5)
