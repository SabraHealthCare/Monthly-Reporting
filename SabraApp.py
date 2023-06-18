import pandas as pd
import streamlit as st
from st_files_connection import FilesConnection


conn = st.experimental_connection('s3', type=FilesConnection)
df = conn.read("sabramapping/test.csv", input_format="csv", ttl=600)

# Print results.
for row in df.itertuples():
    st.write(f"{row.Owner} has a :{row.Pet}:")






