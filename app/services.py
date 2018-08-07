from app import marvel_api


class HeroDataCollector:

    def __init__(self, name):
        self.name = name

    async def collect_hero_info(self):
        hero = await marvel_api.fetch_hero_by_name(self.name)
        return {
            'id': hero.get('id'),
            'name': hero.get('name'),
            'description': hero.get('description'),
            'modified': hero.get('modified'),
            'thumbnail': hero.get('thumbnail'),
            'resourceURI': hero.get('resourceURI')
        }

    async def collect_comics_info(self, hero_id):
        comics_list = await marvel_api.fetch_comics_by_hero_id(hero_id)
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
        return changed_comics_list

    async def collect_events_info(self, hero_id):
        events_list = await marvel_api.fetch_events_by_hero_id(hero_id)
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
        return changed_events_list

    async def collect_creators_info(self, comics_list):
        creators_list = []
        for comics in comics_list:
            creators = await marvel_api.fetch_comics_creators(comics['id'])
            if len(creators) > 0:
                creators_list.append(creators[0])
        changed_creator_list = []
        for creator in creators_list:
            changed_creator_list.append({
                'id': creator.get('id'),
                'fullName': creator.get('fullName'),
                'resourceURI': creator.get('resourceURI'),
                'modified': creator.get('modified'),
                'thumbnail': creator.get('thumbnail'),
                'urls': creator.get('urls'),
            })
        return changed_creator_list

    async def collect_full(self):
        hero = await self.collect_hero_info()
        full_dict = {}
        if hero:
            comics = await self.collect_comics_info(hero['id'])
            events = await self.collect_events_info(hero['id'])
            creators = await self.collect_creators_info(comics)
            full_dict.update({
                'hero': hero,
                'comics': comics,
                'events': events,
                'creators': creators,
            })
        return full_dict
