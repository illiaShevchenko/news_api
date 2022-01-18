from rest_framework import serializers

from news_app.models import Company, Post
from django.contrib.auth import get_user_model

User = get_user_model()


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = '__all__'


class UserBigSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = 'email', 'password', 'first_name',\
                 'last_name',  'user_type', 'company',\
                 'avatar', 'telephone_number',


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'


class UserNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = 'name'


class PostUserSmallSerializer(serializers.ModelSerializer):

    user = UserNameSerializer(read_only=True, many=False)

    class Meta:
        model = Post
        fields = '__all__'


class CompanyUserSmallSerializer(serializers.ModelSerializer):

    company = CompanySerializer(read_only=True, many=False)

    class Meta:
        model = User
        fields = '__all__'

            # 'email', 'password', 'first_name',\
            #      'last_name',  'user_type', 'company',\
            #      'avatar', 'telephone_number',


class UsersDetailsSerializer(serializers.ModelSerializer):

    company = CompanySerializer(read_only=True, many=False)

    class Meta:
        model = User
        fields = '__all__'


class CompaniesDetailsSerializer(serializers.ModelSerializer):

    user = CompanyUserSmallSerializer(read_only=True, many=False)

    class Meta:
        model = Post
        fields = '__all__'
