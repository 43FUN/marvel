import aiohttp_jinja2
from aiohttp import web

from app.services import generate_info


class IndexView(web.View):
    @aiohttp_jinja2.template('index.html')
    async def get(self):
        return {}


class GetHeroView(web.View):

    async def get(self):
        name = self.request.query.get('name')
        response = await generate_info(name)
        return web.json_response(response)
