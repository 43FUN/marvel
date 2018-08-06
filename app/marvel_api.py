import datetime

import aiohttp

from app import setting
from app.utils import get_hash


async def make_request_to_marvel(path, params):
    marvel_hash = get_hash()
    ts = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    apikey = setting.MARVEL_API_CONF.get('public_key')
    host = setting.MARVEL_API_CONF.get('host')
    version = setting.MARVEL_API_CONF.get('version')
    other_params = '&'.join([f'{k}={v}' for k, v in params.items()])
    uri = f'{host}{version}{path}ts={ts}&apikey={apikey}' \
          f'&hash={marvel_hash}&{other_params}'
    async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(verify_ssl=False)
    ) as session:
        async with session.get(uri) as resp:
            return await resp.json()


async def fetch_hero_by_name(name):
    raw_hero_info = await make_request_to_marvel(
        path='public/characters?',
        params={
            'limit': 1,
            'name': name
        }
    )
    hero_list = raw_hero_info.get('data', {}).get('results', [])
    hero = hero_list[0] if hero_list else None
    return hero


async def fetch_comics_by_hero_id(hero_id):
    return await make_request_to_marvel(
        path=f'public/characters/{hero_id}/comics?',
        params={
            'limit': 12,
            'orderBy': '-onsaleDate',
        }
    )


async def fetch_events_by_hero_id(hero_id):
    return await make_request_to_marvel(
        path=f'public/characters/{hero_id}/events?',
        params={
            'limit': 12,
            'orderBy': '-startDate',
        }
    )


async def fetch_comics_creators(comics_id):
    return await make_request_to_marvel(
        path=f'public/comics/{comics_id}/creators?',
        params={
            'limit': 1,
            'orderBy': '-modified',
        }
    )
