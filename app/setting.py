import os


ROOT_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '../'))
TEMPLATE_PATH = os.path.normpath(os.path.join(ROOT_DIR, 'app/templates'))

MARVEL_API_CONF = {
    'host': 'https://gateway.marvel.com/',
    'version': 'v1/',
    'public_key': 'bb62f6ae140a13de2fb9f1fd4b2c3d9d',
    'private_key': 'a27ac1d08a3b6ca01f4b28cd2bced0473bfdd3eb',
}
