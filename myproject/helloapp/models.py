from django.db import models
#from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import BaseUserManager
from multiselectfield import MultiSelectField
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from datetime import timedelta

# Sets default date until account delation
def default_deletion_date():
    return now().date() + timedelta(days=29)

def default_last_reset():
    return now().date()

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
    
    COUNTRY_CHOICES = [
        ('AF', _('Afghanistan')),
        ('AL', _('Albania')),
        ('DZ', _('Algeria')),
        ('AS', _('American Samoa')),
        ('AD', _('Andorra')),
        ('AO', _('Angola')),
        ('AG', _('Antigua and Barbuda')),
        ('AR', _('Argentina')),
        ('AM', _('Armenia')),
        ('AU', _('Australia')),
        ('AT', _('Austria')),
        ('AZ', _('Azerbaijan')),
        ('BS', _('Bahamas')),
        ('BH', _('Bahrain')),
        ('BD', _('Bangladesh')),
        ('BB', _('Barbados')),
        ('BY', _('Belarus')),
        ('BE', _('Belgium')),
        ('BZ', _('Belize')),
        ('BJ', _('Benin')),
        ('BT', _('Bhutan')),
        ('BO', _('Bolivia')),
        ('BA', _('Bosnia and Herzegovina')),
        ('BW', _('Botswana')),
        ('BR', _('Brazil')),
        ('BN', _('Brunei')),
        ('BG', _('Bulgaria')),
        ('BF', _('Burkina Faso')),
        ('BI', _('Burundi')),
        ('CV', _('Cabo Verde')),
        ('KH', _('Cambodia')),
        ('CM', _('Cameroon')),
        ('CA', _('Canada')),
        ('CF', _('Central African Republic')),
        ('TD', _('Chad')),
        ('CL', _('Chile')),
        ('CN', _('China')),
        ('CO', _('Colombia')),
        ('KM', _('Comoros')),
        ('CG', _('Congo (Brazzaville)')),
        ('CD', _('Congo (Kinshasa)')),
        ('CR', _('Costa Rica')),
        ('CI', _('Côte d’Ivoire')),
        ('HR', _('Croatia')),
        ('CU', _('Cuba')),
        ('CY', _('Cyprus')),
        ('CZ', _('Czechia')),
        ('DK', _('Denmark')),
        ('DJ', _('Djibouti')),
        ('DM', _('Dominica')),
        ('DO', _('Dominican Republic')),
        ('EC', _('Ecuador')),
        ('EG', _('Egypt')),
        ('SV', _('El Salvador')),
        ('EN', _('England')),
        ('GQ', _('Equatorial Guinea')),
        ('ER', _('Eritrea')),
        ('EE', _('Estonia')),
        ('SZ', _('Eswatini')),
        ('ET', _('Ethiopia')),
        ('FJ', _('Fiji')),
        ('FI', _('Finland')),
        ('FR', _('France')),
        ('GA', _('Gabon')),
        ('GM', _('Gambia')),
        ('GE', _('Georgia')),
        ('DE', _('Germany')),
        ('GH', _('Ghana')),
        ('GR', _('Greece')),
        ('GD', _('Grenada')),
        ('GT', _('Guatemala')),
        ('GN', _('Guinea')),
        ('GW', _('Guinea-Bissau')),
        ('GY', _('Guyana')),
        ('HT', _('Haiti')),
        ('HN', _('Honduras')),
        ('HU', _('Hungary')),
        ('IS', _('Iceland')),
        ('IN', _('India')),
        ('ID', _('Indonesia')),
        ('IR', _('Iran')),
        ('IQ', _('Iraq')),
        ('IE', _('Ireland')),
        ('IL', _('Israel')),
        ('IT', _('Italy')),
        ('JM', _('Jamaica')),
        ('JP', _('Japan')),
        ('JO', _('Jordan')),
        ('KZ', _('Kazakhstan')),
        ('KE', _('Kenya')),
        ('KI', _('Kiribati')),
        ('KP', _('Korea (North)')),
        ('KR', _('Korea (South)')),
        ('KW', _('Kuwait')),
        ('KG', _('Kyrgyzstan')),
        ('LA', _('Laos')),
        ('LV', _('Latvia')),
        ('LB', _('Lebanon')),
        ('LS', _('Lesotho')),
        ('LR', _('Liberia')),
        ('LY', _('Libya')),
        ('LI', _('Liechtenstein')),
        ('LT', _('Lithuania')),
        ('LU', _('Luxembourg')),
        ('MG', _('Madagascar')),
        ('MW', _('Malawi')),
        ('MY', _('Malaysia')),
        ('MV', _('Maldives')),
        ('ML', _('Mali')),
        ('MT', _('Malta')),
        ('MH', _('Marshall Islands')),
        ('MR', _('Mauritania')),
        ('MU', _('Mauritius')),
        ('MX', _('Mexico')),
        ('FM', _('Micronesia')),
        ('MD', _('Moldova')),
        ('MC', _('Monaco')),
        ('MN', _('Mongolia')),
        ('ME', _('Montenegro')),
        ('MA', _('Morocco')),
        ('MZ', _('Mozambique')),
        ('MM', _('Myanmar (Burma)')),
        ('NA', _('Namibia')),
        ('NR', _('Nauru')),
        ('NP', _('Nepal')),
        ('NL', _('Netherlands')),
        ('NZ', _('New Zealand')),
        ('NI', _('Nicaragua')),
        ('NOI', _('Northern Ireland')),
        ('NE', _('Niger')),
        ('NG', _('Nigeria')),
        ('MK', _('North Macedonia')),
        ('NO', _('Norway')),
        ('OM', _('Oman')),
        ('PK', _('Pakistan')),
        ('PW', _('Palau')),
        ('PS', _('Palestine')),
        ('PA', _('Panama')),
        ('PG', _('Papua New Guinea')),
        ('PY', _('Paraguay')),
        ('PE', _('Peru')),
        ('PH', _('Philippines')),
        ('PL', _('Poland')),
        ('PT', _('Portugal')),
        ('QA', _('Qatar')),
        ('RO', _('Romania')),
        ('RU', _('Russia')),
        ('RW', _('Rwanda')),
        ('KN', _('Saint Kitts and Nevis')),
        ('LC', _('Saint Lucia')),
        ('VC', _('Saint Vincent and the Grenadines')),
        ('WS', _('Samoa')),
        ('SM', _('San Marino')),
        ('ST', _('São Tomé and Príncipe')),
        ('SA', _('Saudi Arabia')),
        ('SN', _('Senegal')),
        ('RS', _('Serbia')),
        ('SC', _('Seychelles')),
        ('SCO', _('Scotland')),
        ('SL', _('Sierra Leone')),
        ('SG', _('Singapore')),
        ('SK', _('Slovakia')),
        ('SI', _('Slovenia')),
        ('SB', _('Solomon Islands')),
        ('SO', _('Somalia')),
        ('ZA', _('South Africa')),
        ('SS', _('South Sudan')),
        ('ES', _('Spain')),
        ('LK', _('Sri Lanka')),
        ('SD', _('Sudan')),
        ('SR', _('Suriname')),
        ('SE', _('Sweden')),
        ('CH', _('Switzerland')),
        ('SY', _('Syria')),
        ('TW', _('Taiwan')),
        ('TJ', _('Tajikistan')),
        ('TZ', _('Tanzania')),
        ('TH', _('Thailand')),
        ('TL', _('Timor-Leste')),
        ('TG', _('Togo')),
        ('TO', _('Tonga')),
        ('TT', _('Trinidad and Tobago')),
        ('TN', _('Tunisia')),
        ('TR', _('Turkey')),
        ('TM', _('Turkmenistan')),
        ('TV', _('Tuvalu')),
        ('UG', _('Uganda')),
        ('UA', _('Ukraine')),
        ('AE', _('United Arab Emirates')),
        ('GB', _('United Kingdom')),
        ('US', _('United States')),
        ('UY', _('Uruguay')),
        ('UZ', _('Uzbekistan')),
        ('VU', _('Vanuatu')),
        ('VA', _('Vatican City')),
        ('VE', _('Venezuela')),
        ('VN', _('Vietnam')),
        ('YE', _('Yemen')),
        ('WA', _('Wales')),
        ('ZM', _('Zambia')),
        ('ZW', _('Zimbabwe')),
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
        choices= COUNTRY_CHOICES,
        blank = True, 
        default = '',  # Default value for country
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
    deletion_date = models.DateField(
        default=default_deletion_date,
        help_text="Das Datum, an dem der Account gelöscht wird."
    )
    last_reset = models.DateField(
        default=default_last_reset,
        help_text="Das letzte Mal, als der Countdown zurückgesetzt wurde."
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

    # Resets automatic deletion date of user by number of days specified in timedelta
    def reset_deletion_date(self):
        self.deletion_date = now().date() + timedelta(days=365)
        self.last_reset = now().date()
        self.save()

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
    content_de = models.TextField(_("Content in German"), default="Willkommen auf der Seite!")
    content_en = models.TextField(_("Content in English"), default="Welcome to the page!")
    last_updated = models.DateTimeField(auto_now=True)  # Wird bei jeder Änderung automatisch aktualisiert

    def __str__(self):
        return f"Homepage Text (aktualisiert am {self.last_updated})"
    


class Feedback(models.Model):
    '''
    Model to store feedback from students.
    '''
    RATING_CHOICES = [
        ('EX', 'Excellent'),
        ('VG', 'Very Good'),
        ('G', 'Good'),
        ('F', 'Fair'),
        ('P', 'Poor'),
        ('NA', 'N/A'),
    ]

    student = models.ForeignKey(BuddyMatchingUser, on_delete=models.CASCADE)  # Link to BuddyMatchingUser
    text_feedback = models.TextField(blank=True, help_text="Provide your detailed feedback.")
    rating_1 = models.CharField(max_length=2, choices=RATING_CHOICES, help_text="Rate your experience.")
    rating_2 = models.CharField(max_length=2, choices=RATING_CHOICES, help_text="Rate the matching process.")
    # Add more rating fields

    # Automatically set the date and time when the feedback is submitted
    submitted_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return f"Feedback from {self.student.email} on {self.submitted_at}"