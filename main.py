import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# Thumbnail for PLN
st.title("OCR System")

col1, col2 = st.columns(2)
col1.header("Labels here")
labels = col1.text_area("input your labels here", key="labels")

col2.header("Image links here")
image_links = col2.text_area("input your links of images here", key="image_links")

st.button("Submit")
st.divider()


data = [
    [
        "Cat",
        "Dog",
        False,
        "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/5435b8cb-6c6c-490b-9608-799b543655d3/Home_Page.png",
    ],
    [
        "Dog",
        "Dog",
        False,
        "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/5435b8cb-6c6c-490b-9608-799b543655d3/Home_Page.png",
    ],
    [
        "Apple",
        "Banana",
        False,
        "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/5435b8cb-6c6c-490b-9608-799b543655d3/Home_Page.png",
    ],
    [
        "Car",
        "Truck",
        False,
        "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/5435b8cb-6c6c-490b-9608-799b543655d3/Home_Page.png",
    ],
    [
        "Person",
        "Bicycle",
        False,
        "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/5435b8cb-6c6c-490b-9608-799b543655d3/Home_Page.png",
    ],
    [
        "House",
        "Building",
        False,
        "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/5435b8cb-6c6c-490b-9608-799b543655d3/Home_Page.png",
    ],
    [
        "Tree",
        "Plant",
        False,
        "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/5435b8cb-6c6c-490b-9608-799b543655d3/Home_Page.png",
    ],
    [
        "Flower",
        "Rose",
        False,
        "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/5435b8cb-6c6c-490b-9608-799b543655d3/Home_Page.png",
    ],
    [
        "Shirt",
        "Dress",
        False,
        "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/5435b8cb-6c6c-490b-9608-799b543655d3/Home_Page.png",
    ],
    [
        "Book",
        "Pen",
        False,
        "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/5435b8cb-6c6c-490b-9608-799b543655d3/Home_Page.png",
    ],
    [
        "Cloud",
        "Sky",
        False,
        "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/5435b8cb-6c6c-490b-9608-799b543655d3/Home_Page.png",
    ],
    [
        "Sun",
        "Moon",
        False,
        "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/5435b8cb-6c6c-490b-9608-799b543655d3/Home_Page.png",
    ],
    [
        "Star",
        "Planet",
        False,
        "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/5435b8cb-6c6c-490b-9608-799b543655d3/Home_Page.png",
    ],
    [
        "Bird",
        "Animal",
        False,
        "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/5435b8cb-6c6c-490b-9608-799b543655d3/Home_Page.png",
    ],
    [
        "Fish",
        "Sea",
        False,
        "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/5435b8cb-6c6c-490b-9608-799b543655d3/Home_Page.png",
    ],
    [
        "Bicycle",
        "Vehicle",
        False,
        "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/5435b8cb-6c6c-490b-9608-799b543655d3/Home_Page.png",
    ],
    [
        "Car",
        "Truck",
        False,
        "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/5435b8cb-6c6c-490b-9608-799b543655d3/Home_Page.png",
    ],
    [
        "Motorcycle",
        "Scooter",
        False,
        "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/5435b8cb-6c6c-490b-9608-799b543655d3/Home_Page.png",
    ],
    [
        "Train",
        "Bus",
        False,
        "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/5435b8cb-6c6c-490b-9608-799b543655d3/Home_Page.png",
    ],
    [
        "Airplane",
        "Helicopter",
        False,
        "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/5435b8cb-6c6c-490b-9608-799b543655d3/Home_Page.png",
    ],
    [
        "Table",
        "Chair",
        False,
        "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/5435b8cb-6c6c-490b-9608-799b543655d3/Home_Page.png",
    ],
    [
        "Cup",
        "Mug",
        False,
        "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/5435b8cb-6c6c-490b-9608-799b543655d3/Home_Page.png",
    ],
    [
        "Plate",
        "Bowl",
        False,
        "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/5435b8cb-6c6c-490b-9608-799b543655d3/Home_Page.png",
    ],
    [
        "Fork",
        "Spoon",
        False,
        "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/5435b8cb-6c6c-490b-9608-799b543655d3/Home_Page.png",
    ],
    [
        "Knife",
        "Scissors",
        False,
        "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/5435b8cb-6c6c-490b-9608-799b543655d3/Home_Page.png",
    ],
    [
        "Pen",
        "Pencil",
        False,
        "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/5435b8cb-6c6c-490b-9608-799b543655d3/Home_Page.png",
    ],
    [
        "Paper",
        "Notebook",
        False,
        "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/5435b8cb-6c6c-490b-9608-799b543655d3/Home_Page.png",
    ],
    [
        "Computer",
        "Laptop",
        False,
        "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/5435b8cb-6c6c-490b-9608-799b543655d3/Home_Page.png",
    ],
    [
        "Phone",
        "Tablet",
        False,
        "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/5435b8cb-6c6c-490b-9608-799b543655d3/Home_Page.png",
    ],
    [
        "Watch",
        "Clock",
        False,
        "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/5435b8cb-6c6c-490b-9608-799b543655d3/Home_Page.png",
    ],
]

# Create a DataFrame
df = pd.DataFrame(data, columns=["Label", "Predictions", "Correct", "ImageLink"])

# only unlock Label columns
st.data_editor(
    df,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "Correct": st.column_config.CheckboxColumn(
            "Correct", help="Check if the prediction is correct"
        ),
        "ImageLink": st.column_config.ImageColumn(
            "Preview Image", help="Image data preview"
        ),
    },
)
