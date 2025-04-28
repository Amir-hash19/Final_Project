from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, Group
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator
from django.db import models




class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("Phone number is required for regular users")

        email = extra_fields.get("email")
        if email:
            extra_fields["email"] = self.normalize_email(email)

        extra_fields.setdefault("username", None)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        user = self.model(phone=phone, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()    
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Superuser must have a username")

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        email = extra_fields.get("email")
        if email:
            extra_fields["email"] = self.normalize_email(email)

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=80)
    phone = PhoneNumberField(unique=True,region="IR")
    email = models.EmailField(unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    birthday = models.DateField(null=True, blank=True)
    about_me = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    national_id = models.CharField(
        max_length=10,
        unique=True,
        validators=[RegexValidator(regex=r'^\d{10}$', message="National ID must be 10 digits")]
    )

    GENDER_TYPES = (
        ("female", "FEMALE"),
        ("male", "MALE")
    )
    gender = models.CharField(max_length=20, choices=GENDER_TYPES, null=True, blank=True)

    

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone' 
    REQUIRED_FIELDS = ['username', 'email']  



    def __str__(self):
        return f"{self.first_name} - {self.last_name}" 







        