from app import views


def index(app):
    app.router.add_route(
        'GET', '/', views.IndexView, name='index'
    )


def get_hero(app):
    app.router.add_route(
        'GET', '/get_hero', views.GetHeroView, name='get_hero'
    )
