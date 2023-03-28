from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate,login, logout
from .tokens  import generate_token
# Create your views here.
def home(request):
    return render(request,"login_page/index.html")

def signup(request):
    if request.method == "POST"  :
        username = request.POST.get('username')
        #username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        key1 = request.POST['key']

        if User.objects.filter(username =username):
            messages.error(request,'Username Already Exists')
            return redirect('home')
        
        if User.objects.filter(email = email):
            messages.error(request,'Email Already Exists')
            return redirect('home')

        if key1 != 'iitj':
            messages.error(request, "Wrong pin. Please Contact administrator") 
            return redirect("home")
        
        myuser = User.objects.create_user(username, email, password)

        myuser.is_active=False
        messages.success(request, "Account created successfully.Check your mailbox")

        subject  = "Welcome to IITJ's plag check interface"
        message = "Just for testing purpose"

        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject,message,from_email,to_list,fail_silently =False)

        #writing code for activating account if clicked on confirmation email
        current_site = get_current_site(request)
        email_subject = 'Confirm Your email'
        message2 = render_to_string('login_page/email_confirmation.html',{
            'name':myuser.username,
            'domain':current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token':generate_token.make_token(myuser),
            })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = False
        email.send()
        myuser.save()
        return redirect('signin')

            
    else:
        return render(request, "login_page/signup.html")


def signin(request):
    if request.method == 'POST':
        username1 = request.POST['username']
        password1 = request.POST['password']

        user = authenticate(username = username1, password=password1)
        if user is not None:
            login(request,user)
            username = user.username
            return render(request, "login_page/index.html", {'username':username})
        else:
            messages.error(request, "Wrong Username or password")
            return redirect('home')

    return render(request,"login_page/signin.html")
    


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully")
    return redirect('home')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk = uid)
    except(TypeError,ValueError,OverflowError, User.DoesNotExist):
        myuser = None
        
    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active=True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return(request,'activation_failed.html')
