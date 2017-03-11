from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from sqlalchemy import func, desc, select
from sqlalchemy import or_
from itertools import zip_longest

from websauna.system.http import Request
from websauna.system.core.route import simple_route

from enkiblog import models


@simple_route("/", route_name="home", renderer='enkiblog/home.html')
def home(request: Request):
    post = request.dbsession.query(
        models.Post).filter_by(state='published').order_by(models.Post.published_at.desc()).first()
    if post is not None:
        return HTTPFound(request.route_url("posts", slug=post.slug))
    return {}


@simple_route("/posts/{slug}", route_name="posts", renderer='enkiblog/posts.html')
def posts(request: Request):
    dbsession = request.dbsession

    slug = request.matchdict["slug"]

    subl = dbsession.query(models.Post.slug).filter_by(state='published').order_by(models.Post.published_at.desc()).subquery('base_posts')
    neighborhood = dbsession.query(subl.c.slug.label('current'), func.lag(subl.c.slug).over().label('prev'), func.lead(subl.c.slug).over().label('next')).subquery('neighborhood')
    neighbors = dbsession.query(neighborhood).filter(neighborhood.c.current==slug).subquery('neighbors')
    query_post = dbsession.query(models.Post).filter(models.Post.slug==neighbors.c.current)
    posts = query_post.join(neighbors, neighbors.c.current==models.Post.slug).add_columns(neighbors.c.prev, neighbors.c.next).one_or_none()

    if not posts:
        raise HTTPNotFound()

    post, slug_prev, slug_next = posts

    return {"project": "enkiblog", 'post': post, 'slug_prev': slug_prev,' slug_next':  slug_next}
