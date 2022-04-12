from specklepy.objects.base import Base
import json
from rhdhvclient import RhdhvClient


def sort_profiles():
    stream_id = "5e9e00f5da"
    branch_name = "profiles"
    print("started")
    client = RhdhvClient("https://rhdhv.speckle.xyz", "7d37195b623a87c97eb3915d8a596e734aadfb26cf")
    data = client.get(stream_id, branch_name).data
    print("got stream")
    base = Base()
    base.profile_dict = {}

    with open("original_data.json", "w+") as file:
        json.dump([data], file, indent=2)
    print("written original data")
    total_length = 0
    for item in data:
        profile_type = item['profile_type']
        length = float(item.get('length '))
        if not base.profile_dict.get(profile_type):
            base.profile_dict[profile_type] = length
        else:
            base.profile_dict[profile_type] += length
        total_length += length
    print(f"looped over profiles and found in total {total_length} m")

    for key, value in base.profile_dict.items():
        base.profile_dict[key] = round(value, 1)

    with open("sorted_data.json", "w+") as file:
        json.dump(base.profile_dict, file, indent=2)
    print("written sorted data")

    target_stream_id = "7b5675e550"
    branch_name = "profiles"

    send_client = RhdhvClient("https://speckle.xyz", "278e941550a587c89dce1d4778233e9d17b0d9e6f3")
    send_client.send(base, target_stream_id, branch_name)


def retrieve_wind():
    stream_id = "5e9e00f5da"
    branch_name = "wind_loads"

    client = RhdhvClient("https://rhdhv.speckle.xyz", "7d37195b623a87c97eb3915d8a596e734aadfb26cf")
    data = client.get(stream_id, branch_name).data

    base = Base()
    base.data = data

    target_stream_id = "7b5675e550"
    branch_name = "wind_loads"

    with open(f"wind_loads.json", "w+") as file:
        json.dump(data, file, indent=2)

    send_client = RhdhvClient("https://speckle.xyz", "278e941550a587c89dce1d4778233e9d17b0d9e6f3")
    send_client.send(base, target_stream_id, branch_name)


if __name__ == "__main__":

    sort_profiles()
    retrieve_wind()