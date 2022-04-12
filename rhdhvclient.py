from specklepy.api.client import SpeckleClient
from specklepy.transports.server import ServerTransport
from specklepy.api import operations


class RhdhvClient:

    def __init__(self, url: str, token: str):
        self.client = SpeckleClient(url)
        self.client.authenticate_with_token(token)

    def get(self, stream_id, branch_name):
        transport = ServerTransport(client=self.client, stream_id=stream_id)
        commit = self.client.branch.get(stream_id=stream_id, name=branch_name).commits.items[0]
        hash_obj = commit.referencedObject
        return operations.receive(obj_id=hash_obj, remote_transport=transport)

    def send(self, data, stream_id: str, branch_name: str):
        transport = ServerTransport(client=self.client, stream_id=stream_id)
        hash_obj = operations.send(data, transports=[transport])
        commit_id = self.client.commit.create(stream_id, object_id=hash_obj, branch_name=branch_name)
        return commit_id
