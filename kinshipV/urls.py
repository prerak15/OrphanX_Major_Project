"""kinshipV URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('',views.index, name='index'),
    # path('home/',views.index, name='index')
    path('',views.landpage, name='land'),
    path('home/',views.landpage, name='land'),
    path('formParent/',views.formpageP, name='form'),
    path('formChild/',views.formpageC, name='form'),
    path('try/',views.index, name='index'),
    path('upload_file_parent/',views.handle_file_upload_parent, name='file_upload_parent'),
    path('upload_file_child/',views.handle_file_upload_child, name='file_upload_child'),
    path('child_details/',views.child_details_display, name='view_child_details')


]+static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)
