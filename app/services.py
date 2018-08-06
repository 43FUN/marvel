import aiohttp
import datetime

from app import setting
from app.utils import get_hash


class GenerateHeroInfo:

    def __init__(self, name):
        self.name = name
        self.ts = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        self.apikey = setting.MARVEL_API_CONF.get('public_key')
        self.key_hash = get_hash()

    async def get_hero_by_name(self):
        async with aiohttp.ClientSession() as session:
            search_uri = setting.MARVEL_API_CONF.get('search_uri')
            uri = f'{search_uri}ts={self.ts}&name={self.name}' \
                  f'&limit=1&apikey={self.apikey}&hash={self.key_hash}'
            async with session.get(uri) as resp:
                json_resp = await resp.json()
            return json_resp

    async def get_comics_by_hero_id(self, hero_id):
        async with aiohttp.ClientSession() as session:
            comics_uri = setting.MARVEL_API_CONF.get(
                'comics_uri'
            ).format(hero_id)
            uri = f'{comics_uri}ts={self.ts}&limit=12&orderBy=onsaleDate' \
                  f'&apikey={self.apikey}&hash={self.key_hash}'
            async with session.get(uri) as resp:
                json_resp = await resp.json()
            return json_resp

    async def get_events_by_hero_id(self, hero_id):
        async with aiohttp.ClientSession() as session:
            events_uri = setting.MARVEL_API_CONF.get(
                'events_uri'
            ).format(hero_id)
            uri = f'{events_uri}ts={self.ts}&limit=12&orderBy=startDate' \
                  f'&apikey={self.apikey}&hash={self.key_hash}'
            async with session.get(uri) as resp:
                json_resp = await resp.json()
            return json_resp

    async def json_generate(self, hero):
        data = {
            'hero': {
                'id': hero.get('id'),
                'name': hero.get('name'),
                'description': hero.get('description'),
                'modified': hero.get('modified'),
                'thumbnail': hero.get('thumbnail'),
                'resourceURI': hero.get('resourceURI')
            },
        }

        raw_comicses_info = await self.get_comics_by_hero_id(hero['id'])
        comics_list = raw_comicses_info.get('data', {}).get('results', [])
        changed_comics_list = []
        for comics in comics_list:
            changed_comics_list.append({
                'id': comics.get('id'),
                'title': comics.get('title'),
                'description': comics.get('description'),
                'modified': comics.get('modified'),
                'resourceURI': comics.get('resourceURI'),
                'urls': comics.get('urls')
            })
        data['comicses'] = changed_comics_list

        raw_events_info = await self.get_events_by_hero_id(hero['id'])
        events_list = raw_events_info.get('data', {}).get('results', [])
        changed_events_list = []
        for events in events_list:
            changed_events_list.append({
                'id': events.get('id'),
                'title': events.get('title'),
                'description': events.get('description'),
                'modified': events.get('modified'),
                'resourceURI': events.get('resourceURI'),
                'urls': events.get('urls'),
            })
        data['events'] = changed_events_list

        return data

    async def get_full_info(self):
        raw_hero_info = await self.get_hero_by_name()
        hero_list = raw_hero_info.get('data', {}).get('results', [])
        hero = hero_list[0] if hero_list else None
        if hero:
            return await self.json_generate(hero)
        return {}
