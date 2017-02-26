from websauna.system.http import Request
from websauna.system.core.route import simple_route

from . import models


@simple_route("/", route_name="home", renderer='enkiblog/posts.html')
@simple_route("/posts", route_name="posts", renderer='enkiblog/posts.html')
def posts(request: Request):
    """Render site homepage."""
    post = request.dbsession.query(
        models.Post).order_by(models.Post.published_at.desc()).first()
    return {"post": post, "project": "enkiblog"}
