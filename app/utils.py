import hashlib
import datetime

from app import setting


def get_hash():
    return str(hashlib.md5('{ts}{private_key}{public_key}'.format(
        ts=datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
        private_key=setting.MARVEL_API_CONF.get('private_key'),
        public_key=setting.MARVEL_API_CONF.get('public_key'),
    ).encode('utf-8')).hexdigest())

