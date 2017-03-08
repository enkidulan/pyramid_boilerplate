import transaction


def test_user_is_redirected_to_newest_post(
        browser, site, navigator, fakefactory, dbsession):

    with transaction.manager:
        fakefactory.PostFactory.create_batch(2, published_at='2016-12-30')
        post = fakefactory.PostFactory(published_at='2016-12-31')
        dbsession.expunge_all()

    navigator().navigate(site, check_if_navigated=False)

    assert browser.is_text_present(post.title)
    assert browser.url.endswith('/posts/' + post.slug)


def test_user_sees_only_published_posts(
        browser, site, navigator, fakefactory, dbsession):

    with transaction.manager:
        fakefactory.PostFactory.create_batch(2, published_at='2016-12-30')
        post = fakefactory.PostFactory(published_at='2016-12-31')
        dbsession.expunge_all()
    raise
    navigator().navigate(site, check_if_navigated=False)

    assert browser.is_text_present(post.title)
    assert browser.url.endswith('/posts/' + post.slug)
