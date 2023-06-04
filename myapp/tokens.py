from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six  

# Generate token by inheriting PasswordResetTokenGenerator
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    
    # override the default method
    # This method is responsible for generating a unique hash value based on the user and timestamp
    # Use six.text_type to convert into text
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk)+six.text_type(timestamp)+six.text_type(user.is_email_verified))
        

account_activation_token = AccountActivationTokenGenerator()