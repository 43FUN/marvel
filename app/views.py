import aiohttp_jinja2
from aiohttp import web

from app.services import HeroDataCollector


class IndexView(web.View):
    @aiohttp_jinja2.template('index.html')
    async def get(self):
        return {}


class GetHeroView(web.View):

    async def get(self):
        name = self.request.query.get('name')
        if not isinstance(name, str):
            return web.HTTPBadRequest()
        response = await HeroDataCollector(name).collect_full()
        return web.json_response(response)
