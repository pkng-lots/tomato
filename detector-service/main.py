from uuid import UUID, uuid4

import numpy
import requests
from ultralytics import YOLO
from typing import List
import cv2
import json
import logging

KEYCODE_ESCAPE = 27
LESS_AREA_COLOR = (0, 0, 255)
MIN_AREA_COLOR = (0, 255, 0)

CONTENT_TYPE = 'image/jpeg'
HEADERS = {'content-type': CONTENT_TYPE}

model = YOLO("yolov8n.pt")


def convert_image_to_bytes(image: numpy.array) -> bytes:
    _, encoded = cv2.imencode(".jpg", image)
    return encoded.tobytes()


def post_cropped_frame(url: str, frame: numpy.array, box: list, id: UUID) -> None:
    try:
        cropped = frame[box[1]: box[3], box[0]: box[2]]
        response = requests.post(
            url,
            data={"id": str(id)},
            files={"file": convert_image_to_bytes(cropped)},
        )
        print(
            json.dumps(response.json(), indent=2)
        ) if response.status_code == 200 else logging.error(
            json.dumps(response.json(), indent=2)
        )
    except:
        logging.exception("Detected image uploading error")


def detect_cars_from_sources(source: str, id: UUID, min_area: int, skip_frames: int, show_debug: bool,
                             recognition_service: str) -> None:
    """

    :param source:
    :param id:
    :param min_area:
    :param skip_frames:
    :param show_debug:
    :param recognition_service:
    :return:
    """

    cap = cv2.VideoCapture(source)

    frame_count = 0

    while True:
        frame_count += 1

        ret, frame = cap.read()
        if not ret:
            continue
        if frame_count < skip_frames:
            continue

        frame_count = 0

        results = model.track(frame, persist=True)
        h, w, _ = frame.shape
        boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
        ids = results[0].boxes.id.cpu().numpy().astype(int)
        for box, box_id in zip(boxes, ids):
            if box[2] * box[3] / (h * w) * 100 >= min_area:
                res_color = MIN_AREA_COLOR
                post_cropped_frame(recognition_service, frame, box, id)
                # crop_images.append(frame[box[1]:box[3], box[0]:box[2]])
                # cv2.imshow('crop', crop_images[-1])
            else:
                res_color = LESS_AREA_COLOR
            cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), res_color, 1)
            cv2.putText(frame, f"box_id {box_id}", (box[0], box[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, res_color, 1)

        if show_debug:
            cv2.imshow(source, frame)

        if cv2.waitKey(1) == KEYCODE_ESCAPE:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('--source', type=str, help='Define video source RTSP url')
    parser.add_argument('--id', type=str, help='Define identifier of detector instance')
    parser.add_argument('--min-area', type=int, help='Define minimum detect area to frame area (in percents)')
    parser.add_argument('--skip-frames', type=int, default=0, help='Define number of frames that should be skipped')
    parser.add_argument('--show-debug', action='store_true', default=False, help='Show debug window')
    parser.add_argument('--logging-mode', type=float, help='Define logging mode')
    parser.add_argument('--recognition-service', type=str, help='Define recognition service address')

    args = parser.parse_args()

    detect_cars_from_sources(args.source, UUID(args.id), args.min_area, args.skip_frames, args.show_debug,
                             args.recognition_service)
