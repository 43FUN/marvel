import aiohttp_jinja2
from aiohttp import web

from app.services import GenerateHeroInfo


class IndexView(web.View):
    @aiohttp_jinja2.template('index.html')
    async def get(self):
        return {}


class GetHeroView(web.View):

    async def get(self):
        name = self.request.query.get('name')
        if not isinstance(name, str):
            return web.HTTPBadRequest()
        response = await GenerateHeroInfo(name).get_full_info()
        return web.json_response(response)
