from django.db import models
#from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, Group, Permission


class BuddyMatchingUser(AbstractUser):
    """
    Custom user model for the Buddy Matching System.
    Field definitions for the data base.
    """

    LANGUAGE_CHOICES = [
        ('German', 'German'),
        ('English', 'English'),
        ('Both', 'Both'),
    ]

    DEGREE_CHOICES = [
        ('Bachelors', 'Bachelors'),
        ('Masters', 'Masters'),
    ]

    DEPARTMENT_CHOICES = [
        ('FB 1', 'Rechts- und Wirtschaftswissenschaften (FB 1)'),
        ('FB 2', 'Gesellschafts- & Geschichtswissenschaften (FB 2)'),
        ('FB 3', 'Humanwissenschaften (FB 3)'),
        ('FB 4', 'Mathematik (FB 4)'),
        ('FB 5', 'Physik (FB 5)'),
        ('FB 7', 'Chemie (FB 7)'),
        ('FB 10', 'Biologie (FB 10)'),
        ('FB 11', 'Material- und Geowissenschaften (FB 11)'),
        ('FB 13', 'Bau- und Umweltingenieurwissenschaften (FB 13)'),
        ('FB 15', 'Architektur (FB 15)'),
        ('FB 16', 'Maschinenbau (FB 16)'),
        ('FB 18', 'Elektrotechnik und Informationstechnik (FB 18)'),
        ('FB 20', 'Informatik (FB 20)'),
    ]

    ROLE_CHOICES = [
        ('International Student', 'International Student'),
        ('Buddy', 'Buddy'),
    ]
    role = models.CharField(
        max_length = 25,
        choices = ROLE_CHOICES,
        default = 'International Student', 
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
        default = 'none',
    )
    # for local students
    preferred_number_of_partners = models.PositiveIntegerField(
        null = True,   
        default = 1, 
    )
    partners = models.ManyToManyField(
        'self', 
        blank = True,
    )
    is_permitted = models.BooleanField(
        default = False
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
    ) 
    """
    


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
