from ultralytics import YOLO
from typing import List
import cv2

KEYCODE_ESCAPE = 27
LESS_AREA_COLOR = (0, 0, 255)
MIN_AREA_COLOR = (0, 255, 0)

model = YOLO("yolov8n.pt")


def detect_cars_from_sources(sources: List[str], min_area: int, skip_frames: int, show_debug: bool) -> None:
    """

    :param sources:
    :param min_area:
    :param skip_frames:
    :return:
    """

    caps = []
    for source in sources:
        caps.append((cv2.VideoCapture(source), source))

    frame_count = 0

    while True:
        frame_count += 1
        for cap, source in caps:
            ret, frame = cap.read()
            if not ret:
                continue
            if frame_count < skip_frames:
                continue

            results = model.track(frame, persist=True)
            h, w, _ = frame.shape
            boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
            ids = results[0].boxes.id.cpu().numpy().astype(int)
            for box, id in zip(boxes, ids):
                if box[2] * box[3] / (h * w) * 100 >= min_area:
                    res_color = MIN_AREA_COLOR
                else:
                    res_color = LESS_AREA_COLOR
                cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), res_color, 1)
                cv2.putText(frame, f"id {id}", (box[0], box[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, res_color, 1)

            if show_debug:
                cv2.imshow(source, frame)

        if frame_count > skip_frames:
            frame_count = 0

        if cv2.waitKey(1) == KEYCODE_ESCAPE:
            break

    for cap, _ in caps:
        cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('--source-list', type=str, help='Define video source list')
    parser.add_argument('--min-area', type=int, help='Define minimum detect area to frame area (in percents)')
    parser.add_argument('--skip-frames', type=int, default=0, help='Define number of frames that should be skipped')
    parser.add_argument('--show-debug', action='store_true', default=False, help='Show debug window')
    parser.add_argument('--logging-mode', type=float, help='Define logging mode')
    parser.add_argument('--recognition-service', type=str, help='Define recognition service address')

    args = parser.parse_args()
    print(args.source_list)
    print(args.min_area)
    print(args.skip_frames)
    print(args.show_debug)
    print(args.logging_mode)
    print(args.recognition_service)

    detect_cars_from_sources(args.source_list.split(','), args.min_area, args.skip_frames, args.show_debug)
