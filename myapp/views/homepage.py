from django.shortcuts import render, redirect
from django.http import FileResponse
from myapp.models import File
from urllib.parse import urlencode
from urllib.parse import quote
from django.core.mail import EmailMessage
from django.conf import settings
import threading
from django.template.loader import render_to_string
from django.contrib import messages
import mimetypes
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import StreamingHttpResponse

# Home page

# @login_required(login_url='login')


def home(request):
    
    # retrieves a query parameter value from an HTTP GET request
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    # Q filters object that can be encapsulated logically

    pdf_files = File.objects.filter(
        Q(title__icontains=q) |
        Q(description__icontains=q) |
        Q(file__icontains=q) |
        Q(file_type__icontains=q),
        file_type='pdf'
    ).order_by('-created')
    
    image_files = File.objects.filter(
        Q(title__icontains=q) |
        Q(description__icontains=q) |
        Q(file__icontains=q) |
        Q(file_type__icontains=q),
        file_type='image'
    ).order_by('-created')
    
    audio_files = File.objects.filter(
        Q(title__icontains=q) |
        Q(description__icontains=q) |
        Q(file__icontains=q) |
        Q(file_type__icontains=q),
        file_type='audio'
    ).order_by('-created')
    
    video_files = File.objects.filter(
        Q(title__icontains=q) |
        Q(description__icontains=q) |
        Q(file__icontains=q) |
        Q(file_type__icontains=q),
        file_type='video'
    ).order_by('-created')

    context = {
        'pdf_files': pdf_files,
        'image_files': image_files,
        'audio_files': audio_files,
        'video_files': video_files,
    }
    return render(request, "myapp/home.html", context)


@login_required(login_url='login')
def downloadFile(request, pk):
    file = File.objects.get(id=pk)
    
    # increase number of downloads of a particular
    file.downloads_count()
    messages.success(request, 'Download successfully.')
    return redirect('home')


# allows the email to be sent asynchronously while the main program continues to execute.
class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


@login_required(login_url='login')
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

    # Open the file in binary mode and read only
    with open(file_obj.file.path, 'rb') as f:
        file_content = f.read()
        
        # Guess the content type of the file based on it's extension
        # Disregard the encoding part using the underscore
        content_type, _ = mimetypes.guess_type(file_obj.file.path)
        print(f'{content_type} -- content tupes')
        
        # Attach the file to the email
        email.attach(file_obj.file.name, file_content, content_type)

    # Send the email using a different process other than the main program execution
    if not settings.TESTING:
        EmailThread(email).start()

    # Update the file's emails_sent count
    file_obj.emails_sent_count()
    messages.success(request, 'Email successfully sent.')
    return redirect('home')


# Preview PDF by sending files as httpresponse

def previewPdf(request, pk):
    file = File.objects.get(id=pk)

    # pdf is streamed in chunks, rather than loading entire file
    def file_iterator():
        with open(file.file.path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                yield chunk
                
    # use StreamingHttpResponse to load pdf content
    response = StreamingHttpResponse(
        file_iterator(), content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="{}"'.format(
        urlencode({'': file.file.name}))
    return response
