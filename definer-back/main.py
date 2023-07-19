import cv2
import sys
import traceback
import uvicorn
import ujson
import numpy as np
from fastapi import FastAPI, File, UploadFile, Depends, Form
from typing import Dict, List

from nomeroff_net import pipeline
from nomeroff_net.tools import unzip
from uuid import UUID


number_plate_detection_and_reading = pipeline("number_plate_detection_and_reading")


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post('/define_from_bytes')
async def detect_from_bytes(id: UUID = Form(...), file: UploadFile = File(...)):

    try:
        nparr = np.frombuffer(await file.read(), np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        result = number_plate_detection_and_reading([image])
        (images, images_bboxs,
         images_points, images_zones, region_ids,
         region_names, count_lines,
         confidences, texts) = unzip(result)
        print(ujson.dumps(dict(res=texts)))
        return ujson.dumps(dict(res=texts))
    except Exception:
        return ujson.dumps({"error": "There was an error uploading the file(s)"})
    finally:
        file.file.close()


if __name__ == '__main__':
   uvicorn.run(app, host='127.0.0.1', port=8001)
