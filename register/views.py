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
        print(request.POST)
        f_name = request.POST.get('fName')
        l_name = request.POST.get('lName')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        portfolio = request.POST.get('portfolioLink', None)
        summary = request.POST.get('summary')
        image = request.FILES.get('image', None)
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

        # Repeat similar logic for other ManyToMany relationships (Certification, Experience, etc.)
        
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

        return JsonResponse({'message': 'Resume created successfully!'})

        
    return JsonResponse({"hii": 12})

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
    
    