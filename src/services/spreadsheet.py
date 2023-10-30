from googleapiclient.errors import HttpError
import schedule

class Spreadsheet:
  # ===============================================
  def __init__(self, service, spreadsheet_id, range):
    self.service = service
    self.range = range
    self.spreadsheetId = spreadsheet_id
    self.content = self.__get_content(self.spreadsheetId, self.range)

  # ===============================================
  def __get_content(self, spreadsheet_id, range):
    try:
      content = self.service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range).execute()
      values = content.get('values', [])
    except HttpError as error:
      print(error)
    return values  

  # ===============================================
  def __update_status(self, index):
    range = f"B{index+2}:B{index+3}"
    value = [[1]]
    try:
      self.service.spreadsheets().values().update(spreadsheetId=self.spreadsheetId, 
      range=range, valueInputOption="USER_ENTERED", body={'values': value}).execute()
      print('Status updated successfully!')
    except HttpError as error:
      print(error)

  # ===============================================
  def __reset_status(self): 
    array = [[0]]*13
    try:
      self.service.spreadsheets().values().update(spreadsheetId=self.spreadsheetId, 
      range="!B2:B14", valueInputOption="USER_ENTERED", body={'values': array}).execute()
      print('Status reseted sucefully!')
    except HttpError as error:
      print(error)

  # ===============================================
  #Retorna todos os emails
  def get_students(self):
    students = []
    content = self.content
    for person in content:
      students.append({'name': person[0],'email':person[2]})

    students.pop(0)
    return students

  # ===============================================
  #Retorna o horário da reunião
  def get_time(self):
    content = self.content
    time = content[1][4].split(":")
    hour = int(time[0])
    # hour -= 2 #Este parametro pode ser modificavel dependendo da regiao
    return f"{hour}:{time[1]}"

  # ===============================================
  def schedule_job(self, main):
    content = self.content
    day = content[1][5]
    print(f"Day: {day}")
    if(day == 'segunda-feira'):
      schedule.every().monday.at(self.get_time()).do(main)
    elif(day == 'terça-feira'):
      schedule.every().tuesday.at(self.get_time()).do(main)
    elif(day == 'quarta-feira'):
      schedule.every().wednesday.at(self.get_time()).do(main)
    elif(day == 'quinta-feira'):
      schedule.every().thursday.at(self.get_time()).do(main)
    elif(day == 'sexta-feira'):
      schedule.every().friday.at(self.get_time()).do(main)
    elif (day == "sábado"):
      schedule.every().saturday.at(self.get_time()).do(main)
    elif (day == "domingo"):
      schedule.every().sunday.at(self.get_time()).do(main)

  # ===============================================
  def get_todays_writer(self):
    matrix = self.content
    matrix.pop(0)

    for i,person in enumerate(matrix):
      #Caso a pessoa não esteja presente, pula para o próximo
      if int(person[3]) == 0:
        continue
      #Caso a pessoa não tenha preenchido a ata ainda
      if int(person[1]) == 0:
        name = person[0]
        self.__update_status(i)
        return name
    self.__reset_status()
    return self.get_todays_writer()
