from rest_framework import serializers
from user.models import *

class GetUserSerializer (serializers.ModelSerializer) :
    
    class Meta :
        model = users
        fields = ['id','email','first_name','last_name','avatar']
        # fields = "__all__"

class UserSerializer (serializers.ModelSerializer) :
    
    class Meta :
        model = users
        fields = ['id','email','first_name','last_name','avatar','created_at',
                  'updated_at','deleted_at']
        # fields = "__all__"
