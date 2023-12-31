from googleapiclient.errors import HttpError
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()
SHARED_DRIVE_ID = os.getenv("SHARED_DRIVE_ID")

MONTHS_PORTUGUESE = {
 1: 'Janeiro',
 2: 'Fevereiro',
 3: 'Março',
 4: 'Maio',
 5: 'Abril',
 6: 'Junho',
 7: 'Julho',
 8: 'Agosto',
 9: 'Setembro',
 10: 'Outubro',
 11: 'Novembro',
 12: 'Dezembro'
}

class Drive:
    # ===============================================
    def __init__(self, service):
        self.service = service

    # ===============================================
    def copy_weekly_ata(self, main_folder_id):
        today = datetime.now()
        currrent_date = today.strftime("%d/%m/%Y")

        folders = self.get_folders_inside(main_folder_id)
        if folders == None: 
            # print("[ERROR]: no folders found on ata folder directory!")
            exit(1)

        save_file_folder_id = folders[MONTHS_PORTUGUESE[today.month]]
        ata_id = self.get_ata_id(main_folder_id)

        link = self.copy_file_into(ata_id, save_file_folder_id , currrent_date)
        return link

    # ===============================================
    def copy_file_into(self, fileId, folderId, new_name):
        # print(f'fileId: {fileId}')
        reqBody = { 'parents': [ folderId ], 'name': new_name }

        try:
            result = self.service.files().copy(
                    supportsAllDrives=True,
                    fileId=fileId, 
                    body=reqBody,
                    fields='webViewLink'
            ).execute()
            print("New ata created successfully!\n")
            link = result['webViewLink']
            # print(f"Copied file link: {link}")
            return link
        except HttpError as error:
            print(f'An error occurred: {error}')
        
    # ===============================================
    def get_ata_id(self, folder_id): 
        query = f"'{folder_id}' in parents"
        try:
            results = self.service.files().list(
                    pageSize=20,
                    q=query,
                    driveId=SHARED_DRIVE_ID,
                    includeItemsFromAllDrives=True,
                    supportsAllDrives=True,
                    corpora='drive'
            ).execute()

            items = results.get('files', [])

            if not items:
                print('No files found.')
                return
            for item in items:
                if item['name'] == 'Modelo Ata':
                    print(f"-> Ata model found!")
                    return item['id']
            exit('Ata not found!')
        except HttpError as error:
            print(error)
    
    # ===============================================
    def get_folders_inside(self, folder_id):    
        query = f"mimeType = 'application/vnd.google-apps.folder' and '{folder_id}' in parents"
        try:
            results = self.service.files().list(
                    pageSize=20,
                    q=query,
                    driveId=SHARED_DRIVE_ID,
                    includeItemsFromAllDrives=True,
                    supportsAllDrives=True,
                    corpora='drive'
            ).execute()
            folders = results.get('files', [])
            foldersDictionary = {}

            if not folders:
                print('No folders found.')
                return
            for folder in folders:
                foldersDictionary[folder['name']] = folder['id']
            return foldersDictionary

        except HttpError as error:
            print(error)
