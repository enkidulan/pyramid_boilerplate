import transaction

from sqlalchemy.orm.session import Session
from splinter.driver import DriverAPI

from websauna.system import Initializer

from . import fakefactory


def test_login(web_server: str, registry, browser: DriverAPI, dbsession: Session, init: Initializer):

    from .fixtures import db_session_proxy
    db_session_proxy.session = dbsession

    from websauna.tests.utils import create_user
    import transaction

    with transaction.manager:
        user = fakefactory.AdminFactory()
        dbsession.expunge_all()
        # create_user(dbsession, registry, email='email1@email.com', password='qwerty', admin=True)
    # Direct Splinter browser to the website
    b = browser
    b.visit(web_server)

    # This link should be in the top navigation
    b.find_by_css("#nav-sign-in").click()

    # Link gives us the login form
    assert b.is_element_present_by_css("#login-form")

    b.fill("username", user.email)
    b.fill("password", user._fb_excluded.password)
    b.find_by_name("login_email").click()

    # After login we see a profile link to our profile
    assert b.is_element_present_by_css("#nav-logout")
