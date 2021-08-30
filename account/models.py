from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _

# from course.models import Course

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = None
    
    last_name = None
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(max_length=35)
    first_name=models.CharField(max_length=35)
    is_student = models.BooleanField(default=False)
    is_instractor = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()



class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,null=True)
    name = models.CharField(null=True, blank=True, max_length=250)
    email = models.CharField(max_length=200, null=True)
    course_enrolled = models.ForeignKey('course.Course',on_delete=models.CASCADE,null=True,blank=True)
    
    date_of_birth = models.CharField(max_length=200,null=True, blank=True)
    education_qualification = models.CharField(null=True, blank=True, max_length=250)
    institution_name = models.CharField(null=True, blank=True, max_length=250)
    image = models.ImageField(upload_to='photos/%y/%m/%d',null=True, blank=True)
    student_address = models.CharField(null=True, blank=True, max_length=250)
   
    batch_number = models.ForeignKey('course.BatchNumber',on_delete=models.CASCADE,null=True,blank=True)
    confirm = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('-id',)
        verbose_name='Student'
        verbose_name_plural='Students'
        indexes = [models.Index(fields=['user', 'name','email','course_enrolled','date_of_birth','education_qualification','institution_name','image','student_address']),]
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
class Instractor(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='instractor_info')
    name = models.CharField(null=True, blank=True, max_length=250)
    degination = models.CharField(null=True, blank=True, max_length=250)
    image = models.ImageField(upload_to='photos/%y/%m/%d',null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name