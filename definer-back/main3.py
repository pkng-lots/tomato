import os
import glob
import cv2
import argparse

from nomeroff_net import pipeline


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-s",
                    "--show",
                    required=False,
                    default=0,
                    type=int,
                    help="Show filled number plate photos")

    args = vars(ap.parse_args())
    return args


if __name__ == '__main__':
    kwargs = parse_args()
    is_show = True

    number_plate_short_detection_and_reading = pipeline("number_plate_key_points_filling",
                                                        image_loader="opencv")

    images = number_plate_short_detection_and_reading(glob.glob('001.jpg'))
    if is_show:
        for img in images:
            img = img[..., ::-1]  # RGB2BGR
            cv2.imshow("Display window", img)
            k = cv2.waitKey(0)