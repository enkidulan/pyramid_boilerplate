from websauna.system.http import Request
from websauna.system.core.route import simple_route


# Configure view named home at path / using a template enkiblog/home.html
@simple_route("/", route_name="home", renderer='enkiblog/home.html')
def home(request: Request):
    """Render site homepage."""
    return {"project": "enkiblog"}
