import requests
from . import fakefactory
from websauna.system.user import models


def test_provision_card(web_server, dbsession):

    response = requests.get(web_server + "/api/provision")
    assert response.status_code == 404, "Got: {}".format(response.text)

    response = requests.get(web_server)
    assert response.status_code == 200, "Got: {}".format(response.text)


def test_dupa(request, factoryshared_dbsession):
    user = fakefactory.UserFactory()
    assert factoryshared_dbsession.query(models.User).count()
    assert user.id
