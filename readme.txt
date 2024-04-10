sudo apt install imagemagick
pip install pytesseract
sudo cp asm.traineddata /usr/share/tesseract-ocr/4.00/tessdata

pip install datetime \
		gdown==4.4.0 \
		typeguard==2.13.3 \
		uvicorn \
                fastapi \
                pydantic \
                python-multipart
                
python main_fastapi_log.py
