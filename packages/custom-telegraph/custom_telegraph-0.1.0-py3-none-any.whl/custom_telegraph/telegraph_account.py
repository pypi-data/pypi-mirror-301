from telegraph import Telegraph
from .types import *


class TelegraphAccount(Telegraph):
    """ telegraph library helper. Check Telegraph package for more details """
    def create_account(self, short_name, author_name=None, author_url=None,
                       replace_token=True) -> Account:
        """ Create a new Telegraph account

        :param short_name: Account name, helps users with several
                           accounts remember which they are currently using.
                           Displayed to the user above the "Edit/Publish"
                           button on Telegra.ph, other users don't see this name
        :param author_name: Default author name used when creating new articles
        :param author_url: Default profile link, opened when users click on the
                           author's name below the title. Can be any link,
                           not necessarily to a Telegram profile or channels
        :param replace_token: Replaces current token to a new user's token
        """
        _account_info = super().create_account(short_name=short_name,
                                               author_name=author_name,
                                               author_url=author_url,
                                               replace_token=replace_token)
        return Account(**_account_info)

    def get_account_info(self) -> Account:
        """
        Get information about a Telegraph account
        :return: class<Account>
        """
        _account_info = super().get_account_info(["short_name", "author_name", "author_url", "auth_url", "page_count"])
        return Account(**_account_info)

    def edit_account_info(self, short_name=None, author_name=None, author_url=True) -> Account:
        """ Update information about a Telegraph account.
            Pass only the parameters that you want to edit

        :param short_name: Account name, helps users with several
                           accounts remember which they are currently using.
                           Displayed to the user above the "Edit/Publish"
                           button on Telegra.ph, other users don't see this name
        :param author_name: Default author name used when creating new articles
        :param author_url: Default profile link, opened when users click on the
                           author's name below the title. Can be any link,
                           not necessarily to a Telegram profile or channels
        :return: class<Account>
        """
        _account_info = super().edit_account_info(short_name=short_name, author_name=author_name, author_url=author_url)
        return Account(**_account_info)

    def create_page(self, title, content=None, html_content=None,
                    author_name=None, author_url=None, return_content=False) -> Page:
        """ Create a new Telegraph page

        :param title: Page title
        :param content: Content in nodes list format (see doc)
        :param html_content: Content in HTML format
        :param author_name: Author name, displayed below the article's title
        :param author_url: Profile link, opened when users click on
                           the author's name below the title
        :param return_content: If true, a content field will be returned
        :return: class<Page>
        """
        _page = super().create_page(title=title,
                                    content=content,
                                    html_content=html_content,
                                    author_name=author_name,
                                    author_url=author_url,
                                    return_content=return_content)
        return Page(**_page)

    def get_page(self, path, return_content=True, return_html=True) -> Page:
        """ Get a Telegraph page

        :param path: Path to the Telegraph page (in the format Title-12-31,
                     i.e. everything that comes after https://telegra.ph/)
        :param return_content: If true, content field will be returned
        :param return_html: If true, returns HTML instead of Nodes list
        :return: class<Page>
        """
        _page = super().get_page(path, return_content=return_content, return_html=return_html)
        return Page(**_page)

    def edit_page(self, path, title, content=None, html_content=None,
                    author_name=None, author_url=None, return_content=False) -> Page:
        """ Edit an existing Telegraph page

        :param path: Path to the page
        :param title: Page title
        :param content: Content in nodes list format (see doc)
        :param html_content: Content in HTML format
        :param author_name: Author name, displayed below the article's title
        :param author_url: Profile link, opened when users click on
                           the author's name below the title
        :param return_content: If true, a content field will be returned
        :return: class<Page>
        """
        _page = super().edit_page(path=path,
                                  title=title,
                                  content=content,
                                  html_content=html_content,
                                  author_name=author_name,
                                  author_url=author_url,
                                  return_content=return_content)
        return Page(**_page)

    def get_page_list(self, offset=0, limit=50) -> PageList:
        """ Get a list of pages belonging to a Telegraph account
            sorted by most recently created pages first

        :param offset: Sequential number of the first page to be returned
                       (default = 0)
        :param limit: Limits the number of pages to be retrieved
                      (0-200, default = 50)
        :return: class<PageList>
        """
        _page_list = super().get_page_list(offset=offset, limit=limit)
        pages = []
        for _page in _page_list['pages']:
            pages += [Page(**_page)]
        _page_list['pages'] = pages
        return PageList(**_page_list)

    def get_views(self, path, year=None, month=None, day=None, hour=None) -> int:
        """ Get the number of views for a Telegraph article

        :param path: Path to the Telegraph page
        :param year: Required if month is passed. If passed, the number of
                     page views for the requested year will be returned
        :param month: Required if day is passed. If passed, the number of
                      page views for the requested month will be returned
        :param day: Required if hour is passed. If passed, the number of
                    page views for the requested day will be returned
        :param hour: If passed, the number of page views for
                     the requested hour will be returned
        """
        views = super().get_views(path=path, year=year, month=month, day=day, hour=hour)
        return views['views']

    def upload_file(self, f):
        """
        Doesn't work cos telegraph doesn't allow to upload files anymore. Upload photos on your own server
        """
        pass
