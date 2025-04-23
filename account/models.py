from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
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
    phone = PhoneNumberField(unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    birthday = models.DateField()
    about_me = models.TextField(null=True, blank=True)

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

   
    ROLE_CHOICES = (
        ("teacher", "Teacher"),
        ('student', 'Student'),
        ('support', 'Support'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    SUPPORT_SUB_ROLE_CHOICES = (
        ("technical_support", "Technical Support"),
        ("ticket_service", "Ticket Service"),
        ("billing_support", "Billing Support"),
        ("blog_support", "Blog Support"),
    )

    
    sub_role = models.CharField(max_length=50, choices=SUPPORT_SUB_ROLE_CHOICES, null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'  # برای کاربران عادی
    REQUIRED_FIELDS = ['username', 'email']  # برای createsuperuser



    def save(self, *args, **kwargs):
        if self.role != 'support' and self.sub_role:
            self.sub_role = None  

        super().save(*args, **kwargs)  


    


    def __str__(self):
        return self.username or str(self.phone) or self.email or "User"







        