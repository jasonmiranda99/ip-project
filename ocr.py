import easyocr

reader = easyocr.Reader(['en']) # specify the language
result = reader.readtext('image.jpg')

for (bbox, text, prob) in result:d
    print(f'Text: {text}, Probability: {prob}')