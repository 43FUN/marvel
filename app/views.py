import aiohttp_jinja2
import aiohttp
import datetime
import json
from aiohttp import web

from app.utils import get_hash, generate_info
from app import setting


class IndexView(web.View):
    @aiohttp_jinja2.template('index.html')
    async def get(self):
        return {}


class GetHeroView(web.View):

    async def get(self):
        name = self.request.query.get('name')
        await generate_info(name)
        return web.json_response({})
