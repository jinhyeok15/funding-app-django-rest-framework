from funding.apps.core.exceptions import (
    DoesNotExistedUserPocketError,
)

from django.core.exceptions import ObjectDoesNotExist
from funding.apps.user.models import Pocket


class UserValidationMixin:
    pass


class UserCRUDMixin:
    def get_valid_user_pocket(self, user_id):
        try:
            pocket = Pocket.objects.get(user_id=user_id)
            return pocket
        except ObjectDoesNotExist:
            raise DoesNotExistedUserPocketError(user_id)


class UserMixin(
    UserValidationMixin,
    UserCRUDMixin
):
    pass
