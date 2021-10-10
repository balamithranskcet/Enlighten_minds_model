from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .models import *
from .forms import *
from .tokens import account_activation_token

from django.http import HttpResponseRedirect

def index(request):
    #return (render(request,'index.html')if not request.user.is_authenticated else redirect('home'))
    return (redirect('signup') if not request.user.is_authenticated else redirect('home'))

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
#            if User.objects.filter(email__iexact=email).count() == 1:
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            email_from = settings.EMAIL_HOST_USER
            mail_subject = 'Activate your account.'
            message = render_to_string('email_template.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                    })
            #print(message)
            to_email = form.cleaned_data.get('email')
            send_mail(mail_subject, message, email_from, (to_email,))
            #return HttpResponse('Please confirm your email address to complete the registration')
            #return render(request,'emailverification.html',{'confirm_email':'Please confirm your email address to complete the registration'})
            messages.success(request,'Activation Link Sent')
            return redirect('signup')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        #return render(request,'emailverification.html',{'confirm_done': 'Thank you for your email confirmation. Now you can login your account.'})
        messages.success(request,'Thank you for your email confirmation..')
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid!')

def Login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        user=authenticate(request,email=request.POST.get('email'),password=request.POST.get('password'))
        #print(user)
        if user is not None:
            #request.session.set_expiry(600)
            login(request,user)
            return redirect('home')
        messages.error(request,'Invalid Details')
        return redirect('login')
    return render(request,'login.html')

@login_required(login_url='login')
def Logout(request):
    logout(request)
    return redirect('/')

@login_required(login_url='login')
def home(request):
    return render(request, 'studenthome.html')

# Profile part
@login_required(login_url='login')
def student_profile(request):
    data = users.objects.get(first_name=request.user)
    if request.method == "POST":
        return redirect('updateProfile')
    return render(request, 'studprofile.html', {'users': data})



@login_required(login_url='login')
def updateProfile(request,id):
    data = users.objects.get(first_name=request.user)
    if request.method == "POST":
        data = users.objects.get(id=id)
        form = EditProfileForm(request.POST, instance=data)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('profile')
    return render(request, 'updatestudprofile.html', {'users': data})

def my_courses(request):
    return render(request,)





# instructor part
@login_required(login_url='login')
def instructor_mode(request):
    messages.success(request, 'You are now an Instructor hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
    return render(request,'create.html')

@login_required(login_url='login')
def upgrade_to_instructor(request):
    Instructor_level.objects.create(user=request.user,kind_of_teaching=request.POST.get('kind_of_teaching'),video_pro=request.POST.get('video_pro'),audience=request.POST.get('audience'))
    print(request.POST.get('kind_of_teaching'))
    print(request.POST.get('video_pro'))
    print(request.POST.get('audience'))
    request.user.instructor=True
    request.user.save()
    messages.success(request,'You are now an Instructor')
    return redirect('home')
    #return render(request,'')



# course creation part
@login_required(login_url='login')
def courseTitle(request):

    if request.method == "POST":
        course = Courses.objects.create(user=request.user,course_name=request.POST.get('course_title'),course_category=request.POST.get('category'),course_description=request.POST.get('description'),course_price=request.POST.get('price'))
        course.save()
        print(request.POST.get('course_title'))
        print(request.POST.get('category'))
        print(request.POST.get('description'))
        print(request.POST.get('price'))
        return HttpResponseRedirect(f'courseContentCreation/{course.id}')
    return render(request, 'coursetitle.html')

def courseContentCreation(request,id):
    print(id)
    course = Courses.objects.get(id=id)
    return render(request, 'main_createCoursePage.html', {'course': course})

def courseAddSection(request):
    if request.method=='POST':
        print(request.POST.get('Section_Name'))
        print(request.POST.get('Section_Number'))
        print(request.POST.get('description'))
        print(request.POST.get)
        print(request.POST.get('price'))
    return render(request, 'addSections.html')



# POST PART
def postHomePage(request):
    post = Post.objects.all().filter(post_active=True)
    return render(request, 'post.html', {'post':post})

def postCreation(request):
    if request.method == "POST":
        create_post = Post.objects.create(user=request.user,post_name=request.POST.get('title'), post_description=request.POST.get('Description'),post_contact_number=request.POST.get('Phone_Number'),post_email=request.POST.get('email'),post_total_amount=request.POST.get('total_amount'),post_hours=request.POST.get('hours'))
        create_post.post_active = True
        create_post.save()
        print(request.POST.get('title'))
        print(request.POST.get('Description'))
        print(request.POST.get('Phone_Number'))
        print(request.POST.get('email'))
        print(request.POST.get('total_amount'))
        print(request.POST.get('hours'))
        return redirect('postHomePage')
    return render(request, 'postform.html')



# scholarship part
@login_required(login_url='login')
def student_concession(request):
    '''
        if request.user.refugee == True:
        return redirect('scholarship_not_allowed')

    '''

    if request.user.low_income_student == True:
        return redirect('scholarship_applied')

    if request.method=="POST":
        scholarship = Scholarship.objects.create(user=request.user, educational_background=request.POST.get('educational_background'), annual_income=request.POST.get('annual_income'), employment_status=request.POST.get('employment_status'), low_income_student_certificate=request.POST.get('low_income_student_certificate'), students_affordable_money=request.POST.get('students_affordable_money'), students_affordable_money_reason=request.POST.get('students_affordable_money_reason'), reson_for_applying=request.POST.get('reson_for_applying'), goals_achieved_by_this_course=request.POST.get('goals_achieved_by_this_course'))
        request.user.low_income_student = True
        request.user.save()
        scholarship.save()
        '''
        print(request.POST.get('educational_background'))
        print(request.POST.get('annual_income'))
        print(request.POST.get('employment_status'))
        print(request.POST.get('low_income_student_certificate'))

        print(request.POST.get('students_affordable_money'))
        print(request.POST.get('students_affordable_money_reason'))
        print(request.POST.get('reson_for_applying'))
        print(request.POST.get('goals_achieved_by_this_course'))
        '''
        return redirect('scholarship_applied')
    return render(request, 'studentconcession.html')

@login_required(login_url='login')
def refugee(request):
    '''

    if request.user.low_income_student == True:
        return redirect('scholarship_not_allowed')
    '''

    if request.user.refugee == True:
        return redirect('scholarship_applied')

    if request.method == "POST":
        scholarship = RefugeeDetails.objects.create(name=request.user, certificate=request.POST.get('certificate'))
        request.user.refugee = True
        request.user.save()
        scholarship.save()
        files = request.POST.get('certificate')
        print(files)
        return redirect('scholarship_applied')
    return render(request, 'refugee.html')


def Courses(request):
    return render(request, 'courses.html')
