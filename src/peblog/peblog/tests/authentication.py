from .base import BaseTest, dummy_request
from . import fakefactory


class TestAuthentication(BaseTest):

    def test_faker(self):
        user = fakefactory.UserFactory()
        assert user.id
