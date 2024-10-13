from .base import Type


class Page(Type):
    def __init__(self, path=None,
                 url=None,
                 title=None,
                 description=None,
                 content=None,
                 views=None,
                 can_edit=None,
                 ):
        self.path: str | None = path
        self.url: str | None = url
        self.title: str | None = title
        self.description: str | None = description
        self.content: str | None = content
        self.views: int | None = views
        self.can_edit: bool | None = can_edit
