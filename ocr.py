from paddleocr import PaddleOCR, draw_ocr
import gspread
from google.oauth2.service_account import Credentials
import re

SERVICE_ACCOUNT_FILE = '/content/ocr-443522-26fb8021aad9.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
gc = gspread.authorize(credentials)
sheet_url = 'https://docs.google.com/spreadsheets/d/1H3yj08wdZdHulyWeExMtuO8lhwjq9R2VQgbAvlK7ygA/edit?usp=sharing'
sheet = gc.open_by_url(sheet_url)
worksheet = sheet.sheet1

def is_valid_sheet(sheet, sheet_name):
  sheet_titles = [worksheet.title for worksheet in sheet.worksheets()]
  return sheet_name in sheet_titles

sheet_name = "user credentials"
if not is_valid_sheet(sheet, sheet_name):
  sheet.add_worksheet(title=sheet_name, rows=100, cols=26)

def is_valid_email(email):
    #defines a pattern for a valid email
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    #Check if the pattern match or not
    return re.match(pattern, email) is not None

def password_strength(password):
    length_rule = len(password) >= 8
    uppercase_rule = bool(re.search(r'[A-Z]', password))
    lowercase_rule = bool(re.search(r'[a-z]', password))
    digit_rule = bool(re.search(r'[0-9]', password))
    special_char_rule = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))

    if all([length_rule,uppercase_rule, lowercase_rule, digit_rule, special_char_rule]):
        return "Strong password!"
    elif length_rule and (uppercase_rule or lowercase_rule) and (digit_rule or special_char_rule):
        return "moderate password!"
    else:
        return "weak password!"

while True:
    user_type = input("Are you new user? (y/n): ")
    if user_type.isdigit():
        print("please respond with y/n only")
        continue
    elif user_type.lower() == "y" or user_type.lower() == "n":
        break
    else:
        print("please respond with y/n only")
        continue

def user_acess():
    if user_type.lower() == "y":
        username = input("please input your email address: ")
        while True:
            if is_valid_email(username):
                break
            else:
                print("The email address is invalid.")
            username = input("Please provide a valid email address: ")

        while True:

            password = input("please creat your password: ")
            strength = password_strength(password)
            if strength == "weak password!" or strength == "moderate password!" :
                print(strength)
                print("character must contain atleast one capital letter, small letter, number and special character.")
                continue
            password1 = input("please conform your password: ")
            if password == password1:
              while True:
                user = input("Username: ")
                if not is_valid_sheet(sheet, user):
                  sheet.add_worksheet(title=user, rows=100, cols=26)
                  print("you have signed up sucessfuly!")
                  break
                else:
                  print("Username already taken!")
                #append password and email address

                #add a new sheet

              break
            else:
                    print("Password doesn't match correctly")

    else:
        username = input("input your email address to signin: ")
        password = input("input your password: ")
user_acess()

# Initialize the OCR model
ocr = PaddleOCR(use_angle_cls=True, lang='en')

# Specify the image path
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


