from django.contrib import admin

from .models import CertificationQuestion
from .models import MongleGrade as MogleGradeModel
from .models import MongleLevel
from .models import Report as ReportModel
from .models import ReportedUser as ReportedUserModel
from .models import User as UserModel
from .models import UserProfile as UserProfileModel
from .models import UserProfileCategory as UserProfileCategoryModel

# Register your models here.
admin.site.register(UserModel)
admin.site.register(MongleLevel)
admin.site.register(UserProfileModel)
admin.site.register(ReportModel)
admin.site.register(ReportedUserModel)
admin.site.register(UserProfileCategoryModel)
admin.site.register(MogleGradeModel)
admin.site.register(CertificationQuestion)
