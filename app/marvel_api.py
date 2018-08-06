import datetime

import aiohttp

from app import setting
from app.utils import get_hash


async def base_request_to_marvel(path, params):
    marvel_hash = get_hash()
    ts = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    apikey = setting.MARVEL_API_CONF.get('public_key')
    other_params = '&'.join([f'{k}={v}' for k, v in params.items()])
    uri = f'{path}ts={ts}&apikey={apikey}&hash={marvel_hash}&{other_params}'
    async with aiohttp.ClientSession() as session:
        async with session.get(uri) as resp:
            return await resp.json()


async def get_hero_by_name(name):
    return await base_request_to_marvel(
        path=setting.MARVEL_API_CONF.get('search_uri'),
        params={
            'limit': 1,
            'name': name
        }
    )


async def get_comics_by_hero_id(hero_id):
    return await base_request_to_marvel(
        path=setting.MARVEL_API_CONF.get('comics_uri').format(hero_id),
        params={
            'limit': 12,
            'orderBy': 'onsaleDate',
        }
    )


async def get_events_by_hero_id(hero_id):
    return await base_request_to_marvel(
        path=setting.MARVEL_API_CONF.get('events_uri').format(hero_id),
        params={
            'limit': 12,
            'orderBy': 'startDate',
        }
    )
