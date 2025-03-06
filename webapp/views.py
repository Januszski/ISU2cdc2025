import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from pip._internal.utils import logging

from .models import DownloadLink, SoftwareVersion
from .forms import EmailForm
from django.utils.crypto import get_random_string
import os
from django.http import FileResponse, HttpResponseForbidden
from django.contrib.auth.models import User
from .forms import RegistrationForm
from ldap3 import Server, Connection, ALL
from django.contrib.auth.decorators import login_required
import base64
import pickle
from django.urls import reverse
import sqlite3

def home(request):
    versions = SoftwareVersion.objects.all()
    return render(request, "webapp/home.html", {"versions": versions})


def request_download(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        token = get_random_string(32)

        download_link = DownloadLink.objects.create(
            email=email,
            token=token
        )
        download_url = reverse('download_ready', args=[token])
        os.system(f"echo {email} >> /Users/jan/ISU2cdc/ISU2cdc2025/mailing-list")

        return redirect(download_url)

    return render(request, 'webapp/request_download.html')

def download_ready(request, token):
    download_link = get_object_or_404(DownloadLink, token=token)

    if download_link.used:
        return HttpResponseForbidden("This download link has already been used.")

    files = []
    if request.method == 'GET':
        download_dir = settings.DOWNLOADS_ROOT
        files = os.listdir(download_dir)

        files = [f for f in files if os.path.isfile(os.path.join(download_dir, f))]

    if request.method == 'POST':
        file_name = request.POST.get('file_name')
        if file_name:
            file_path = os.path.join(settings.DOWNLOADS_ROOT, file_name)

            if os.path.exists(file_path):
                download_link.used = True
                download_link.save()

                response = FileResponse(open(file_path, 'rb'))
                response['Content-Type'] = 'application/octet-stream'
                response['Content-Disposition'] = f'attachment; filename={file_name}'
                return response

    return render(request, "webapp/download_ready.html", {
        "download_link": download_link,
        "files": files
    })


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']

            # Connect to Active Directory and create the user
            server = Server('localhost', get_info=ALL)
            conn = Connection(server, user='cn=admin,dc=example,dc=org', password='admin', auto_bind=True)

            # Prepare the DN (Distinguished Name) for the new user
            dn = f"cn={username},ou=users,dc=example,dc=org"

            # Use correct object classes and attributes for the new user
            attributes = {
                'objectClass': ['top', 'person', 'organizationalPerson', 'inetOrgPerson'],
                'cn': username,
                'sn': last_name,
                'givenName': first_name,
                'mail': email,
                'userPassword': password
            }

            encoded_password = base64.b64encode(password.encode()).decode('utf-8')
            attributes['userPassword'] = encoded_password

            # Add the user to AD
            conn.add(dn, attributes=attributes)

            if conn.result['result'] == 0:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                return redirect('login')
            else:
                return render(request, 'register.html', {'form': form, 'error': 'Failed to create user in AD'})

    else:
        form = RegistrationForm()

    return render(request, 'webapp/register.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    user_prefs_path = f"user_data/{user.username}_prefs.pickle"

    if os.path.exists(user_prefs_path):
        with open(user_prefs_path, "rb") as f:
            preferences = pickle.load(f)
    else:
        preferences = {"theme": "light"}

    if request.method == "POST":
        pickled_theme = request.POST.get("theme")

        try:

            decoded_bytes = base64.b64decode(pickled_theme)
            new_theme = pickle.loads(decoded_bytes)


            if isinstance(new_theme, str):
                preferences["theme"] = new_theme

                # Save updated preferences
                os.makedirs(os.path.dirname(user_prefs_path), exist_ok=True)
                with open(user_prefs_path, "wb") as f:
                    pickle.dump(preferences, f)

        except Exception as e:
            print(f"Failed to decode/unpickle theme: {e}")

        return redirect("profile")

    return render(request, "webapp/profile.html", {"user": user, "preferences": preferences})