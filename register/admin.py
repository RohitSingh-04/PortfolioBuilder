from django.contrib import admin
from .models import *
# Register your models here.
resume_models = [Language, Skills, UserResumeDetails, Education, Strength, State, Experience, Project, MiniProjects, Address, Certification, Template, ColourScheme, SocialMedia]

for model in resume_models:
    admin.site.register(model)
