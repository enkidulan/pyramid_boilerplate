import pytest
import re
from functools import partial
import transaction


@pytest.fixture()
def fakefactory(dbsession):
    # TODO: Make thread-safe
    from . import fakefactory
    fakefactory.db_session_proxy.session = dbsession
    try:
        yield fakefactory
    finally:
        fakefactory.db_session_proxy.session = None


@pytest.fixture()
def admin_user(fakefactory, dbsession):
    with transaction.manager:
        user = fakefactory.AdminFactory()
        dbsession.expunge_all()
    return user


@pytest.fixture()
def navigator(browser, site):
    return partial(
        Navigator,
        browser=browser,
        login_form=getattr(site, 'login_form', None)
    )


@pytest.fixture()
def site(web_server):
    return site_constructor(web_server)


def convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class Navigator:
    # make proper visitor

    def __init__(self, browser, user=None, login_form=None):
        self.browser = browser
        self.user = user
        self.login_form = login_form

    def navigate(self, page):
        if self.user is not None and not self.login_form.is_user_loged_in(navigator=self, user=self.user):
                self.login_form.parent.navigate(navigator=self)
                self.login_form.navigate(navigator=self)
                self.login_form.submit(navigator=self, data={'user': self.user})
        page._navigate(navigator=self)

    def submit(self, form, data, status='success'):
        assert form.type == 'form'
        assert isinstance(data, dict)

        form.submit(navigator=self, data=data)
        getattr(form, 'check_' + status)(navigator=self, data=data)

        # if status == 'success':
        #     form.parrent.pages.add()

        return form


class SiteNode:

    def __init__(self):
        self.parent = None
        self.nodes = {}
        self.name = convert(self.__class__.__name__)

    def add(self, node):
        assert node.name not in self.nodes  # for having explicit ovverinding
        self.nodes[node.name] = node
        node.parent = self
        setattr(self, node.name, node)

    def navigate(self, navigator):
        raise

    def _navigate(self, navigator):
        # if self.is_current_context(navigator):
        #     return
        if self.parent:
            navigator.navigate(self.parent)
        self.navigate(navigator)
        assert self.is_current_context(navigator)


class SiteRoot(SiteNode):
    type = 'page'

    def __init__(self, url):
        super().__init__()
        self.url = url

    def is_current_context(self, navigator):
        return navigator.browser.url.strip('/') == self.url.strip('/')

    def navigate(self, navigator):
        navigator.browser.visit(self.url)


class AdminMenu(SiteNode):
    type = 'page'

    def is_current_context(self, navigator):
        return navigator.browser.is_element_present_by_css("#admin-main")

    def navigate(self, navigator):
        navigator.browser.find_by_css("#nav-admin").click()


class Posts(SiteNode):  # duplicates AdminMenu for simlicity sake
    type = 'entery'

    def is_current_context(self, navigator):
        return navigator.browser.is_text_present("All posts")

    def navigate(self, navigator):
        navigator.browser.find_by_css('#btn-panel-list-posts').click()


class AddPostPage(SiteNode):
    type = 'page'

    def is_current_context(self, navigator):
        return navigator.browser.is_text_present("Add new post")

    def navigate(self, navigator):
        navigator.browser.find_by_css("#btn-crud-add").click()


class AddPostForm(SiteNode):
    type = 'form'

    def is_current_context(self, navigator):
        return navigator.browser.is_text_present("Add new post")

    def navigate(self, navigator):
        pass

    def submit(self, navigator, data):

        navigator.navigate(self)

        navigator.browser.fill("title", data['title'])
        navigator.browser.fill("descriptions", data['descriptions'])
        navigator.browser.fill("body", data['body'])

        navigator.browser.find_by_name("add").click()

    def check_success(self, navigator, data):

        # After login we see a profile link to our profile
        assert navigator.browser.is_text_present("Item added")
        assert navigator.browser.is_text_present(data['title'])

    def check_validation_error(self, navigator, data):
        assert navigator.browser.is_text_present("There was a problem with your submission")


class LoginForm(SiteNode):
    type = 'form'

    def is_current_context(self, navigator):
        return navigator.browser.is_element_present_by_css("#login-form")

    def navigate(self, navigator):
        navigator.browser.find_by_css("#nav-sign-in").click()

    def submit(self, navigator, data):

        user = data['user']
        navigator.browser.fill("username", user.email)
        navigator.browser.fill("password", user._fb_excluded.password)
        navigator.browser.find_by_name("login_email").click()

        assert self.is_user_loged_in(navigator, user)

    def is_user_loged_in(self, navigator, user):
        return navigator.browser.is_element_present_by_css("#nav-logout")


def site_constructor(url):
    site = SiteRoot(url)
    site.add(AdminMenu())
    site.add(LoginForm())
    site.admin_menu.add(Posts())
    site.admin_menu.posts.add(AddPostPage())
    site.admin_menu.posts.add_post_page.add(AddPostForm())
    return site
