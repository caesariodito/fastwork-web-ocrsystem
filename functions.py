import requests
from datetime import datetime
import typing
from PIL import Image
from ultralytics import YOLO
import time

import streamlit as st


@st.cache_resource
def init_model(model_path):
    model = YOLO(model_path, task="detect")
    return model


def timer(start_time: datetime = None) -> "typing.Union[datetime.datetime, str]":
    """
    Measures the time elapsed from a given start time.

    If no start time is provided, returns the current time. If a start time is provided, returns a formatted string
    representing the time elapsed from the start time to the current time.

    Args:
        start_time (datetime.datetime, optional): The start time to measure elapsed time from, or None to get the current time. Defaults to None.

    Returns:
        Union[datetime.datetime, str]: The current time if no start time is provided, or a formatted string representing the elapsed time.
    """
    if not start_time:
        start_time = datetime.now()
        return start_time
    elif start_time:
        thour, temp_sec = divmod((datetime.now() - start_time).total_seconds(), 3600)
        tmin, tsec = divmod(temp_sec, 60)
        return "%i hours %i minutes and %s seconds." % (
            thour,
            tmin,
            round(tsec, 2),
        )


def perform_ocr(link: str, model, names) -> list:
    try:
        ocr_timer = timer(None)

        im = load_image_from_url(link)

        results = predict(im, model)

        for result in results:
            label = get_text(result, names)

        # st.write(f"Time to perform OCR: {timer(ocr_timer)}")
        # st.write("Done...")

        return label[:5].lstrip("0")
    except Exception as e:
        st.error(f"An error occurred: {e}")
        time.sleep(3)
        return None


# change the package into imread-from-url
@st.cache_data(show_spinner=False)
def load_image_from_url(url):
    result = Image.open(requests.get(url, stream=True).raw)
    return result


def predict(_image, model):
    result = model.predict(source=_image, stream=False, verbose=False)
    return result


def get_text(result, names):
    boxes = result.boxes.xyxy
    classes = result.boxes.cls

    sorted_indices = boxes[:, 0].argsort()
    # sorted_boxes = boxes[sorted_indices]
    sorted_cls = classes[sorted_indices]

    file_labels = [names[int(c)] for c in sorted_cls]
    label = "".join(file_labels)

    return label
