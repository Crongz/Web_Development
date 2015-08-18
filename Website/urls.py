"""WebDev URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','blog.views.index'),
    url(r'^page/(?P<page>\d+)/$', 'blog.views.index'),
    url(r'^entry/(?P<entry_id>\d+)/$', 'blog.views.read'),
    url(r'^write/$', 'blog.views.write_form'),
    url(r'^add/post/$', 'blog.views.add_post'),
    url(r'^add/comment/$', 'blog.views.add_comment'),
    url(r'^get_comments/(?P<entry_id>\d+)/$', 'blog.views.get_comments'),
    url(r'^login/$', 'blog.views.login_user'),
    url(r'^logout/$', 'blog.views.logout_user'), 
    url(r'^add/user/$', 'blog.views.add_user'),
    url(r'^sign_up/$', 'blog.views.sign_up'),
    url(r'^reset/password_form/$', 'django.contrib.auth.views.password_reset', 
        {'template_name': 'reset_password/reset_password_form.html',
	'post_reset_redirect' : '/reset/password_sent'}, name='password_reset'),

    url(r'^reset/password_sent/$','django.contrib.auth.views.password_reset_done',
	{'template_name':'reset_password/reset_password_sent.html'},name='password_reset_sent'),

    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
	'django.contrib.auth.views.password_reset_confirm',
	{'template_name':'reset_password/reset_password_confirm.html'},name='password_reset_confirm'),

    url(r'^rest/password_complete/$', 
        'django.contrib.auth.views.password_reset_complete',
	{'template_name':'reset_password/reset_password_complete.html'},name='password_reset_complete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

