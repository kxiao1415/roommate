import base64
import uuid


def generate_guid():
    guid = base64.urlsafe_b64encode(uuid.uuid4().hex.encode('UTF-8')).decode('ascii')
    return guid[:-1]
