import requests
from websauna.system.user import models


def test_provision_card(web_server, dbsession):

    response = requests.get(web_server + "/api/provision")
    assert response.status_code == 404, "Got: {}".format(response.text)

    response = requests.get(web_server)
    assert response.status_code == 200, "Got: {}".format(response.text)


def test_user_creation(dbsession, fakefactory):
    user = fakefactory.UserFactory()
    assert dbsession.query(models.User).count()
    assert user.id
