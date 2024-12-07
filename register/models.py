from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage()
# Create your models here.
class Strength(models.Model):
    strength = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.strength

class Skills(models.Model):
    skill = models.CharField(max_length=30, unique = True)

    def __str__(self):
        return self.skill

class Education(models.Model):

    title = models.TextField(null=False, blank=False)
    institute = models.TextField(null=False, blank=False)
    start_date = models.DateField()
    end_date = models.DateField()
    class Meta:
        unique_together = ('title', 'institute', 'start_date', 'end_date')
    
    def __str__(self):
        return self.title+"-"+self.institute+"-"+f"{self.start_date}"+f"{self.end_date}"
    
class Certification(models.Model):

    title = models.TextField(null=False, blank=False)
    institute = models.TextField(null=False, blank=False)
    start_date = models.DateField()
    end_date = models.DateField()
    class Meta:
        unique_together = ('title', 'institute', 'start_date', 'end_date')
    
    def __str__(self):
        return self.title+"-"+self.institute+"-"+f"{self.start_date}"+f"{self.end_date}"

class Experience(models.Model):
    title = models.TextField(null=False)
    org = models.TextField(null=False)
    location = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(null = False, blank=False)  # Combine responsibilities into a single field


    class Meta:
        unique_together = ('title', 'org', 'start_date', 'end_date')

    def __str__(self):
        return self.title+"-"+self.org+"-"+f"{self.start_date}"+f"{self.end_date}"

class Project(models.Model):
    title = models.CharField(max_length=30)
    desc = models.TextField()
    link = models.URLField()
    start_date = models.DateField()
    end_date = models.DateField()
    class Meta:
        unique_together = ('title', 'desc', 'link', 'start_date', 'end_date')
    
    def __str__(self):
        return self.title+"-"+self.desc+"-"+f"{self.start_date}"+f"{self.end_date}"

class MiniProjects(models.Model):
    title = models.CharField(max_length=30)
    link = models.URLField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self) -> str:
        return self.title

class State(models.Model):
    state = models.TextField()

    def __str__(self):
        return self.state

class Address(models.Model):
    line1 = models.TextField()
    state = models.ForeignKey(State, null=True, on_delete=models.SET_NULL)
    pin_code = models.PositiveIntegerField()
    
    def __str__(self):
        return self.line1+str(self.state)+str(self.pin_code)

class Template(models.Model):
    template = models.TextField()
    template_html = models.TextField(unique=True, blank=False, null=False)
    def __str__(self):
        return self.template

class SocialMedia(models.Model):
    name = models.TextField()
    url = models.URLField(blank = False, unique = True)
    def __str__(self):
        return self.name

class UserResumeDetails(models.Model):
    name = models.TextField(default="resume")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.TextField(max_length=20)
    last_name = models.TextField(max_length=20)
    summary = models.TextField(max_length=500)
    is_global = models.BooleanField(default=False)
    skill_id = models.ManyToManyField(Skills)
    image = models.ImageField(blank=True, null=True, upload_to='images/', storage=fs)
    email = models.EmailField()
    phone = models.PositiveBigIntegerField()
    education = models.ManyToManyField(Education)
    certification = models.ManyToManyField(Certification)
    experience = models.ManyToManyField(Experience)
    project = models.ManyToManyField(Project)
    miniproject = models.ManyToManyField(MiniProjects)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    strength = models.ManyToManyField(Strength)
    template = models.ForeignKey(Template, on_delete=models.SET_DEFAULT, default=1)
    portfolio = models.URLField(null=True, blank=True)
    social = models.ManyToManyField(SocialMedia)

