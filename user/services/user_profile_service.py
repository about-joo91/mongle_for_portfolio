from typing import Dict

from user.models import UserProfile as UserProfileModel
from user.serializers import UserProfileSerializer


def get_user_profile_data(user_id: int) -> Dict:
    user_profile = (
        UserProfileModel.objects.filter(user_id=user_id)
        .select_related("user__monglegrade__mongle_level")
        .prefetch_related("categories")
        .get()
    )
    return UserProfileSerializer(user_profile).data


def update_user_profile_data(user_id: int, update_data: Dict) -> None:
    cur_userprofile = UserProfileModel.objects.filter(user_id=user_id).get()
    user_profile_serializer = UserProfileSerializer(cur_userprofile, data=update_data, partial=True)
    user_profile_serializer.is_valid(raise_exception=True)
    user_profile_serializer.save()
