from django.db import models

class Entry(models.Model):
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
        max_length=255,
        default = 'Mustermann',
    )
    first_name = models.CharField(
        max_length=255,
        default = 'Max',
    )
    preferred_language = models.CharField(
        max_length = 10,
        choices = LANGUAGE_CHOICES,
        default = 'English',
    )
    # student's email address
    email = models.EmailField(
        max_length=255,
        default = 'default@stud.tu-darmstadt.de')
    degree_level = models.CharField(
        max_length = 10,
        choices = DEGREE_CHOICES,
        default = 'Bachelors',  # Default value for degree
    )
    # TODO: ask, whether application number only contains numbers
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



    def __str__(self):
        return (
            f'{self.role} - '
            f'{self.surname}, {self.first_name} - '
            f'{self.preferred_language} - '
            f'{self.email} - '
            f'{self.degree_level} - '
            f'{self.app_matr_number} - '
            f'{self.department} - '
            f'{self.country}'
        )
