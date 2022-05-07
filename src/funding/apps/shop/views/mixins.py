from funding.apps.core.exceptions import (
    UserAlreadyParticipateError,
    PostCannotParticipateError,
    PosterCannotParticipateError,
    PostDoesNotExistError,
    UserCannotModifyPostError,
)

from django.core.exceptions import ObjectDoesNotExist
from ..models import *


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
    
    def validate_poster(self, user_id, post_id):
        try:
            Post.objects.get(pk=post_id, poster=user_id)
            pass
        except ObjectDoesNotExist:
            raise UserCannotModifyPostError(user_id, post_id)


class ShopCRUDMixin:
    def get_item_by_post_id_to_participate(self, post_id):
        try:
            post = Post.objects.get(pk=post_id, status="FUNDING")
            return post.item
        except ObjectDoesNotExist:
            raise PostCannotParticipateError(post_id)
    
    def get_active_post(self, post_id):
        try:
            post = Post.objects.get(pk=post_id, status__in=['FUNDING', 'SUCCESS', 'CLOSE'])
            return post
        except ObjectDoesNotExist:
            raise PostDoesNotExistError(post_id)
    
    def get_item_by_post_id(self, post_id):
        try:
            post = Post.objects.get(pk=post_id)
            return post.item
        except ObjectDoesNotExist:
            raise PostDoesNotExistError(post_id)
    
    def delete_post(self, post_id):
        """
        펀딩 중인 상품을 삭제할 수 없음
        """
        try:
            Post.objects.get(pk=post_id, status__in=['SUCCESS', 'CLOSE']).delete()
        except ObjectDoesNotExist:
            raise PostDoesNotExistError(post_id)
    
    def read_posts(self, search=None):
        posts = Post.objects.exclude(status='CANCEL')
        if search:
            posts = posts.filter(title__startswith=search).exclude(status='CANCEL')
        return posts

class ShopMixin(
    ShopValidationMixin,
    ShopCRUDMixin
):
    pass
