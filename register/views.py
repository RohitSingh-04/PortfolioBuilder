from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseForbidden, JsonResponse
from json import loads
from .models import *
from django.shortcuts import get_object_or_404

# Create your views here.
def createResume(request):
    if request.method == "GET":
        return render(request, 'resume_form.html', context = {"resume_templates": Template.objects.all()})

    elif request.method == "POST":
        f_name = request.POST.get('fName')
        l_name = request.POST.get('lName')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        portfolio = request.POST.get('portfolioLink', None)
        summary = request.POST.get('summary')
        image = request.FILES.get('image', None)
        is_global  = request.POST.get('isGlobal') == 'on'
        # Handle ForeignKey: Template
        template = get_object_or_404(Template, template=request.POST.get('template'))

        # Handle ForeignKey: Address and State
        state_name = request.POST.get('state')
        state, _ = State.objects.get_or_create(state=state_name)
        address, _ = Address.objects.get_or_create(
            line1=request.POST.get('address'),
            state=state,
            pin_code=request.POST.get('zip')
        )

        # Create the main object
        user_resume = UserResumeDetails.objects.create(
            user=request.user,  # Assuming the user is authenticated
            first_name=f_name,
            last_name=l_name,
            email=email,
            phone=phone,
            portfolio=portfolio,
            summary=summary,
            address=address,
            image = image,
            template=template,
            is_global = is_global
        )

        # Handle ManyToMany: Skills
        for i in range(1, 9):  # Assuming 8 skill fields
            skill_name = request.POST.get(f'skill{i}')
            if skill_name:
                skill, _ = Skills.objects.get_or_create(skill=skill_name)
                user_resume.skill_id.add(skill)

        # Handle ManyToMany: Education
        for i in range(1, 3):  # Assuming up to 2 education entries
            title = request.POST.get(f'eTitle{i}')
            institute = request.POST.get(f'eInstitute{i}')
            start_date = request.POST.get(f'esd{i}')
            end_date = request.POST.get(f'eed{i}')
            if title and institute and start_date and end_date:
                education, _ = Education.objects.get_or_create(
                    title=title, institute=institute,
                    start_date=start_date, end_date=end_date
                )
                user_resume.education.add(education)
        
        
        # Handle ManyToMany: Certifications
        for i in range(1, 3):  # Assuming up to 2 certification entries
            title = request.POST.get(f'cTitle{i}')
            institute = request.POST.get(f'cOrganisation{i}')
            start_date = request.POST.get(f'csd{i}')
            end_date = request.POST.get(f'ced{i}')
            if title and institute and start_date and end_date:
                certification, _ = Certification.objects.get_or_create(
                    title=title, institute=institute,
                    start_date=start_date, end_date=end_date
                )
                user_resume.certification.add(certification)

        # Handle ManyToMany: Experience
        for i in range(1, 3):  # Assuming up to 2 experience entries
            title = request.POST.get(f'exTitle{i}')
            org = request.POST.get(f'exOrganisation{i}')
            location = request.POST.get(f'location{i}')
            start_date = request.POST.get(f'exsd{i}')
            end_date = request.POST.get(f'exed{i}')
            description = request.POST.get(f'exDescription{i}')
            if title and org and start_date and end_date and description:
                experience, _ = Experience.objects.get_or_create(
                    title=title, org=org, location=location,
                    start_date=start_date, end_date=end_date,
                    description=description
                )
                user_resume.experience.add(experience)

        # Handle ManyToMany: Projects
        for i in range(1, 3):  # Assuming up to 2 project entries
            title = request.POST.get(f'pName{i}')
            desc = request.POST.get(f'pDescription{i}')
            link = request.POST.get(f'pLink{i}')
            start_date = request.POST.get(f'psd{i}')
            end_date = request.POST.get(f'ped{i}')
            if title and desc and link and start_date and end_date:
                project, _ = Project.objects.get_or_create(
                    title=title, desc=desc, link=link,
                    start_date=start_date, end_date=end_date
                )
                user_resume.project.add(project)

        # Handle ManyToMany: MiniProjects
        for i in range(1, 3):  # Assuming up to 2 mini project entries
            title = request.POST.get(f'mpName{i}')
            link = request.POST.get(f'mpLink{i}')
            start_date = request.POST.get(f'mpsd{i}')
            end_date = request.POST.get(f'mped{i}')
            if title and link and start_date and end_date:
                mini_project, _ = MiniProjects.objects.get_or_create(
                    title=title, link=link,
                    start_date=start_date, end_date=end_date
                )
                user_resume.miniproject.add(mini_project)

        # Handle ManyToMany: Strengths
        for i in range(1, 4):  # Assuming up to 3 strength entries
            strength_name = request.POST.get(f'strength{i}')
            if strength_name:
                strength, _ = Strength.objects.get_or_create(strength=strength_name)
                user_resume.strength.add(strength)

        
        # Save social media links
        for i in range(1, 4):  # Assuming 3 social media links
            platform_name = request.POST.get(f'platformName{i}')
            social_url = request.POST.get(f'socialURL{i}')
            if platform_name and social_url:
                social_media, _ = SocialMedia.objects.get_or_create(
                    name=platform_name, url=social_url
                )
                user_resume.social.add(social_media)

        # Save the complete object
        user_resume.save()


        return redirect('/')

        
    return HttpResponseForbidden()

def newUser(request):
    if request.method == 'POST':
        data = request.POST
        if User.objects.filter(username = data['username']).exists():
            data = {i:data[i] for i in data if i != 'username'}
            return render(request, 'newRegistration.html', {'data': data, 'error':'invalid Username', 'hidden': 'false'})
        
        if User.objects.filter(email = data['email']).exists():
            data = {i:data[i] for i in data if i != 'email'}
            return render(request, 'newRegistration.html', {'data': data, 'error':'invalid Email', 'hidden': 'false'})

        User.objects.create_user(username=data['username'], first_name=data['first_name'], last_name=data['last_name'], email=data['email'], password = data['password'])


        return redirect('/login/')
    return render(request, 'newRegistration.html', {'hidden': 'true'})

def UserExists(request):
    if request.method == 'POST':
        data = request.body
        data = loads(data)

        if User.objects.filter(username = data['username']).exists():
            return JsonResponse({"exist":True})
        else:
            return JsonResponse({"exist": False})
        
    return HttpResponseForbidden()
    
    