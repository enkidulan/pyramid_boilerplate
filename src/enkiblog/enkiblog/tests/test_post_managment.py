import transaction
from uuid import uuid4


def test_create_post(site, navigator, admin_user, fakefactory):

    post = fakefactory.PostFactory.build()

    navigator = navigator(user=admin_user)
    navigator.submit(
        site.admin_menu.posts.add_post_page.add_post_form,
        data={
            "title": post.title,
            "descriptions": post.description,
            "body": post.body},
        status='success',
    )


def test_post_create_validation(site, navigator, admin_user, fakefactory):

    post = fakefactory.PostFactory.build()

    navigator = navigator(user=admin_user)
    navigator.submit(
        site.admin_menu.posts.add_post_page.add_post_form,
        data={
            "title": '',
            "descriptions": post.description,
            "body": post.body},
        status='validation_error',
    )


def test_delete_post(navigator, admin_user, site, dbsession, fakefactory):

    with transaction.manager:
        fakefactory.PostFactory()
    navigator = navigator(user=admin_user)

    navigator.navigate(site.admin_menu.posts)

    assert navigator.browser.is_text_present("Total 1 item")

    navigator.browser.find_by_css('.btn-crud-listing-delete').click()
    assert navigator.browser.is_text_present("Confirm delete")

    navigator.browser.find_by_css('#btn-delete-yes').click()
    assert navigator.browser.is_text_present("Deleted")

    navigator.navigate(site.admin_menu.posts)
    assert navigator.browser.is_text_present("No items")


def test_list_posts(site, navigator, admin_user, fakefactory, dbsession):

    with transaction.manager:
        fakefactory.PostFactory.create_batch(size=30)

    navigator = navigator(user=admin_user)
    navigator.navigate(site.admin_menu.posts)
    assert navigator.browser.is_text_present("Total 30 items")


def test_edit_post(site, navigator, admin_user, fakefactory, dbsession):
    with transaction.manager:
        fakefactory.PostFactory()
        dbsession.expunge_all()

    navigator = navigator(user=admin_user)
    navigator.navigate(site.admin_menu.posts)

    navigator.browser.find_by_css('.btn-crud-listing-edit').click()
    assert navigator.browser.is_text_present("Editing")

    text = uuid4().hex
    navigator.browser.fill("title", text)
    navigator.browser.find_by_name("save").click()

    assert navigator.browser.is_text_present("Changes saved.")
    assert navigator.browser.is_text_present(text)


# def test_create_post_plain(web_server, browser, admin_user, fakefactory):

#     user = admin_user

#     # Direct Splinter browser to the website
#     b = browser
#     b.visit(web_server)

#     # This link should be in the top navigation
#     b.find_by_css("#nav-sign-in").click()

#     # Link gives us the login form
#     assert b.is_element_present_by_css("#login-form")

#     b.fill("username", user.email)
#     b.fill("password", user._fb_excluded.password)
#     b.find_by_name("login_email").click()

#     # After login we see a profile link to our profile
#     assert b.is_element_present_by_css("#nav-logout")

#     b.find_by_css("#nav-admin").click()
#     assert b.is_element_present_by_css("#admin-main")

#     b.find_by_css("#btn-panel-add-posts").click()
#     assert b.is_text_present("Add new post")

#     post = fakefactory.PostFactory.build()

#     b.fill("title", post.title)
#     b.fill("descriptions", post.description)
#     b.fill("body", post.body)

#     b.find_by_name("add").click()
#     assert b.is_text_present("Item added")
#     assert b.is_text_present(post.title)
#     # assert b.is_text_present(post.description)
#     # assert b.is_text_present(post.body)
