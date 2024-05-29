from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.crypto import get_random_string


from django.core.mail import send_mail

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):   #this is for creating superusers that can access the django dashboard , but can be used to create admin ; which will be able to visit both django dhasboard and platform dashboard , function isAdmin (Basepermission ) return is_staff ..check phone photo
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        #addedotp
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        #addedotp
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
           

        return self.create_user(email, password, **extra_fields)  #this is for creating a user
    


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField( unique=True, error_messages={"unique": "A user with that email already exists."} )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False) 
    #the password field is not explicitly declared in the custom user model 
    # because it's handled by the AbstractBaseUser and BaseUserManager classes.
    start_date = models.DateTimeField(default=timezone.now)
    #addedotp
    confirmation_code = models.CharField(max_length=6, blank=True, null=True)
    is_active = models.BooleanField(default=False) 

    objects = CustomUserManager() #to handle the creation 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
    
    #addedotp
    def generate_code(self):
        self.confirmation_code = get_random_string(length=6, allowed_chars='0123456789')
        self.save()

    def send_confirmation_email(self):
        message = (
        f"Your confirmation code is {self.confirmation_code}. "
        f"If you ever lost the confirmation page click here: "
         f"http://127.0.0.1:3000/signup/user/confirmpage/{self.email}" #the problem is this will be sent as well when reseting password which is not logic so either remove it or make seperate one for resetpass
    )
        send_mail(
        subject='Email Confirmation',
        message=message,
        from_email='fstalert2023@gmail.com',
        recipient_list=[self.email],
        fail_silently=False,
    )
    

    

class Job(models.Model):
       title = models.CharField(max_length=300)  
       description = models.TextField()
       summary = models.TextField()
       salary = models.IntegerField(default=0)
       skills = models.CharField(max_length=500, default='no_skills')
       promoted = models.BooleanField(default=False)
       created_at = models.DateTimeField(default=timezone.now)

       def __str__(self):
        return self.title
       
       def total_applications(self):
        return self.applications.count()


    
class Application(models.Model):
    # Choices for the application status
    STATUS_CHOICES = (
        ('sent', 'Sent'),
        ('in review', 'In review'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    created_at = models.DateTimeField(default=timezone.now)
    cv = models.FileField(upload_to='cvs/',blank=True)  # Assuming files are stored in MEDIA_ROOT/cvs/
    cover_letter = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='sent')
    job = models.ForeignKey('Job', on_delete=models.CASCADE, related_name='applications')
    candidate = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='applications')
    
    class Meta:
     constraints = [
        models.UniqueConstraint(fields=['job', 'candidate'], name='unique_application_per_job')
        ]
  # Enforces that each user can only apply once per job

    def __str__(self):
        return f"{self.candidate.email} - {self.job.title}"
    

class Contact(models.Model):
       name = models.CharField(max_length=300, null=True , blank=True)  
       message = models.TextField(null=True, blank=True)
       email = models.CharField(max_length=500,null=True, blank=True)
       created_at = models.DateTimeField(default=timezone.now)

       def __str__(self):
        return self.name
       
