from app import views


routes = (
    dict(
        method='GET',
        path='/',
        handler=views.IndexView,
        name='index',
    ),
    dict(
        method='GET',
        path='/get_hero',
        handler=views.GetHeroView,
        name='get_hero',
    ),
)

