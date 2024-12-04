from PIL import Image, ImageDraw, ImageFont
from paddleocr import PaddleOCR, draw_ocr

ocr = PaddleOCR(use_angle_cls=True, lang='en')
image_path = "/content/card.png"
image = Image.open(image_path)
result = ocr.ocr(image_path)

#targeted word need to be added
target_word = {
    "M": "Amanuel Tekaling",
    "attending" : "2"
}

for line in result[0]:
  box, (detected_text, confidence) = line 
  detected_text_lower = detected_text.lower()
  if detected_text_lower in target_word:
    x, y = box[0]
    w = box[2][0] - box[0][0] 
    h = box[2][1] - box[0][1]
    new_txt_pst = (x + w + 10, y)
    new_word = target_word[detected_text_lower]
    draw.text(new_txt_pst, new_word, fill="red")

image = image.convert("RGB")
image.save("printed.jpg")
image.show()