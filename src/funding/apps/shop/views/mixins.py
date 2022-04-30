from funding.apps.core.views import IntegrationMixin as CoreIntegrationMixin
from funding.apps.core.exceptions import (
    DoesNotExistedUserPocketError,
    UserAlreadyParticipateError,
)

from django.core.exceptions import ObjectDoesNotExist
from funding.apps.user.models import Pocket
from ..models import Participant


class ShopValidationMixin:
    def get_valid_user_pocket(self, user_id):
        try:
            pocket = Pocket.objects.get(user_id=user_id)
            return pocket
        except ObjectDoesNotExist:
            raise DoesNotExistedUserPocketError(user_id)
    
    def validate_unparticipated_user(self, user_id, post_id):
        try:
            participant = Participant.objects.get(user_id=user_id, post_id=post_id)
            raise UserAlreadyParticipateError(user_id, post_id)
        except ObjectDoesNotExist:
            return None
    

class ShopCRUDMixin:
    pass


class IntegrationMixin(
    ShopValidationMixin,
    ShopCRUDMixin,
    CoreIntegrationMixin
):
    pass
