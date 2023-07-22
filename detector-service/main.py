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


def get_lp_from_definer(url: str, frame: numpy.array, box: list, id: UUID) -> dict:
    try:
        cropped = frame[box[1]: box[3], box[0]: box[2]]
        response = requests.post(
            url,
            data={"id": str(id)},
            files={"file": convert_image_to_bytes(cropped)},
        )
        return response.json() \
            if response.status_code == 200 else logging.error(
                json.dumps(response.json(), indent=2)
            )
    except:
        logging.exception("Detected image uploading error")


def detect_and_define_cars_from_source(source: str, id: UUID, min_area: int, skip_frames: int, show_debug: bool,
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
        try:
            boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
            ids = results[0].boxes.id.cpu().numpy().astype(int)
            for box, box_id in zip(boxes, ids):
                if (box[2] - box[0]) * (box[3] - box[1]) / (h * w) * 100 >= min_area:
                    res_color = MIN_AREA_COLOR
                    result = get_lp_from_definer(recognition_service, frame, box, id)
                    if result and result.get('text'):
                        cv2.rectangle(frame,
                                      (result['lb_x'] + box[0], result['lb_y'] + box[1]),
                                      (result['rt_x'] + box[0], result['rt_y'] + box[1]),
                                      res_color, 2)
                        cv2.putText(frame, f"{result['text']}",
                                    (result['lb_x'] + box[0], result['rt_y'] + box[1] - 5),
                                    cv2.FONT_HERSHEY_SIMPLEX, (result['lb_y'] - result['rt_y']) / 50, res_color, 1)

                    # crop_images.append(frame[box[1]:box[3], box[0]:box[2]])
                    # cv2.imshow('crop', crop_images[-1])
                else:
                    res_color = LESS_AREA_COLOR
                if show_debug:
                    cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), res_color, 1)
                    cv2.putText(frame, f"box_id {box_id}", (box[0], box[1] - 5),
                                cv2.FONT_HERSHEY_SIMPLEX, (box[2] - box[0]) / 300, res_color, 1)

            if show_debug:
                # down_points = (1920, 1080)
                # resized = cv2.resize(frame, down_points, interpolation=cv2.INTER_LINEAR)

                # cv2.imshow(source, resized)
                cv2.imshow(source, frame)

            if cv2.waitKey(1) == KEYCODE_ESCAPE:
                break

        except:
            pass

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

    detect_and_define_cars_from_source(args.source, UUID(args.id), args.min_area, args.skip_frames, args.show_debug,
                                       args.recognition_service)
