from django.contrib.auth.tokens import PasswordResetTokenGenerator


class ChangeEmailTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return f"{user.new_email}{user.pk}{timestamp}"


change_email_token_generator = ChangeEmailTokenGenerator()
