from django.shortcuts import render, redirect
from django.http import HttpResponse
from myapp.models import File
from django.core.mail import EmailMessage
from django.conf import settings
import threading
from django.template.loader import render_to_string
from django.contrib import messages
import mimetypes
from django.db.models import Q

# Home page


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    pdf_files = File.objects.filter(
        Q(title__icontains=q) | 
        Q(description__icontains=q) | 
        Q(file__icontains=q) | 
        Q(file_type__icontains=q),
        file_type='pdf'
    )
    image_files = File.objects.filter(
        Q(title__icontains=q) | 
        Q(description__icontains=q) | 
        Q(file__icontains=q) | 
        Q(file_type__icontains=q),
        file_type='image'
    )
    audio_files = File.objects.filter(
        Q(title__icontains=q) | 
        Q(description__icontains=q) | 
        Q(file__icontains=q) | 
        Q(file_type__icontains=q),
        file_type='audio'
    )
    video_files = File.objects.filter(
        Q(title__icontains=q) | 
        Q(description__icontains=q) | 
        Q(file__icontains=q) | 
        Q(file_type__icontains=q),
        file_type='video'
    )
    
    print(pdf_files)

    context = {
        'pdf_files': pdf_files,
        'image_files': image_files,
        'audio_files': audio_files,
        'video_files': video_files,
    }
    return render(request, "myapp/home.html", context)


def downloadFile(request, pk):
    file_obj = File.objects.get(id=pk)
    print("download successfull")
    file_obj.downloads_count()
    messages.success(request, 'Download successfully.')
    return redirect('home')


def emailFile(request, pk):
    user = request.user
    # Retrieve the file object
    file_obj = File.objects.get(id=pk)

    # Create an EmailMessage object
    email = EmailMessage(
        subject='File Attachment',
        body=render_to_string('myapp/send_email.html',
                              {'user': user, 'file_obj': file_obj}),
        from_email=settings.EMAIL_FROM_USER,
        to=[user.email]
    )

    # Attach the file to the email
    with open(file_obj.file.path, 'rb') as f:
        file_content = f.read()
        content_type, _ = mimetypes.guess_type(file_obj.file.path)
        email.attach(file_obj.file.name, file_content, content_type)

    # Send the email
    if not settings.TESTING:
        EmailThread(email).start()

    # Update the file's emails_sent count
    file_obj.emails_sent_count()
    messages.success(request, 'Email successfully sent.')
    return redirect('home')


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()
