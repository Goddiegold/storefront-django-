from djoser.serializers import UserCreateSerializer
# from store.models import Customer

class AppUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = ['id', 'username', 'password', 'email','first_name', 'last_name']


class UserSerializer(UserCreateSerializer):
    # def save(self, **kwargs):
    #     user =  super().save(**kwargs)
    #     Customer.objects.create(user=user)

    class Meta(UserCreateSerializer.Meta):
        fields = ['id','username','email', 'first_name', 'last_name']