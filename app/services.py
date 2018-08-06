from app import marvel_api


class GenerateHeroInfo:

    def __init__(self, name):
        self.name = name

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

        raw_comicses_info = await marvel_api.get_comics_by_hero_id(hero['id'])
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

        raw_events_info = await marvel_api.get_events_by_hero_id(hero['id'])
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

        creators_list = []
        for comics in comics_list:
            raw_creators = await marvel_api.get_comics_creators(comics['id'])
            creators = raw_creators.get('data', {}).get('results', [])
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
        data['creators'] = changed_creator_list

        return data

    async def get_full_info(self):
        raw_hero_info = await marvel_api.get_hero_by_name(self.name)
        hero_list = raw_hero_info.get('data', {}).get('results', [])
        hero = hero_list[0] if hero_list else None
        return await self.json_generate(hero) if hero else {}
