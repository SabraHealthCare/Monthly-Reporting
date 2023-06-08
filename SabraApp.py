import requests
import streamlit as st
#from streamlit_lottie import st_lottie
from PIL import Image


# Find more emojis here: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="My Webpage", page_icon=":tada:", layout="wide")


st.title("Sabra HealthCare Reporting App")

st.subheader("Operator name:")
option = st.selectbox(
    ' ',
    ("Advanced Recovery Systems",
"Affinity",
"Andrew Residence",
"Atrium Health",
"Aurora",
"Avalon",
"Avalon Realty",
"Avamere Family",
"Avista",
"Baybridge",
"Baylor Scott & White",
"Bear Mountain",
"Brickyard",
"Cadia",
"Celebration",
"Chai",
"Civitas",
"Claiborne",
"CommuniCare",
"Consulate",
"Covenant Care",
"Discovery",
"Dwight",
"EBS",
"EHG",
"Emerald",
"EmpRes Healthcare",
"Encore",
"Enlivant",
"Ensign",
"Epic Group",
"Focused Post Acute",
"Forest Park",
"Fox",
"Fundamental",
"Genesis",
"Golden Living",
"Haven",
"Health Systems",
"Health_Dimension",
"Healthmark Group",
"Holiday",
"Ignite",
"Inspirit Senior Living",
"Landmark Recovery",
"Legacy Living",
"LeoBrownGroup",
"LifeHouse",
"Lifes Journey",
"Magnolia Health Sys",
"Maison",
"Marlin Spring - Excelsoins",
"Marlin Spring - Spring Living",
"Maxwell Group",
"Meridian",
"Meridian Health Care",
"National Healthcare",
"NeuroRestorative",
"New Dawn",
"New Haven",
"New Orange Hills",
"Nexion Health Mgmt",
"Nexus Systems",
"NMS",
"No Relationship",
"North Shore",
"Nye",
"Oakbrook",
"Paradigm",
"Parkside",
"Pathways",
"Peregrine",
"RCA",
"ResCare HomeCare",
"Retirement Living",
"RoseCastle",
"Saber",
"Sacred Heart",
"Salem Villages",
"Senior Care Centers",
"Shelbourne",
"Sienna",
"Signature Behavioral",
"Signature Healthcare",
"Sinceri Senior Living",
"Solvere",
"Southern Admin",
"Southern Healthcare",
"Southwest LTC",
"Spectrum Healthcare",
"Spring Hills",
"Stoney River",
"Sundara",
"Tenet",
"The McGuire Group",
"Titan",
"Trinity",
"TRMC",
"Tryko Partners",
"Vibra Healthcare",
"Vivra",
"Wachusett Ventures",
"Welcov Healthcare",
"Wingate Healthcare"))
    

st.subheader("Upload P&L:")
uploaded_files = st.file_uploader(" ", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.write("filename:", uploaded_file.name)
    st.write(bytes_data)

st.write(
        "By default, this P&L is for 2023 May reporting. "
        )
st.write("[Learn More >](https://pythonandvba.com)")


with st.container():

    # Documention: https://formsubmit.co/ !!! CHANGE EMAIL ADDRESS !!!
    contact_form = """
    <form action="https://formsubmit.co/YOUR@MAIL.COM" method="POST">
        <button type="submit">Run Checking</button>
    </form>
    """
    left_column, right_column = st.columns(2)
    with left_column:
        st.markdown(contact_form, unsafe_allow_html=True)
    with right_column:
        st.empty()
