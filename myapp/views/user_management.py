from django.shortcuts import render, redirect
from myapp.forms import SignupForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
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

# Signup page
def signupPage(request):
    msg = None
    
    # saves form and send activation code, then redirect to login
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

    return render(request, "authenticate/login.html", context)


# login page
def loginPage(request):
    form = LoginForm(request.POST or None)
    context = {'form': form, 'page':'login'}
    
    # if user is authenticated, redirect to home, when user tries to access login
    if request.user.is_authenticated:
        return redirect('home')
    
    # Check if user is authenticated before login to home
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


# allows the email to be sent asynchronously while the main program continues to execute.
class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

# sends activation code to the email
def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    
    # render a template file and pass in context
    email_body = render_to_string('authenticate/activate.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user)
    })

    # create an email from using EmailMessage()
    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email=settings.EMAIL_FROM_USER,
                         to=[user.email]
                         )

    # creates a different process for email other than the main program process
    if not settings.TESTING:
        EmailThread(email).start()


# activate user
def activate_user(request, uidb64, token):

    # decode uid64 back to the user id, and get the user
    try:
        uid = force_str (urlsafe_base64_decode(uidb64))

        user = User.objects.get(pk=uid)

    except Exception as e:
        user = None

    # checks the user and token with the token generated from token.py   
    if user and account_activation_token.check_token(user, token):
        user.is_email_verified = True
        user.save()

        messages.add_message(request, messages.SUCCESS,
                             'Email verified, you can now login')
        return redirect(reverse('login'))

    return render(request, 'authenticate/activate-failed.html', {"user": user})