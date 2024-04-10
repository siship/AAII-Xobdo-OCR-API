import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel

import pytesseract as pyt
from IPython.display import display

import os
import datetime
import pathlib
import sys

try:
    from PIL import Image
except ImportError:
    import Image    


from fastapi.middleware.cors import CORSMiddleware

import logging

logger = logging.getLogger(__name__)
log_formatter = logging.Formatter("%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s")
stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler('app.log')
stream_handler.setFormatter(log_formatter)
file_handler.setFormatter(log_formatter)
logger.handlers = [stream_handler, file_handler]

logger.setLevel(logging.INFO)
time_now = datetime.datetime.now()
logger.info(f"API is starting up at: {time_now}")

app= FastAPI(title='api')

# Please update the following - Sishir - 10.04-2024
origins = [
    "https://.*\.xobdo.org",
    "https://reqbin.com",  #this is for API testing
    "http://0.0.0.0:5555"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def ocr_infer(infile_image):

    filename_temp = datetime.datetime.now().strftime('%Y-%m-%d_%H_%S_%f')
    folder_name = datetime.datetime.now().strftime('%Y-%m-%d_%H')
    pathlib.Path('image_dir/'+folder_name).mkdir(parents=True,exist_ok=True)

    outfile_image = 'image_dir/'+folder_name+'/'+filename_temp+'.png'
    outfile_txt = 'image_dir/'+folder_name+'/'+filename_temp+'.txt'

    command_convert_image = 'convert -density 300 {} -depth 8 -strip -background white {}'.format(infile_image, outfile_image)

    os.system(command_convert_image)
    img = Image.open(outfile_image)
    txt = pyt.image_to_string(img, lang='asm+eng')

    with open(outfile_txt, "w+") as text_file:
        text_file.write(txt)
    logger.info(f"Processing complete for {infile_image}")
    return outfile_txt


@app.route('/')
def index():
    return 'Xobdo-AAII Assamese OCR'

class xobdo_ocr_details(BaseModel):
    path : str

@app.post('/ocrxobdoaaii')
async def ocrxobdoaaii(xobdo_ocr : xobdo_ocr_details):

    image = xobdo_ocr.path

    extension = image.split(".")[-1].lower()

    time_now = datetime.datetime.now()
    logger.info(f"Received image for conversion--> {image} at {time_now}")

    if extension not in ("jpg", "jpeg", "png", "tiff"):
        logger.error("Unsupported image type attempted to be uploaded.")
        raise HTTPException(status_code=400, detail="Unsupported file type.")

    try:
        output_txt = ocr_infer(image)
        logger.info(f"Image {image} uploaded and processed successfully.")
        return { 'status_num' : '1', 'status_string':'success', 'synthesize_audio_file': output_txt}

    except Exception as e:
        print("Caught exception: %s" % repr(e))
        string = "Caught exception: %s" % repr(e)
        logger.exception(f"Error processing image {image}: {str(e)}")
        #raise HTTPException(status_code=500, detail=str(e))
        return { 'status_num' : '0', 'status_string': string}

if __name__=="__main__":    	    
     uvicorn.run("main_fastapi_log:app", host="0.0.0.0", port=5555, workers=1)
