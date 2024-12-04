from paddleocr import PaddleOCR, draw_ocr
import gspread
from google.oauth2.service_account import Credentials


SERVICE_ACCOUNT_FILE = '/content/ocr-443522-26fb8021aad9.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
gc = gspread.authorize(credentials)
sheet_url = 'https://docs.google.com/spreadsheets/d/1H3yj08wdZdHulyWeExMtuO8lhwjq9R2VQgbAvlK7ygA/edit?usp=sharing'
sheet = gc.open_by_url(sheet_url)
worksheet = sheet.sheet1

# Initialize the OCR model
ocr = PaddleOCR(use_angle_cls=True, lang='en')


image_path = '/content/cbe.jpg'

# Perform OCR
result = ocr.ocr(image_path)

# function to extract words from string
def separate(start,end):
  start_index= recognized_text.index(start) + 1
  end_index= recognized_text.index(end)
  extracted_data = recognized_text[start_index:end_index]
  return extracted_data

# Print the recognized text
recognized_text = " ".join(line[1][0] for line in result[0]).split(' ')
date = separate("on", "transaction")
date = date[0:1]
recognized_text = [sub_word for word in recognized_text for sub_word in word.split('-')]
recognized_text = [sub_word for word in recognized_text for sub_word in word.split('.')]



sender = separate("from","for")
receiver = separate("for","transaction")
receiver = receiver[0:3]
transaction_id = separate("transaction","Total")
amount = separate("Amount","commission")
amount = amount[1:3]

data_row = {
    "Sender": " ".join(sender),
    "receiver": " ".join(receiver),
    "Transaction ID": transaction_id[0],
    "Amount": " ".join(amount),
    "Date": " ".join(date)
}

all_rows = worksheet.get_all_values()
if len(all_rows) == 0 or all_rows[0] != ["Sender", "Receiver", "Transaction ID", "Amount", "Date"]:
    worksheet.insert_row(["Sender", "Receiver", "Transaction ID", "Amount", "Date"], 1)

transaction_ids = worksheet.col_values(3)
if data_row["Transaction ID"] not in transaction_ids:

  worksheet.append_row([
      data_row["Sender"],
      data_row["receiver"],
      data_row["Transaction ID"],
      data_row["Amount"],
      data_row["Date"]
    ])
  print("Data successfully saved to Google Sheets!")

else:
  print(f"Transaction ID {data_row['Transaction ID']} already exists in the sheet.")
