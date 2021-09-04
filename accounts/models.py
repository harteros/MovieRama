from django.contrib.auth.models import User


# Create your models here.
def get_name(self):
    """
        Returns a string based on :model:`auth.User` first name and last name
    """
    return '{} {}'.format(self.first_name, self.last_name)


User.add_to_class("__str__", get_name)
