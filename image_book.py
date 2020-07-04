import minecart              #extracts images from pdf
import pytesseract           #open source ocr library
import numpy as np           #numpy to convert PIL image to numpy array for opencv
import cv2 as cv             #opencv for image processing
import re                    #regular expression
import json                  #for outputting in a json file
from tqdm import tqdm        #just for a fancy progess bar as this program takes time for execution
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'   #I am on windows so my installed tessaract filepath
pdffile = open('HSSC GK PREVIOUS QUESTIONS.pdf', 'rb')
doc = minecart.Document(pdffile)

#getting images
images=[]
print("iterating through all pages")
for page in doc.iter_pages():
    im = page.images[0].as_pil()  # requires pillow
    images.append(im)
complete_text=''

pdffile.close()
print("processing"+str(len(images))+"images")
for image in tqdm(images):    #here tqdm(images) gives a progress bar
    image=np.array(image)
    image=cv.cvtColor(image,cv.COLOR_RGB2GRAY)
    image = cv.resize(image, None, fx=2, fy=2, interpolation=cv.INTER_CUBIC)
    retval, threshold = cv.threshold(image,127,255,cv.THRESH_BINARY)
    text = pytesseract.image_to_string(threshold)
    complete_text=complete_text+text

print("pattern finding")
complete_text=complete_text.replace("\n","")
regx=r'(Q[\d]+\.[’‘\sa-zA-Z\-\(\),\'\x21-\x2F\x3A-\x40\x5B-\x60\x7B-\x7E]+)\(a\)([’‘\sa-zA-Z\-\(\),\'\x21-\x2F\x3A-\x40\x5B-\x60\x7B-\x7E]+)\(b\)([’‘\sa-zA-Z\-\(\),\'\x21-\x2F\x3A-\x40\x5B-\x60\x7B-\x7E]+)\(c\)([’‘\sa-zA-Z\-\(\),\'\x21-\x2F\x3A-\x40\x5B-\x60\x7B-\x7E]+)\(d\)([’‘\sa-zA-Z\-\(\),\'\x21-\x2F\x3A-\x40\x5B-\x60\x7B-\x7E]+)Ans:([\sa-d\-\(\),\'\x21-\x2F\x3A-\x40\x5B-\x60\x7B-\x7E]+\))'
questions_list=re.findall(regx,complete_text)
questions_list=[list(item) for item in questions_list]

print("outputing a JSON")
to_json=[]
for i in questions_list:
    if len(i[5])>4:
        i[5]=i[5][:-3]+i[5][-2:]
    to_json.append({'question':i[0],'option1':i[1],'option2':i[2],'option3':i[3],'option4':i[4],'answer':i[5]})
with open("book.json",'w') as file:
    json.dump(to_json,file,indent=4)
