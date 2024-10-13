from .base import Type
from .page import Page


class PageList(Type):
    def __init__(self, total_count, pages):
        self.total_count: int = total_count
        self.pages: list[Page] = pages
