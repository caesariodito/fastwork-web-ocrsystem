import streamlit as st
import functions as f
from PIL import Image

thumbnail = Image.open("./docs/thumbnail.jpg")
logo = Image.open("./docs/logo.png")

# PAGE CONFIG
st.set_page_config(layout="centered", page_icon=logo, page_title="OCR System")

# SESSION CONFIG
st.session_state.disabled = True
st.session_state.clicked = False

# Thumbnail for PLN
st.image(thumbnail, use_column_width=True)
st.title("OCR System")

# col1, col2 = st.columns(2)
# col1.header("Labels here")
# labels = col1.text_area("input your labels here", key="labels")

# col2.header("Image links here")
# image_links = col2.text_area("input your links of images here", key="image_links")

placeholder_image_link = """https://portalapp.iconpln.co.id/acmt/DisplayBlobServlet1?idpel=322722109343&nomor_meter=null&blth=202403
https://portalapp.iconpln.co.id/acmt/DisplayBlobServlet1?idpel=322700119528&nomor_meter=null&blth=202403
https://portalapp.iconpln.co.id/acmt/DisplayBlobServlet1?idpel=322700134188&nomor_meter=null&blth=202403
"""
st.header("Image links here")
image_links = st.text_area(
    "input your links of images here",
    key="image_links",
    placeholder=placeholder_image_link,
)

if image_links.replace(" ", "") != "":
    st.session_state.disabled = False

st.write("Ctrl + Enter to read the link of images")
st.divider()

st.session_state.clicked = not st.session_state.get("disabled")
if st.session_state.get("clicked"):
    predictions = f.perform_ocr(image_links)

    df = f.generate_dataframe(image_links, predictions)
    st.data_editor(
        df,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Status": st.column_config.CheckboxColumn(
                "Status", help="Check if the prediction is correct"
            ),
            "ImageURL": st.column_config.ImageColumn(
                "ImageURL", help="Image data preview"
            ),
        },
    )
else:
    st.write("Please input the link of images and the table will be shown here.")
