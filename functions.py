import pandas as pd
import requests
from PIL import Image
from ultralytics import YOLO

import streamlit as st


COLUMNS = ["ImageURL", "Status", "Hasil OCR", "Blth", "IDPEL"]
model_path = "./model/ocr_best.pt"
model = YOLO(model_path, task="detect")


@st.cache_data(show_spinner=False)
def generate_dataframe(links: str, predictions: list) -> pd.DataFrame:
    total_row = len(links.split("\n"))

    statuses = [False] * total_row
    blth = [""] * total_row
    idpel = [""] * total_row
    df = pd.DataFrame(
        {
            "ImageURL": links.split("\n"),
            "Status": statuses,
            "Hasil OCR": predictions,
            "Blth": blth,
            "IDPEL": idpel,
        },
        columns=COLUMNS,
    )

    return df


@st.cache_data(show_spinner=False)
def load_image_from_url(url):
    return Image.open(requests.get(url, stream=True).raw)


def perform_ocr(links: str) -> list:
    labels = []
    urls = links.split("\n")
    my_bar = st.progress(0, text="Performing OCR...")

    for i, url in enumerate(urls):
        my_bar.progress(int(i * 100 / len(urls)), text="Performing OCR...")

        im = load_image_from_url(url)

        results = predict(im)
        for result in results:
            label = get_text(result)
            labels.append(label)

    my_bar.empty()

    return labels


def predict(_image):
    return model(source=_image, stream=True)


def get_text(result):
    boxes = result.boxes.xyxy
    cls = result.boxes.cls

    sorted_indices = boxes[:, 0].argsort()
    # sorted_boxes = boxes[sorted_indices]
    sorted_cls = cls[sorted_indices]

    file_labels = [model.names[int(c)] for c in sorted_cls]
    label = "".join(file_labels)

    return label
