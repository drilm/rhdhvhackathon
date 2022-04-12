from specklepy.api.client import SpeckleClient
from rhdhvclient import RhdhvClient
from streamlit_echarts import st_echarts
# from streamlit.components
# from streamlit_echarts

light_purple = "#d7c7d9"
middle_purple = "#be99f2"
dark_purple = "#544f73"
light_yellow = "#f2f0d8"
orange = "#f2c48d"
background_grey = "#d3d3d3"


def get_embedded_viewer_url(client: RhdhvClient, stream_id="7b5675e550", branch_name="main"):
    branch = client.client.branch.get(stream_id, branch_name)
    commit = branch.commits.items[0]
    string = f"https://speckle.xyz/embed?stream={stream_id}&commit={commit.id}"
    print(string)
    return string


def get_results(client: RhdhvClient, stream_id="7b5675e550", branch_name="results"):
    data = client.get(stream_id, branch_name)
    results = getattr(data, "@results")[0][0]

    result_items = []
    for name in ["area_living", "area_office", "area_shopping", "concrete_volume", "steel_volume_circular",
                 "steel_volume_total"]:
        result_items.append(getattr(results, f"@{name}", 0))
    return result_items


def get_donut_chart(names, values):
    data = []
    for name, value in zip(names, values):
        data.append({"value": value, "name": name})
    options = {
        "tooltip": {"trigger": "item"},
        "legend": {"top": "5%", "left": "center"},
        "series": [
            {
                "name": "Area distribution",
                "type": "pie",
                "radius": ["40%", "70%"],
                "avoidLabelOverlap": False,
                "itemStyle": {
                    "borderRadius": 10,
                    "borderColor": "#fff",
                    "borderWidth": 2,
                },
                "label": {"show": False, "position": "center"},
                "emphasis": {
                    "label": {"show": True, "fontSize": "30", "fontWeight": "bold"}
                },
                "labelLine": {"show": False},
                "data": data,
            }
        ],
    }
    return st_echarts(
        options=options, height="500px",
    )


def get_area_chart(area_residential, area_shopping, area_offices):
    requirement_residential = 9600
    requirement_shopping = 1600
    requirement_offices = 8000

    area_residential = int(area_residential)
    area_shopping = int(area_shopping)
    area_offices = int(area_offices)

    options = {
        "tooltip": {
          "trigger": 'axis',
          "axisPointer": {
            "type": 'shadow'
          }
        },
        "legend": {},
        "grid": {
          "left": '3%',
          "right": '4%',
          "bottom": '3%',
          "containLabel": True
        },
        "xAxis": {
          "type": 'value'
        },
        "yAxis": {
          "type": 'category',
          "data": ["Residential Area [m\u00b2]", "Shopping Area [m\u00b2]", "Office Area [m\u00b2]"]
        },
        "series": [
            {
                "name": 'Required Area',
                "type": 'bar',
                "stack": 'total',
                "label": {
                    "show": True
                },
                "emphasis": {
                    "focus": 'series'
                },
                "data": [requirement_residential, requirement_shopping, requirement_offices],
                "itemStyle": {"color": dark_purple},
            },
            {
                "name": 'Designed Area',
                "type": 'bar',
                "stack": 'total',
                "label": {
                    "show": True
                },
                "emphasis": {
                    "focus": 'series'
                },
                "data": [area_residential, area_shopping, area_offices],
                "itemStyle": {"color": light_yellow},
            }
        ]}
    return st_echarts(options)


if __name__ == "__main__":
    rhdhv_client = RhdhvClient("https://speckle.xyz", "278e941550a587c89dce1d4778233e9d17b0d9e6f3")
    get_embedded_viewer_url(rhdhv_client)

    print(get_results(rhdhv_client))