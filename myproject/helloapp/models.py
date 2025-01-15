from django.db import models
#from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import BaseUserManager
from multiselectfield import MultiSelectField
from django.utils.translation import gettext_lazy as _


class BuddyMatchingUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class BuddyMatchingUser(AbstractUser):
    """
    Custom user model for the Buddy Matching System.
    Field definitions for the data base.
    """

    objects = BuddyMatchingUserManager()

    
    LANGUAGE_CHOICES = [
        ('German', _('German')),
        ('English', _('English')),
        ('Both', _('Both')),
    ]

    DEGREE_CHOICES = [
        ('Bachelors', _('Bachelors')),
        ('Masters', _('Masters')),
    ]

    DEPARTMENT_CHOICES = [
        ('FB 1', _('Law and Economics (FB 1)')),
        ('FB 2', _('Social and Historical Sciences (FB 2)')),
        ('FB 3', _('Human Sciences (FB 3)')),
        ('FB 4', _('Mathematics (FB 4)')),
        ('FB 5', _('Physics (FB 5)')),
        ('FB 7', _('Chemistry (FB 7)')),
        ('FB 10', _('Biology (FB 10)')),
        ('FB 11', _('Material and Earth Sciences (FB 11)')),
        ('FB 13', _('Civil and Environmental Engineering (FB 13)')),
        ('FB 15', _('Architecture (FB 15)')),
        ('FB 16', _('Mechanical Engineering (FB 16)')),
        ('FB 18', _('Electrical Engineering and IT (FB 18)')),
        ('FB 20', _('Computer Science (FB 20)')),
    ]

    ROLE_CHOICES = [
        ('International Student', _('International Student')),
        ('Buddy', _('Buddy')),
    ]

    INTEREST_CHOICES = [
        ('Sports', _('Sports')),
        ('Culture', _('Culture')),
        ('Nature', _('Nature')),
        ('Technology', _('Technology')),
    ]

    role = models.CharField(
        max_length = 25,
        choices = ROLE_CHOICES,
        default = 'Buddy', 
    )
    surname = models.CharField(
        max_length = 255,
        default = 'Mustermann',
    )
    first_name = models.CharField(
        max_length = 255,
        default = 'Max',
    )
    preferred_language = models.CharField(
        max_length = 10,
        choices = LANGUAGE_CHOICES,
        default = 'English',
    )
    # student's email address
    email = models.EmailField(
        max_length = 255,
        unique = True,
        default = 'default@stud.tu-darmstadt.de')
    
    degree_level = models.CharField(
        max_length = 10,
        choices = DEGREE_CHOICES,
        default = 'Bachelors',  # Default value for degree
    )
    # application or matriculation number
    app_matr_number = models.PositiveIntegerField(
        unique = True,
        blank = True, # Allow blank values
        default = 0,
    )
    department = models.CharField(
        max_length = 50,
        choices = DEPARTMENT_CHOICES,
        default = 'FB 1',  
    )
    # country of sending university - for international students; country of preference - for local students
    country = models.CharField(
        max_length = 255,
        blank = True, 
        default = '',
    )
    # for local students
    preferred_number_of_partners = models.PositiveIntegerField(
        null = True,   
        default = 1, 
    )
    interests = MultiSelectField(
        choices = INTEREST_CHOICES, 
        blank = True,
    )
    partners = models.ManyToManyField(
        'self', 
        blank = True,
    )
    is_permitted = models.BooleanField(
        default = True
    )
    is_staff = models.BooleanField(
        default = False
    )

    # set user to email
    username = None
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []



    # Defines how the model is displayed in the admin interface
    class Meta:
        verbose_name = 'User' # Singular display name for the model
        verbose_name_plural = 'Users' # Plural display name for the model
        
        """
        # ANNA: kann auch nur ein me issue sein, aber mein terminal macht bei dem code oben:
        
        #ERRORS:
        #auth.User.groups: (fields.E304) Reverse accessor 'Group.user_set' for 'auth.User.groups' clashes with reverse accessor for 'helloapp.BuddyMatchingUser.groups'.
        #HINT: Add or change a related_name argument to the definition for 'auth.User.groups' or 'helloapp.BuddyMatchingUser.groups'.
        #auth.User.user_permissions: (fields.E304) Reverse accessor 'Permission.user_set' for 'auth.User.user_permissions' clashes with reverse accessor for 'helloapp.BuddyMatchingUser.user_permissions'.
        #HINT: Add or change a related_name argument to the definition for 'auth.User.user_permissions' or 'helloapp.BuddyMatchingUser.user_permissions'.
        #helloapp.BuddyMatchingUser.groups: (fields.E304) Reverse accessor 'Group.user_set' for 'helloapp.BuddyMatchingUser.groups' clashes with reverse accessor for 'auth.User.groups'.
        #HINT: Add or change a related_name argument to the definition for 'helloapp.BuddyMatchingUser.groups' or 'auth.User.groups'.
        #helloapp.BuddyMatchingUser.user_permissions: (fields.E304) Reverse accessor 'Permission.user_set' for 'helloapp.BuddyMatchingUser.user_permissions' clashes with reverse accessor for 'auth.User.user_permissions'.
        #HINT: Add or change a related_name argument to the definition for 'helloapp.BuddyMatchingUser.user_permissions' or 'auth.User.user_permissions'.
        
        verbose_name = 'Buddy Matching User'
        verbose_name_plural = 'Buddy Matching Users'

    groups = models.ManyToManyField(
        Group,
        related_name="buddy_matching_user_set",  # Provide unique related_name
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="buddy_matching_user_permissions",  # Provide unique related_name
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    ) """

    


    def __str__(self):
        return (
            f'{self.role} - '
            f'{self.surname}, {self.first_name} - '
            f'{self.preferred_language} - '
            f'{self.email} - '
            f'{self.degree_level} - '
            f'{self.app_matr_number} - '
            f'{self.department} - '
            f'{self.country} - '
            f'{self.is_permitted}'
        )


class HomepageText(models.Model):
    content = models.TextField(default="Willkommen auf der Seite!")  # Standardtext
    last_updated = models.DateTimeField(auto_now=True)  # Automatisch aktualisieren bei jeder Änderung

    def __str__(self):
        return f"Homepage Text (aktualisiert am {self.last_updated})"