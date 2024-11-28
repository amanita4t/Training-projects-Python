from paddleocr import PaddleOCR, draw_ocr

# Initialize the OCR model
ocr = PaddleOCR(use_angle_cls=True, lang='en')

# Specify the image path
image_path = 'imagepath'

# Perform OCR
result = ocr.ocr(image_path)

# Print the recognized text
recognized_text = " ".join(line[1][0] for line in result[0]).split(' ')
recognized_text = [sub_word for word in recognized_text for sub_word in word.split('-')]
recognized_text = [sub_word for word in recognized_text for sub_word in word.split('.')]

# function to extract words from string
def separate(start,end):
  start_index= recognized_text.index(start) + 1
  end_index= recognized_text.index(end)
  extracted_data = recognized_text[start_index:end_index]
  return extracted_data

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
    "Amount": " ".join(amount)
}

csv_file = 'transaction_data.csv'

file_exists = os.path.isfile(csv_file)

try:
  with open(csv_file, 'r') as file:
    is_file_empty = False
except FileNotFoundError:
    is_file_empty = True

with open(csv_file, mode = 'a', newline='', encoding='utf-8') as file:
    writer= csv.DictWriter(file, fieldnames= ["Sender", "receiver", "Transaction ID", "Amount"])
    if not file_exists or file.tell() == 0:
        writer.writeheader()

    writer.writerow(data_row)