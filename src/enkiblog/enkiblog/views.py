from pyramid.httpexceptions import HTTPFound

from websauna.system.http import Request
from websauna.system.core.route import simple_route

from . import models


@simple_route("/", route_name="home")
def home(request: Request):
    post = request.dbsession.query(
        models.Post).order_by(models.Post.published_at.desc()).first()
    return HTTPFound(request.route_url("posts", slug=post.slug))


@simple_route("/posts/{slug}", route_name="posts", renderer='enkiblog/posts.html')
def posts(request: Request):
    slug = request.matchdict["slug"]
    post = request.dbsession.query(models.Post).filter_by(slug=slug).first()
    return {"post": post, "project": "enkiblog"}
