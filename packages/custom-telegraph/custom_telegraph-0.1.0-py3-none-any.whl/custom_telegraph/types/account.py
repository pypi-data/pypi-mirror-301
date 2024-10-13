from .base import Type


class Account(Type):
    def __init__(self, short_name=None, author_name=None, author_url=None, auth_url=None, page_count=None):
        self.short_name: str | None = short_name
        self.author_name: str | None = author_name
        self.author_url: str | None = author_url
        self.auth_url: str | None = auth_url
        self.page_count: int | None = page_count
