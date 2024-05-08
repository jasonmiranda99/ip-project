import easyocr
import os

# Full path to the directory where you want to save the file
output_directory = "C:\\Users\\jason\\Documents\\VS Code Programs\\ip-project\\output"

# Create the directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

reader = easyocr.Reader(['en'])  # specify the language
result = reader.readtext(r"C:\Users\jason\Documents\VS Code Programs\ip-project\canvas\canvas.png")

# Open a text file in write mode, specifying the full path
output_file_path = os.path.join(output_directory, "detected_text.txt")
with open(output_file_path, 'w') as file:
    # Iterate through the detected text and write it to the file
    for (bbox, text, prob) in result:
        file.write(f'Text: {text}, Probability: {prob}\n')
