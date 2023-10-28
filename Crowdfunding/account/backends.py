from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        user = None
        try:
            user = UserModel.objects.get(email=username)
        except:
            if not user :
                return user
        if user.check_password(password):
            print('p',user)
            return user
        else:
            return user