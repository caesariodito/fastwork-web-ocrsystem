import streamlit as st
from streamlit import session_state as ss, data_editor as de, rerun as rr
import functions as f
from PIL import Image
import pandas as pd

# PAGE CONFIG
thumbnail = Image.open("./docs/thumbnail.jpg")
logo = Image.open("./docs/logo.png")
st.set_page_config(layout="centered", page_icon=logo, page_title="OCR System")


# INITS
NAMES = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
model_path = "./model/ocr_best.pt"
model = f.init_model(model_path)

blth = ["202403"]
idpel = ["322732002569"]
image_urls = [
    f"https://portalapp.iconpln.co.id/acmt/DisplayBlobServlet1?idpel={idpel[0]}&nomor_meter=null&blth={blth[0]}"
]

start_data = pd.DataFrame(
    {
        "ImageURL": image_urls,
        "Status": False,
        "Hasil OCR": "5693",
        "Stand Kini": None,
        "Blth": blth,
        "IDPEL": idpel,
    },
)

if "start_df" not in ss:
    ss.start_df = start_data


def main():
    # Thumbnail for PLN
    st.image(thumbnail, use_column_width=True)
    st.title("OCR System")

    st.divider()

    false_status = st.button("Show only incorrect data")

    edited_df = de(
        ss.start_df,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        disabled=("Status", "Hasil OCR"),
        column_config={
            "Status": st.column_config.CheckboxColumn(
                "Status", help="Check if the prediction is correct"
            ),
            "ImageURL": st.column_config.ImageColumn(
                "ImageURL", help="Image data preview"
            ),
        },
    )

    if false_status:
        edited_df = edited_df[edited_df["Status"] == False]

    if not ss.start_df.equals(edited_df):
        ss.start_df = edited_df
        ss.start_df.reset_index(drop=True, inplace=True)
        my_bar = st.progress(0, text="Loading...")
        for index, row in ss.start_df.iterrows():
            my_bar.progress(int(index * 100 / ss.start_df.shape[0]), text="Loading...")
            row["Status"] = False
            if (
                not pd.isna(row["Blth"])
                and not pd.isna(row["IDPEL"])
                and row["Hasil OCR"] is None
            ):
                row["ImageURL"] = (
                    f"https://portalapp.iconpln.co.id/acmt/DisplayBlobServlet1?idpel={row['IDPEL']}&nomor_meter=null&blth={row['Blth']}"
                )
                row["Hasil OCR"] = f.perform_ocr(row["ImageURL"], model, NAMES)
            if row["Stand Kini"] == row["Hasil OCR"] and (
                row["Stand Kini"] is not None and row["Hasil OCR"] is not None
            ):
                row["Status"] = True
        rr()


if __name__ == "__main__":
    main()
