import hashlib
import datetime
import json
import aiohttp

from app import setting


def get_hash():
    return str(hashlib.md5('{ts}{private_key}{public_key}'.format(
        ts=datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
        private_key=setting.MARVEL_API_CONF.get('private_key'),
        public_key=setting.MARVEL_API_CONF.get('public_key'),
    ).encode('utf-8')).hexdigest())


async def generate_info(name):
    ts = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    pk = setting.MARVEL_API_CONF.get('public_key')
    hash = get_hash()
    async with aiohttp.ClientSession() as session:
        search_uri = setting.MARVEL_API_CONF.get('search_uri')
        uri = '{}ts={}&name={}&limit=100&apikey={}&hash={}'.format(
            search_uri, ts, name, pk, hash
        )
        async with session.get(uri) as resp:
            json_resp = await resp.text()

    data = json.loads(json_resp)

    try:
        results = data['data']['results']
        hero_id = [i['id'] for i in results][0]
    except:
        hero_id = None

    if hero_id:
        async with aiohttp.ClientSession() as session:
            hero_uri = setting.MARVEL_API_CONF.get('hero_uri').format(hero_id)
            uri = '{}ts={}&limit=100&apikey={}&hash={}'.format(
                hero_uri, ts, pk, hash
            )
            async with session.get(uri) as resp:
                hero = await resp.text()

        async with aiohttp.ClientSession() as session:
            comics_uri = setting.MARVEL_API_CONF.get('comics_uri').format(hero_id)
            uri = '{}ts={}&limit=12&orderBy=onsaleDate&apikey={}&hash={}'.format(
                comics_uri, ts, pk, hash
            )
            async with session.get(uri) as resp:
                comics = await resp.text()

        async with aiohttp.ClientSession() as session:
            events_uri = setting.MARVEL_API_CONF.get('events_uri').format(id)
            uri = '{}ts={}&limit=12&orderBy=startDate&apikey={}&hash={}'.format(
                events_uri, ts, pk, hash
            )
            async with session.get(uri) as resp:
                events = await resp.text()
