from django.shortcuts import render, redirect
from myapp.forms import SignupForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str , DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings
import threading
from myapp.tokens import account_activation_token
from myapp.models import User
from django.urls import reverse

class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('authenticate/activate.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user)
    })

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email=settings.EMAIL_FROM_USER,
                         to=[user.email]
                         )

    if not settings.TESTING:
        EmailThread(email).start()

# Signup page
def signupPage(request):
    msg = None
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            send_activation_email(user, request)
            messages.add_message(request, messages.SUCCESS,
                                 'We sent you an email to verify your account')
            return redirect('login')
        else:
            msg = "Password don't match or email already exist"
    else:
        form = SignupForm()

    context = {'form': form, 'msg': msg}

    return render(request, "authenticate/signup.html", context)


# login page
def loginPage(request):
    form = LoginForm(request.POST or None)
    context = {'form': form}
    
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            
            if user and not user.is_email_verified:
                messages.add_message(request, messages.ERROR,
                                    'Email is not verified, please check your email inbox')
                return render(request, 'authenticate/login.html', context, status=401)
            elif user is not None and user.is_email_verified:
                login(request, user)
                return redirect('home')
            else:
                messages.add_message(request, messages.ERROR,
                                 'Invalid credentials, try again')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Error validating, try again')

    

    return render(request, "authenticate/login.html", context)


# Logout User
def logoutUser(request):
    logout(request)
    return redirect('login')

# activate user
def activate_user(request, uidb64, token):

    try:
        uid = force_str (urlsafe_base64_decode(uidb64))

        user = User.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user and account_activation_token.check_token(user, token):
        user.is_email_verified = True
        user.save()

        messages.add_message(request, messages.SUCCESS,
                             'Email verified, you can now login')
        return redirect(reverse('login'))

    return render(request, 'authenticate/activate-failed.html', {"user": user})