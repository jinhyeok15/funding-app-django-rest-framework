from funding.apps.core.exceptions import (
    UserAlreadyParticipateError,
    PostCannotParticipateError,
    PosterCannotParticipateError,
    PostDoesNotExistError,
)

from django.core.exceptions import ObjectDoesNotExist
from ..models import *
from funding.apps.user.models import User


class ShopValidationMixin:
    def validate_unparticipated_user(self, user_id, post_id):
        try:
            Participant.objects.get(user=user_id, post_id=post_id)
            raise UserAlreadyParticipateError(user_id, post_id)
        except ObjectDoesNotExist:
            pass
    
    def validate_user_not_poster(self, user_id, post_id):
        try:
            Post.objects.get(pk=post_id, poster=user_id)
            raise PosterCannotParticipateError(user_id)
        except ObjectDoesNotExist:
            pass


class ShopCRUDMixin:
    def get_item_by_post_id_to_participate(self, post_id):
        try:
            post = Post.objects.get(pk=post_id, status="FUNDING")
            return post.item
        except ObjectDoesNotExist:
            raise PostCannotParticipateError(post_id)
    
    def get_activate_post(self, post_id):
        try:
            post = Post.objects.get(pk=post_id, status__in=['FUNDING', 'SUCCESS', 'CLOSE'])
            return post
        except ObjectDoesNotExist:
            raise PostDoesNotExistError(post_id)

class ShopMixin(
    ShopValidationMixin,
    ShopCRUDMixin
):
    pass
