#!/usr/bin/env python
# coding: utf-8

import pytesseract as pyt
from IPython.display import display
try:
    from PIL import Image
except ImportError:
    import Image    
#pyt.pytesseract.tesseract_cmd = '/home/self/anaconda3/envs/work/bin/pytesseract'   
img = Image.open('/home/self/workspace/AAII/OCR/ocr-image.png')
txt = pyt.image_to_string(img, lang='asm+eng')
print("Image:")
display(img)
print("Text:")
print(txt)