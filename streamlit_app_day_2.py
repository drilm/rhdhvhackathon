import streamlit as st
import streamlit.components.v1 as components
from streamlit_echarts import st_echarts
from rhdhvclient import RhdhvClient
from utils import *
from PIL import Image

client = RhdhvClient("https://speckle.xyz", "278e941550a587c89dce1d4778233e9d17b0d9e6f3")

light_purple = "#d7c7d9"
middle_purple = "#be99f2"
dark_purple = "#544f73"
light_yellow = "#f2f0d8"
orange = "#f2c48d"
background_grey = "#d3d3d3"


st.set_page_config(
     page_title="Hackathon Dashboard team Wekker",
     page_icon="alarm-clock.png",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://www.extremelycoolapp.com/help',
         'Report a bug': "https://www.extremelycoolapp.com/bug",
         'About': "# This is a header. This is an *extremely* cool app!"
     }
 )

st.image(Image.open("alarm-clock.png"), width=200)

header = st.container()
results = st.container()
viewer = st.container()

with header:
    st.title(f"Hackathon Dashboard team Wekker")
    st.write("This is the dashboard that visualises the results of the Hackathon challenge for team Wekker! Here you "
             "will find the performance of the building ")


with results:
    st.subheader("Function allocation")
    area_living, area_offices, area_shopping, concrete_volume, steel_volume_circular, steel_volume_total = \
        get_results(client)

    requirement_residential = 9600
    requirement_shopping = 1600
    requirement_offices = 8000

    concrete_kg = 2400 * concrete_volume
    steel_kg = 7850 * (steel_volume_total - steel_volume_circular)
    circular_steel_kg = 7850 * steel_volume_circular

    concrete_CO2 = concrete_kg * 0.103
    steel_CO2 = steel_kg * 2.5  # kgCO2e
    saved_C02 = circular_steel_kg * 2.5  # kgCO2e
    total_CO2 = concrete_CO2 + steel_CO2

    circular_steel_meters_total = 53967.3
    circular_steel_meters_used = 20000

    col_1, col_2, col_3 = st.columns(3)
    with col_1:
        st.metric("Office Area", value=f"{round(area_offices, 1)} m\u00b2",
                  delta=f"{round((area_offices - requirement_offices) / requirement_offices * 100, 1)} %")
    with col_2:
        st.metric("Shopping Area", value=f"{round(area_shopping, 1)} m\u00b2",
                  delta=f"{round((area_shopping - requirement_shopping) / requirement_shopping * 100, 1)} %")
    with col_3:
        st.metric("Residential area", value=f"{round(area_living, 1)} m\u00b2",
                  delta=f"{round((area_living - requirement_residential) / requirement_residential * 100, 1)} %")

    get_area_chart(area_living, area_shopping, area_offices)

    st.subheader("Building Metrics")

    st.empty()

    st.metric("Building carbon [tons CO\u2082e]", value=f"{round(total_CO2 / 1000, 1)}", delta=f"- {round(saved_C02 / total_CO2 * 100, 1)}%",
              delta_color='inverse')

    st.metric("Circular steel stock used",
              value=f"{round(circular_steel_meters_used / circular_steel_meters_total * 100, 1)} %", delta="8.2 %")


with viewer:
    st.subheader("Viewer")
    st.write("Complete model:")
    components.iframe(src=get_embedded_viewer_url(client), height=400)
    st.write("Karamba model:")
    components.iframe(src=get_embedded_viewer_url(client, branch_name="karamba"), height=400)
