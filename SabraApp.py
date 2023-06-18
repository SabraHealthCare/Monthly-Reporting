import pandas as pd
import streamlit as st
from st_files_connection import FilesConnection



conn = st.experimental_connection('s3', type=FilesConnection)
df = conn.read("sabramapping/test.csv", input_format="csv", ttl=600)
st.write(df)
# Print results.
for row in df.itertuples():
    st.write(f"{row.Owner} has a :{row.Pet}:")


import boto3
import streamlit as st

pdf = st.file_uploader(label="Drag the PDF file here. Limit 100MB")
if pdf is not None:
    s3 = boto3.client(
        service_name="s3",
        region_name="xxx",
        aws_access_key_id="xxx",
        aws_secret_access_key="xxx",
    )

    id = 123
    bucket_name = "xxx"
    print(pdf)
    print(type(pdf))
    pdf.seek(0)
    name = "pdf_" + str(id) + ".pdf"
    print(name)
    s3.upload_fileobj(pdf, "pdf_storage", name)



