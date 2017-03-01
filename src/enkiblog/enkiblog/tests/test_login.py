"""An example login test case."""

import transaction


def test_login(web_server, browser, dbsession, fakefactory):

    with transaction.manager:
        user = fakefactory.UserFactory()
        dbsession.expunge_all()

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
