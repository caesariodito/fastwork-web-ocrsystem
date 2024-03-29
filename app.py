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
        "Status": True,
        "Hasil OCR": "5693",
        "Stand Kini": "5693",
        "BLTH": blth,
        "IDPEL": idpel,
    },
)

if "start_df" not in ss:
    ss.start_df = start_data
if "clicks" not in ss:
    ss["clicks"] = {}

if "file_uploader_key1" not in st.session_state:
    st.session_state["file_uploader_key1"] = 0

if "file_uploader_key2" not in st.session_state:
    st.session_state["file_uploader_key2"] = 0

if "uploaded_files" not in st.session_state:
    st.session_state["uploaded_files"] = []


def click(key):
    ss.clicks[key] = True


def main():
    # Thumbnail for PLN
    st.image(thumbnail, use_column_width=True)
    st.title("OCR System")

    col1, col2 = st.columns(2)
    df_columns_to_take = ["BLTH", "IDPEL", "SAHLWBP", "LWBPPAKAI"]

    with col1:
        file1 = st.file_uploader(
            "Upload Data Periode Sebelumnya",
            key="old_csv",
            type=["csv", "xlsx", "xls"],
        )
        if file1 is not None:
            try:
                # ss.start_df = pd.read_csv(file1)
                temp = pd.read_csv(file1)
            except Exception as e:
                # ss.start_df = pd.read_excel(file1)
                temp = pd.read_excel(file1)
            df_file1 = temp[df_columns_to_take]
            df_file1["BLTH"] = df_file1["BLTH"].astype(str)
            df_file1["IDPEL"] = df_file1["IDPEL"].astype(str)

    with col2:
        file2 = st.file_uploader(
            "Upload Data Periode Sekarang",
            key="new_csv",
            type=["csv", "xlsx", "xls"],
        )
        if file2 is not None:
            try:
                # ss.start_df = pd.read_csv(file2)
                temp = pd.read_csv(file2)
            except Exception as e:
                # ss.start_df = pd.read_excel(file2)
                temp = pd.read_excel(file2)
            df_file2 = temp[df_columns_to_take]
            df_file2["BLTH"] = df_file2["BLTH"].astype(str)
            df_file2["IDPEL"] = df_file2["IDPEL"].astype(str)

    st.divider()

    p1, p2 = st.columns(2)
    p1.button("Filter Status", on_click=click, args=("false",), key="false_data")
    p2.button("Perform Ocr", on_click=click, args=("ocr",), key="ocr_button")
    lock = st.checkbox("Lock Data", key="lock_data", value=ss.clicks.get("ocr"))

    # filter UI
    col_f1, col_f2 = st.columns(2)
    upfilter = col_f1.text_input("Filter Data Diatas Prosentase", key="up_filter")
    downfilter = col_f2.text_input("Filter Data Dibawah Prosentase", key="down_filter")

    edited_df = de(
        ss.start_df,
        num_rows="fixed" if lock else "dynamic",
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
        column_order=(
            "Status",
            "BLTH",
            "IDPEL",
            "Stand Kini",
            "Hasil OCR",
            "ImageURL",
            "Presentase",
        ),
    )

    if file1 is not None and file2 is not None:
        ss.start_df = df_file2.merge(df_file1, on="IDPEL", how="inner").sample(
            100, random_state=42
        )
        ss.start_df["Deviasi"] = ss.start_df["LWBPPAKAI_x"] - ss.start_df["LWBPPAKAI_y"]
        ss.start_df["Presentase"] = ss.start_df["Deviasi"] / ss.start_df["LWBPPAKAI_x"]
        base_url = "https://portalapp.iconpln.co.id/acmt/DisplayBlobServlet1?idpel={}&nomor_meter=null&blth={}"
        ss.start_df["ImageURL"] = [
            base_url.format(idpel, blth)
            for idpel, blth in zip(ss.start_df["IDPEL"], ss.start_df["BLTH_x"])
        ]
        ss.start_df.drop(
            ["BLTH_y", "SAHLWBP_y"],
            axis=1,
            inplace=True,
        )
        ss.start_df.rename(
            columns={
                "BLTH_x": "BLTH",
                "SAHLWBP_x": "Stand Kini",
                "LWBPPAKAI_x": "LWBP Pakai",
                "LWBPPAKAI_y": "LWBP Lalu",
            },
            inplace=True,
        )
        ss.start_df["Hasil OCR"] = None
        ss.start_df["Status"] = False

        ss.start_df["Stand Kini"] = ss.start_df["Stand Kini"].astype(str)
        ss.start_df.reset_index(inplace=True)

        ss.clicks["file1"] = False
        ss.clicks["file2"] = False

    if upfilter:
        ss.start_df = ss.start_df[ss.start_df["Presentase"] >= float(upfilter)]

    if downfilter:
        ss.start_df = ss.start_df[ss.start_df["Presentase"] <= float(downfilter)]

    if ss.clicks.get("ocr"):
        # if ocr_button:
        # ss.start_df["Hasil OCR"] = f.batch_ocr(
        #     ss.start_df["ImageURL"].tolist(), model, NAMES
        # )
        # my_bar = st.progress(0, text="Loading...")
        for index, row in ss.start_df.iterrows():
            # my_bar.progress(int(index * 100 / ss.start_df.shape[0]), text="Loading...")
            ocr_result = f.perform_ocr(row["ImageURL"], model, NAMES)
            ss.start_df.loc[index, "Hasil OCR"] = ocr_result
        # my_bar.empty()

        ss.start_df["Status"] = ss.start_df["Hasil OCR"] == ss.start_df["Stand Kini"]
        # st.write(ss.start_df["Status"])
        # ss.clicks["ocr"] = False

    if ss.clicks.get("false"):
        ss.start_df = ss.start_df[ss.start_df["Status"] == False]

    # st.write(not ss.start_df.equals(edited_df), file1 is None, file2 is None)
    # st.write(ss.start_df)
    # st.write(edited_df)

    if not edited_df.equals(ss.start_df) and file1 is None and file2 is None:
        ss.start_df = edited_df
        ss.start_df.reset_index(drop=True, inplace=True)
        my_bar = st.progress(0, text="Loading...")
        for index, row in ss.start_df.iterrows():
            my_bar.progress(int(index * 100 / ss.start_df.shape[0]), text="Loading...")
            row["Status"] = False
            if (
                not pd.isna(row["BLTH"])
                and not pd.isna(row["IDPEL"])
                and row["Hasil OCR"] is None
            ):
                row["ImageURL"] = (
                    f"https://portalapp.iconpln.co.id/acmt/DisplayBlobServlet1?idpel={row['IDPEL']}&nomor_meter=null&blth={row['BLTH']}"
                )
                row["Hasil OCR"] = f.perform_ocr(row["ImageURL"], model, NAMES)
            if row["Stand Kini"] == row["Hasil OCR"] and (
                row["Stand Kini"] is not None and row["Hasil OCR"] is not None
            ):
                row["Status"] = True
        rr()
    elif not ss.start_df.equals(edited_df):
        edited_df = ss.start_df
        rr()


if __name__ == "__main__":
    main()
