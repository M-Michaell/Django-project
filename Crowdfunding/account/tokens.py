from django.contrib.auth.tokens import PasswordResetTokenGenerator

class EmailTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return 'activate_email' + str(user.pk) + str(timestamp) + str(user.is_active)

account_activation_token = EmailTokenGenerator()




# class PassTokenGenerator(PasswordResetTokenGenerator):
#     def _make_hash_value(self, user, timestamp):
#         return 'activate_email' + str(user.pk) + str(timestamp) + str(user.is_active)

# password_activation_token = PassTokenGenerator()
