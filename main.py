import aiohttp_jinja2
import jinja2
from aiohttp import web

from app import setting
from app.routes import routes

app = web.Application()

for route in routes:
    app.router.add_route(**route)

aiohttp_jinja2.setup(
    app, loader=jinja2.FileSystemLoader(setting.TEMPLATE_PATH)
)

web.run_app(app)
