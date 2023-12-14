from fastapi import APIRouter, Request
from starlette.templating import Jinja2Templates

from src.services.analytics.analytics_queries_bd.flight_population_raw import population_of_flights
from src.services.logic.logic_population_flight import create_plot

router = APIRouter()
templates = Jinja2Templates(directory='templates')


@router.get('/popularity_routes', name='popularity_routes')
async def get_popularity_routes(request: Request):
    polpularity_flights = await population_of_flights()
    print({'polpularity_flights': polpularity_flights})
    fig = create_plot(polpularity_flights)
    print({'fig': fig})
    fig.show()
    graph_html = fig.to_html(full_html=False)
    # print({'graph_html': graph_html})
    context = {
        'request': request,
        'graph': graph_html,
    }
    return templates.TemplateResponse(
        '/analytics/flight_population.html',
        context=context,
    )
