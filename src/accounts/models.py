from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.

# Custom User Manager class that inherits from BaseUserManager
class TechnoUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user with an email and password."""
        # Ensure that the email is provided
        if not email:
            raise ValueError("The Email field must be set")

        # Normalize the email to ensure it's in a standard format (lowercase)
        email = self.normalize_email(email)

        # Create a new user
        user = self.model(email=email, **extra_fields)

        # Hash the password using the set_password method
        user.set_password(password)

        user.save(using=self._db)
        return  user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with an email and password."""
        # Set default values for staff and superuser status
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        # Use the create_user method to create the superuser
        return self.create_user(email, password, **extra_fields)

# Custom User model class that inherits from AbstractBaseUser and PermissionsMixin
class TechnoUser(AbstractBaseUser, PermissionsMixin):
    # Define fields for the custom user model
    email = models.EmailField(unique=True)
    pseudonym = models.CharField(max_length=12, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Attach the TechnoUserManager to the TechnoUser model for managing users
    objects = TechnoUserManager()

    USERNAME_FIELD = 'email'

    #Validation of the pseudonym field
    def clean_pseudonym(self):
        if not self.pseudonym.isalnum():
            raise ValidationError("The pseudonym must contain only letters and numbers.")

    # General clean method for future specific needs
    def clean(self):
        super().clean()
        self.clean_pseudonym()

    # String representation of the user object, returning the email
    def __str__(self):
        return self.email
