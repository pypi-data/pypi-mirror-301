from pydantic import BaseModel
from typing import Optional
from flask import url_for


class Link(BaseModel):
    rel: str
    type: str
    title: Optional[str]
    href: str


def make_link(rel: str, route: str, title: Optional[str] = None, type: str = "application/json", **args):
    return Link(rel=rel, type=type, title=title, href=url_for(route, **args, _external=True))
