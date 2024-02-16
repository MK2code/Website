from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMessage
import random, string

#################### index####################################### 
def index(request):
	return render(request, 'user/index.html', {'title':'index'})

########### register here ##################################### 
otp_storage= {}
forms = []
def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		forms.append(form)
		if form.is_valid():
			

			otp = ''.join(random.choices(string.digits, k=6))
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			otp_storage[email] = otp

			######################### mail system #################################### 
			htmly = get_template('user/Email.html')
			context = { 'username': username, 'otp': otp}
			subject, from_email, to = 'OTP for account verification', 'kumawat.7@iitj.ac.in', email
			html_content = htmly.render(context)
			msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
			msg.attach_alternative(html_content, "text/html")
			# msg.attach_alternative(f'<p>Your OTP is: <strong>{otp}</strong></p>', "text/html")
			msg.send()
			################################################################## 
			messages.info(request, 'An OTP has been sent to your email. Please enter it to complete registration.')
			
			return redirect("verify_otp")
	else:
		form = UserRegisterForm()
	return render(request, 'user/register.html', {'form': form, 'title':'register here'})

def verify_otp(request):
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        otp_entered = str(otp_entered)
        email = request.POST.get('email')  # Assuming you have a hidden input field with email in the form
        if email in otp_storage and str(otp_storage[email]) == str(otp_entered):
            # OTP is valid, register the user
            form = forms[0]
            if form.is_valid():
                form.save()
                del otp_storage[email]  # Remove OTP from storage after successful registration
                forms.clear()
                ###Email send to user
                htmly = get_template('user/Email2.html')
                context = { 'username': email }
                subject, from_email, to = 'Account created Succesfuly', 'kumawat.7@iitj.ac.in', email
                html_content = htmly.render(context)
                msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                messages.success(request, 'Your account has been created! You are now able to log in.')
                return redirect('login')
            else:	
                messages.error(request, 'Invalid form data.')
                return redirect('verify_otp')
        else:	
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect('verify_otp')
    else:
        # Display OTP verification form
        return render(request, 'user/verify_otp.html')


################ login forms################################################### 
def Login(request):
	if request.method == 'POST':

		# AuthenticationForm_can_also_be_used__

		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username = username, password = password)
		if user is not None:
			form = login(request, user)
			messages.success(request, f' welcome {username} !!')
			return redirect('index')
		else:
			messages.info(request, f'account done not exit plz sign in')
	form = AuthenticationForm()
	return render(request, 'user/login.html', {'form':form, 'title':'log in'})
