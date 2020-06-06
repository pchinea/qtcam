from datetime import datetime
from functools import wraps
from typing import Callable, Tuple

import cv2
import numpy as np

FilterType = Callable[[np.ndarray], np.ndarray]


def add_filter_name(description: str) -> Callable[[FilterType], FilterType]:
    def wrapper(func: FilterType) -> FilterType:
        class FuncType:
            def __call__(self, *args, **kwargs) -> np.ndarray:
                return func(*args, **kwargs)

            def __str__(self) -> str:
                return description

            @property
            def is_filter(self) -> bool:
                return True
        return wraps(func)(FuncType())
    return wrapper


class Filter:

    @classmethod
    def get_all_filters(cls) -> Tuple[FilterType, ...]:
        filters = []
        for flt in dir(cls):
            if hasattr(getattr(cls, flt), 'is_filter'):
                filters.append(getattr(cls, flt))
        return tuple(filters)

    # Filter implementations:

    @staticmethod
    @add_filter_name("Grayscale")
    def gray(frame: np.ndarray) -> np.ndarray:
        if len(frame.shape) == 3:
            return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            return frame

    @staticmethod
    @add_filter_name("Vertical Flip")
    def x_flip(frame: np.ndarray) -> np.ndarray:
        return cv2.flip(frame, 0)

    @staticmethod
    @add_filter_name("Horizontal Flip")
    def y_flip(frame: np.ndarray) -> np.ndarray:
        return cv2.flip(frame, 1)

    @staticmethod
    @add_filter_name("Negative")
    def negative(frame: np.ndarray) -> np.ndarray:
        return cv2.bitwise_not(frame)

    @staticmethod
    @add_filter_name("BGR")
    def bgr(frame: np.ndarray) -> np.ndarray:
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    @staticmethod
    @add_filter_name("Timestamp")
    def timestamp(frame: np.ndarray) -> np.ndarray:
        now = str(datetime.now())[:-7]
        org = (1, frame.shape[0] - 3)
        font = cv2.FONT_HERSHEY_PLAIN
        size = 1
        cv2.putText(frame, now, org, font, size, (0, 0, 0), 2)
        cv2.putText(frame, now, org, font, size, (255, 255, 255), 1)
        return frame

    #

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    @staticmethod
    @add_filter_name("Face Detection")
    def face_detection(frame: np.ndarray) -> np.ndarray:
        if len(frame.shape) == 3:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            gray = frame
        faces = Filter.face_cascade.detectMultiScale(
            gray,
            1.05,
            5,
            minSize=(30, 30)
        )
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
        return frame

    #

    back_sub = cv2.createBackgroundSubtractorKNN()

    @staticmethod
    @add_filter_name("Subtract background")
    def subtract_background(frame: np.ndarray) -> np.ndarray:
        return Filter.back_sub.apply(frame)

    @staticmethod
    @add_filter_name("Sobel")
    def sobel(frame: np.ndarray) -> np.ndarray:
        dx = cv2.convertScaleAbs(cv2.Sobel(frame, cv2.CV_32F, 1, 0))
        dy = cv2.convertScaleAbs(cv2.Sobel(frame, cv2.CV_32F, 0, 1))
        return cv2.addWeighted(dx, 0.5, dy, 0.5, 0)

    @staticmethod
    @add_filter_name("Pixelated")
    def pixelated(frame: np.ndarray) -> np.ndarray:
        height, width = frame.shape[:2]
        h, w = (height // 10, width // 10)
        reduced = cv2.resize(frame, (w, h), interpolation=cv2.INTER_LINEAR)
        return cv2.resize(
            reduced,
            (width, height),
            interpolation=cv2.INTER_NEAREST
        )

    @staticmethod
    @add_filter_name("Edges")
    def edges(frame: np.ndarray) -> np.ndarray:
        return cv2.Canny(frame, 200, 100)
