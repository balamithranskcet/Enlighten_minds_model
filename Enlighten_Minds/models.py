from django.core.validators import MinValueValidator,MaxValueValidator,RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _


class MyUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class users(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    Phone_number=models.CharField(max_length=10,blank=True,null=True)
    state=models.CharField(max_length=20,blank=True,null=True)
    city=models.CharField(max_length=20,blank=True,null=True)
    USERNAME_FIELD = 'email'
    #image = models.ImageField(upload_to='profile_image', default='images.jpeg', blank=True)
    instructor=models.BooleanField(default=False)
    #learner=models.BooleanField(default=True)
    refugee=models.BooleanField(default=False)
    low_income_student = models.BooleanField(default=False)




    REQUIRED_FIELDS = ['first_name']
    objects = MyUserManager()

    def __str__(self):
        return self.first_name


class Profile(models.Model):
    user=models.OneToOneField(users,on_delete=models.CASCADE)

    total_course_enrolled=models.PositiveIntegerField(default=0)
    earnings=models.PositiveIntegerField(default=0)

    total_course_created = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.first_name


def createProfile(sender, **kwargs):
    if kwargs['created']:
        user_profile = Profile.objects.create(user=kwargs['instance'])
post_save.connect(createProfile, sender=users)

class Instructor_level(models.Model):
    user=models.OneToOneField(users,on_delete=models.CASCADE)

    kind_of_teaching=models.CharField(max_length=50)
    video_pro=models.CharField(max_length=50)
    audience=models.CharField(max_length=50)

    def __str__(self):
        return self.user.first_name




class Courses(models.Model):
    user=models.ForeignKey(users,on_delete=models.CASCADE)

    course_name=models.CharField(max_length=50)
    course_category = models.CharField(max_length=50,default="null")
    course_description=models.TextField()
    #in Minutes
    course_duration=models.PositiveIntegerField(default=0)
    course_contibuted_money = models.PositiveIntegerField(default=0)

    course_author = models.CharField(max_length=50)
    course_price=models.PositiveIntegerField(validators=[MinValueValidator(1)])
    course_published=models.BooleanField(default=False)

    course_no_of_registrations=models.PositiveIntegerField(default=0)
    money_earned_from_course=models.PositiveIntegerField(default=0)
    overall_rating=models.PositiveIntegerField(default=1)

    course_price_for_refugees=models.PositiveIntegerField(default=0)
    #course_fund_raising

    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-overall_rating','-created',]

    def __str__(self):
        return self.course_name

class MyCourses(models.Model):
    user=models.ForeignKey(users,on_delete=models.CASCADE)

    course=models.ForeignKey(Courses,on_delete=models.CASCADE)
    completion=models.BooleanField(default=False)
    course_rating=models.PositiveIntegerField(default=1,validators=[MinValueValidator(1),MaxValueValidator(5)])

    course_started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=['-course_started_at']

    def __str__(self):
        return self.course.__str__()

class Post(models.Model):
    user = models.ForeignKey(users, on_delete=models.CASCADE)
    post_name=models.CharField(max_length=50)
    post_description=models.TextField()
    post_active=models.BooleanField(default=False)
    post_hours=models.PositiveIntegerField(default=0)
    post_total_amount= models.PositiveIntegerField(default=0)
    post_balance_amount = models.PositiveIntegerField(default=0)
    post_email = models.EmailField()
    post_contact_number=models.CharField(max_length=10, blank=True, null=True)
    post_no_of_courses = models.PositiveIntegerField(default=0)
    post_total_contibutors = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.post_name

class RefugeeDetails(models.Model):
    name = models.ForeignKey(users, on_delete=models.CASCADE)
    certificate = models.FileField(upload_to='RefugeeCertificates')

    def __str__(self):
        return self.name.first_name


class Scholarship(models.Model):
    user=models.OneToOneField(users,on_delete=models.CASCADE)
    low_income_student_certificate=models.FileField()

    students_affordable_money = models.PositiveIntegerField(default=0)
    students_affordable_money_reason = models.CharField(max_length=500,default=" ")
    reson_for_applying = models.CharField(max_length=500, default=" ")
    goals_achieved_by_this_course = models.CharField(max_length=500, default=" ")

    educational_background =  models.CharField(max_length=100, default=" ")
    employment_status = models.CharField(max_length=100, default=" ")
    annual_income = models.CharField(max_length=100, default=" ")

    def __str__(self):
        return self.user.first_name


class Fundraiser(models.Model):
    name_of_course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    name_of_post  = models.CharField(max_length=100)
    percentage_shared = models.PositiveIntegerField(default=0)
