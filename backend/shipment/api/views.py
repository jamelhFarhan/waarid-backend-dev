from dj_rest_auth.views import LoginView, PasswordResetView
from dj_rest_auth.registration.views import RegisterView

from api.v1.serializers.auth import CustomPasswordResetSerializer


class CustomLoginView(LoginView):
    def get_response(self):
        original_response = super().get_response()
        data = {
            "user_id": self.user.id,
            "role": self.user.role,
            "is_admin": self.user.is_admin,
            "first_name": self.user.first_name,
            "company_name": self.user.company.name,
        }
        original_response.data.update(data)
        #print(data)
        return original_response


class CustomRegisterView(RegisterView):
    def get_response_data(self, user):
        original_response = super().get_response_data(user)
        data = {"user_id": user.id, "role": user.role, "is_admin": user.is_admin}
        original_response.update(data)
        return original_response


class CustomPasswordResetView(PasswordResetView):
    serializer_class = CustomPasswordResetSerializer
