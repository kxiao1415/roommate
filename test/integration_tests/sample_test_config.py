import os


class TestConfig(object):
    PRIVILEGED_TOKEN = 'this-really-needs-to-be-changed'
    IMAGES_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'images')
