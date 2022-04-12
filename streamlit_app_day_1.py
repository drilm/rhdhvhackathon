import streamlit as st
import streamlit.components.v1 as components

from specklepy.api.client import SpeckleClient
from specklepy.transports.server import ServerTransport
from specklepy.api import operations

import matplotlib.pyplot as plt

from PIL import Image

header = st.container()
graphs = st.container()
energy = st.container()
viewer = st.container()


area_shopping = 0
area_living = 0
area_offices = 0
area_green = 0
energy_production = 0
road_area = 0


def get_results():
    client = SpeckleClient("https://speckle.xyz")
    speckle_token = "278e941550a587c89dce1d4778233e9d17b0d9e6f3"
    client.authenticate(speckle_token)
    stream_id = "74151d106b"
    branch_name = "result"
    transport = ServerTransport(client=client, stream_id=stream_id)
    commit = client.branch.get(stream_id=stream_id, name=branch_name).commits.items[0]
    hash_obj = commit.referencedObject
    speckle_obj = operations.receive(obj_id=hash_obj, remote_transport=transport)
    data = getattr(speckle_obj, "@Data")[0][0]

    global area_green
    global area_shopping
    global area_living
    global area_offices
    global energy_production
    global road_area

    area_green = getattr(data, "@area_green", 0)
    area_shopping = getattr(data, "@area_shopping", 0)
    area_living = getattr(data, "@area_living", 0)
    area_offices = getattr(data, "@area_offices", 0)
    energy_production = getattr(data, "@energy_production", 0)
    road_area = getattr(data, "@road_area", 0)


def commit2viewer(stream_id, commit_id, height=400) -> str:
    embed_src = "https://speckle.xyz/embed?stream=74151d106b&commit=22e0c77955"
    return components.iframe(src=embed_src, height=height)


with header:
    st.title("Royal Hackathon Dashboard ")
    st.write("This is the dashboard of Team 'Innovation Hub'. Below you can find the are distribution of the different "
             "zones in the model.")


with graphs:
    labels = 'Residential', 'Office', 'Shopping', 'Green'
    get_results()
    sizes = [area_living, area_offices, area_shopping, area_green]

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, colors=['#FB86FF', '#3D084A', '#8C08FF', '#3C714A'],
            shadow=True, startangle=90)
    ax1.axis('equal')
    st.pyplot(fig1)

with energy:

    st.header("Yearly Energy Production")
    st.metric("kWh per year", energy_production, delta_color="normal")

with viewer:
    st.write(f"Below you can find the latest speckle commit in the 'building' branch of team 'Innovation Hub'.")

    stream_id = "74151d106b"
    commit_id = "22e0c77955"
    st.subheader("Latest Commit👇")
    commit2viewer(stream_id, commit_id)



if __name__ == "__main__":
    get_results()


