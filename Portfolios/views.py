from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from register.models import UserResumeDetails
from django.http import HttpResponseBadRequest, JsonResponse
from register.models import *
from django.core.files.storage import default_storage
from django.shortcuts import get_object_or_404

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        resultSet = UserResumeDetails.objects.filter(user = request.user).all()

        return render(request, 'listdocs.html', {"data_type": "Resumes", "show_resume": True, "show_portfolio":False, "resultset":resultSet})
    
        # return render(request, 'dashboard.html')
    return render(request, 'login.html')

def login_fx(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {"error": "Username or Password is Incorrect!"})
            
    return render(request, 'login.html', {"hidden": "true"})

def logout_fx(request):
    logout(request)
    return redirect('/login/')

def fetch_docs(request):
    return render(request, 'listdocs.html', {"data_type": "Documents", "show_resume": True, "show_portfolio":True})
    # to add logic for all the documents

def fetch_resume(request):
    
    resultSet = UserResumeDetails.objects.filter(user = request.user).all()

    return render(request, 'listdocs.html', {"data_type": "Resumes", "show_resume": True, "show_portfolio":False, "resultset":resultSet})

def fetch_portfolios(request):
    return render(request, 'listdocs.html', {"data_type": "Portfolios", "show_resume": False, "show_portfolio":True})

def show_resume(request, id):

    if request.method == "GET":

        userdetail = UserResumeDetails.objects.filter(id = id).first()

        if userdetail == None:
            #return no resume to show template
            return HttpResponseBadRequest()
            ...

        if userdetail.is_global or userdetail.user == request.user:

            return render(request, userdetail.template.template_html, {'userdetail': userdetail})
                
        else:
            #not authorized
            print(userdetail.is_global)
            return HttpResponseBadRequest()
            ...


    else:
        return HttpResponseBadRequest()

def edit(request, id):
    if request.method == "GET":
        userdetail = UserResumeDetails.objects.filter(id = id).first()
        if request.user != userdetail.user:
            return HttpResponseBadRequest()
        return render(request, "edit.html", {'userdetail': userdetail, "resume_templates": Template.objects.all()})
    
    elif request.method == "POST":
        user_resume = get_object_or_404(UserResumeDetails, id = id)  

        # Get the updated values from the request
        f_name = request.POST.get('fName')
        l_name = request.POST.get('lName')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        portfolio = request.POST.get('portfolioLink', None)
        summary = request.POST.get('summary')
        is_global = request.POST.get('isGlobal') == 'on'
        template = get_object_or_404(Template, template=request.POST.get('template'))

        # Handle the Image (Delete old if new image is uploaded)
        new_image = request.FILES.get('image', None)
        if new_image:
            # Delete the old image from the server if it exists
            if user_resume.image:
                try:
                    # Remove the old image file from the storage
                    default_storage.delete(user_resume.image.name)
                except:
                    pass

            # Set the new image for the object
            user_resume.image = new_image

        # Handle ForeignKey: Address and State
        state_name = request.POST.get('state')
        state, _ = State.objects.get_or_create(state=state_name)
        address, _ = Address.objects.get_or_create(
            line1=request.POST.get('address'),
            state=state,
            pin_code=request.POST.get('zip')
        )

        # Update the main object
        user_resume.first_name = f_name
        user_resume.last_name = l_name
        user_resume.email = email
        user_resume.phone = phone
        user_resume.portfolio = portfolio
        user_resume.summary = summary
        user_resume.address = address
        user_resume.template = template
        user_resume.is_global = is_global

        # Handle ManyToMany: Skills
        user_resume.skill_id.clear()  # Clear previous skills before adding new ones
        for i in range(1, 9):  # Assuming 8 skill fields
            skill_name = request.POST.get(f'skill{i}')
            if skill_name:
                skill, _ = Skills.objects.get_or_create(skill=skill_name)
                user_resume.skill_id.add(skill)

        # Handle ManyToMany: Education
        user_resume.education.clear()  # Clear previous education entries
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

        # Handle ManyToMany: Social Media
        user_resume.social.clear()  # Clear previous social media entries
        for i in range(1, 4):  # Assuming 3 social media links
            platform_name = request.POST.get(f'platformName{i}')
            social_url = request.POST.get(f'socialURL{i}')
            if platform_name and social_url:
                social_media, _ = SocialMedia.objects.get_or_create(
                    name=platform_name, url=social_url
                )
                user_resume.social.add(social_media)

        # Handle ManyToMany: Certifications
        user_resume.certification.clear()  # Clear previous certifications
        for i in range(1, 4):  # Assuming up to 3 certifications
            certificate_name = request.POST.get(f'cTitle{i}')
            issued_by = request.POST.get(f'cOrganisation{i}')
            start_date = request.POST.get(f'csd{i}')
            end_date = request.POST.get(f'ced{i}')
            if certificate_name and issued_by and start_date and end_date:
                certification, _ = Certification.objects.get_or_create(
                    title=certificate_name, institute=issued_by, start_date=start_date, end_date=end_date
                )
                user_resume.certification.add(certification)
            
        # Handle ManyToMany: Experience
        user_resume.experience.clear()  # Clear previous experience entries
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
        user_resume.project.clear()  # Clear previous project entries
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
        user_resume.miniproject.clear()  # Clear previous mini project entries
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
        user_resume.strength.clear()  # Clear previous strength entries
        for i in range(1, 4):  # Assuming up to 3 strength entries
            strength_name = request.POST.get(f'strength{i}')
            if strength_name:
                strength, _ = Strength.objects.get_or_create(strength=strength_name)
                user_resume.strength.add(strength)

        # Save the updated object
        user_resume.save()



        return redirect(f"/show/{id}")

def delete(request, id):
    if request.method == "GET":
        userdetail = UserResumeDetails.objects.filter(id = id).first()
        if request.user != userdetail.user:
            return HttpResponseBadRequest()
        userdetail.delete()
        return redirect('/')
    else:
        return HttpResponseBadRequest()