import cv2
import sys
import traceback

import numpy
import uvicorn
import ujson
import numpy as np
from fastapi import FastAPI, File, UploadFile, Depends, Form
from typing import Dict, List

from starlette.responses import JSONResponse

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
        results = number_plate_detection_and_reading([image])
        (images, images_bboxs,
         images_points, images_zones, region_ids,
         region_names, count_lines,
         confidences, texts) = unzip(results)
        image_point, text = images_points[0], texts[0]
        if len(image_point):
            lb_x, lb_y = image_point[0][0]
            # rb_x, rb_y = image_point[0][1]
            rt_x, rt_y = image_point[0][2]
            # lt_x, lt_y = image_point[0][3]
            result = {
                "lb_x": int(lb_x), "lb_y": int(lb_y),
                "rt_x": int(rt_x), "rt_y": int(rt_y),
                "text": text[0]
            }
        else:
            result = {}
        return JSONResponse(content=result)
    except ValueError:
        return ujson.dumps({"error": "There was an error uploading the file(s)"})
    finally:
        file.file.close()


if __name__ == '__main__':
   uvicorn.run(app, host='127.0.0.1', port=8001)
