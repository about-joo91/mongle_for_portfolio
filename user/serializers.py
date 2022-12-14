from rest_framework import serializers

from .models import MongleGrade, MongleLevel
from .models import User as UserModel
from .models import UserProfile as UserProfileModel

MONGLE_GRADE_LIST = [0, 200, 600, 1200, 2500]


class UserSignupSerializer(serializers.ModelSerializer):
    def validate(self, data):
        condition = all(x not in ["!", "@", "#", "$", "%", "^", "&", "*", "_"] for x in data["password"])
        if len(data["username"]) < 4:
            raise serializers.ValidationError("아이디는 4자 이상 입력해주세요.")

        elif len(data["nickname"]) == 0:
            raise serializers.ValidationError("닉네임을 입력해주세요.")
        elif str(data["certification_question"]) == "None":
            raise serializers.ValidationError("본인인증 질문을 선택해주세요.")
        elif len(data["certification_answer"]) == 0:
            raise serializers.ValidationError("본인인증 답변을 입력해주세요.")
        elif UserModel.objects.filter(nickname=data["nickname"]).exists():
            raise serializers.ValidationError("중복된 닉네임이 존재합니다.")

        elif len(data["password"]) < 8 or condition:
            raise serializers.ValidationError("비밀번호는 8자 이상 특수문자 포함해 입력해주세요")
        return data

    def create(self, *args, **kwargs):
        user = super().create(*args, **kwargs)
        p = user.password
        user.set_password(p)
        user.save()
        UserProfileModel(user=user).save()
        mongle_level = MongleLevel.objects.get(id=1)
        MongleGrade(user=user, mongle_level=mongle_level).save()
        return user

    # def update(ser, *args, **kwargs):
    #     user = super().create(*args, **kwargs)
    #     p = user.password
    #     user.set_password(p)
    #     user.save()
    #     return user

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
                continue

            setattr(instance, key, value)
        instance.save()
        return instance

    class Meta:
        model = UserModel
        fields = "__all__"


class NewPasswordSerializer(serializers.ModelSerializer):
    def validate(self, data):
        condition = all(x not in ["!", "@", "#", "$", "%", "^", "&", "*", "_"] for x in data["password"])

        if len(data["password"]) < 8 or condition:
            raise serializers.ValidationError("비밀번호는 8자 이상 특수문자 포함해 입력해주세요")
        return data

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
                continue

            setattr(instance, key, value)
        instance.save()
        return instance

    class Meta:
        model = UserModel
        fields = ["password"]


class MongleGradeSerializer(serializers.ModelSerializer):

    mongle_image = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()
    left_grade = serializers.SerializerMethodField()

    def get_mongle_image(self, obj):
        return obj.mongle_level.mongle_image

    def get_level(self, obj):
        return obj.mongle_level.level

    def get_left_grade(self, obj):
        return int(MONGLE_GRADE_LIST[obj.mongle_level.level]) - obj.grade

    class Meta:
        model = MongleGrade
        fields = ["mongle_image", "level", "grade", "left_grade"]


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    mongle_grade = serializers.SerializerMethodField(read_only=True)
    certification_question_id = serializers.SerializerMethodField(read_only=True)
    certification_answer = serializers.SerializerMethodField(read_only=True)

    def get_categories(self, obj):
        return [{"id": cate.id, "cate_name": cate.category.cate_name} for cate in obj.userprofilecategory_set.all()]

    def get_mongle_grade(self, obj):
        return MongleGradeSerializer(obj.user.monglegrade).data

    def get_user(self, obj):
        return obj.user.nickname

    def get_certification_question_id(self, obj):
        if obj.user.certification_question:
            return obj.user.certification_question.id
        return None

    def get_certification_answer(self, obj):
        return obj.user.certification_answer

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    class Meta:
        model = UserProfileModel
        fields = [
            "user",
            "description",
            "mongle_grade",
            "fullname",
            "profile_img",
            "categories",
            "certification_question_id",
            "certification_answer",
        ]


class UserCertificationSerializer(serializers.ModelSerializer):
    certification_question = serializers.SerializerMethodField()

    def get_certification_question(self, obj):
        return obj.certification_question.certification_question

    class Meta:
        model = UserModel
        fields = ["username", "certification_question"]
