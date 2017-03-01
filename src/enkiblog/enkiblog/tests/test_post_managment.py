import transaction


def test_create_post(web_server, browser, dbsession, fakefactory):

    with transaction.manager:
        user = fakefactory.AdminFactory()
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

    b.find_by_css("#nav-admin").click()
    assert b.is_element_present_by_css("#admin-main")

    b.find_by_css("#btn-panel-add-posts").click()
    assert b.is_text_present("Add new post")

    post = fakefactory.PostFactory.build()

    b.fill("title", post.title)
    b.fill("descriptions", post.description)
    b.fill("body", post.body)

    b.find_by_name("add").click()
    assert b.is_text_present("Item added")
    assert b.is_text_present(post.title)
    # assert b.is_text_present(post.description)
    # assert b.is_text_present(post.body)

    # import pdb; pdb.set_trace()


def test_list_posts(web_server, browser, dbsession, fakefactory):
    raise


def test_edit_post(web_server, browser, dbsession, fakefactory):
    raise


def test_delete_post(web_server, browser, dbsession, fakefactory):
    raise
