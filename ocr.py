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

#assigning the extracted words to var
sender = separate("from","for")
reciever = separate("for","ETB")
transaction_id = separate("transaction","Total")
amount = separate("Amount","commission")
amount = amount[1:3]

print(sender)
print(reciever)
print(transaction_id)
print(amount)