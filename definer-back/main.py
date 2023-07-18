import cv2
import sys
import traceback
import uvicorn
import ujson
import numpy as np
from fastapi import FastAPI, File, UploadFile
from typing import Dict, List

from nomeroff_net import pipeline
from nomeroff_net.tools import unzip

number_plate_detection_and_reading = pipeline("number_plate_detection_and_reading")


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post('/detect_from_bytes')
def detect_from_bytes(files: List[UploadFile] = File(...)):
    images = []
    for file in files:
        try:
            img = cv2.imdecode(np.frombuffer(file.file.read(), dtype=np.uint8), 1)
            images.append(img[:, :, ::-1])
        except Exception:
            return ujson.dumps({"error": "There was an error uploading the file(s)"})
        finally:
            file.file.close()
    try:
        result = number_plate_detection_and_reading(images)
        (images, images_bboxs,
         images_points, images_zones, region_ids,
         region_names, count_lines,
         confidences, texts) = unzip(result)
        return ujson.dumps(dict(res=texts))
    except Exception as e:
        exc_type, exc_value, exc_tb = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_tb)
        return ujson.dumps(dict(error=str(e)))


if __name__ == '__main__':
   uvicorn.run(app, host='127.0.0.1', port=8001)
