import aiohttp_jinja2
import jinja2
from aiohttp import web

from app import setting
from app import routes

app = web.Application()
routes.index(app)
routes.get_hero(app)
aiohttp_jinja2.setup(
    app, loader=jinja2.FileSystemLoader(setting.TEMPLATE_PATH)
)
web.run_app(app)
