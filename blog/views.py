# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from blog.models import *
from django.shortcuts import render,redirect,render_to_response
from blog.forms import ImageUploadForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

import md5

def login_user(request):
    logout(request)
    username = password = ''
    state = 'Please login to write a post on Mini-reddit'
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
	    else:
		state = 'Use user with admin control'
	else:
	    state = 'Invaild Password or Username. Please try it again.'
    context = {'username': username, 'state': state}
    return render(request,'login.html', context)

def logout_user(request):
    logout(request)
    return redirect('/')

def sign_up(request):
    return render(request, 'signup_form.html')

def add_user(request):
    # 글쓴이 이름 처리
    if request.POST.has_key('username') == False:
        return HttpResponse('Missing name')
    else:
	username = request.POST['username']
        if len(username) == 0:
            return HttpResponse('username must be exist')
	elif User.objects.filter(username=username).exists():
	    return HttpResponse('someone is using this uesrname')
        else:
            user_username = username

    # 비밀번호
    user_password = request.POST['inputPassword']

    # Email
    email=request.POST['email']
    if len(email) == 0:
            return HttpResponse('Email must be longer than one letter')
    elif User.objects.filter(email=email).exists():
	    return HttpResponse('someone is using email') 
    else:
            user_email = email

    # 글쓴이 이름 처리
    user_first_name = request.POST['first_name']

    # 글쓴이 이름 처리
    user_last_name = request.POST['last_name']
    
    try:
        user = User.objects.create_user(username=user_username, email=user_email, password=user_password)
	user.first_name=user_first_name
	user.last_name=user_last_name
	user.save()
	return redirect('/')
	#return HttpResponse(new_user)
    except:
        return HttpResponse('Error: couldnt create user')
    return HttpResponse('Err`or: End of the program. Didnt happened anything')    

def reset_password_form(request):
    return render(request, 'reset_password/reset_password_form.html')


def status(request):
    status=''
    if request.user.is_authenticated():
	status = 'Log Out'
    return status

def index(request, page=1):

    per_page = 10
    start_pos = (page - 1) * per_page
    end_pos = start_pos + per_page
    
    page_title = '블로그 글 목록 화면'
    
    entries = Entries.objects.select_related().all().order_by('-created')[start_pos:end_pos]

    context={
        'page_title':page_title,
        'entries':entries,
        'current_page':page,
    }
    return render(request, 'list.html', context)

def read(request, entry_id=None):
    page_title = '블로그 글 읽기 화면'
    
    try:
        current_entry = Entries.objects.get(id=int(entry_id))
    except:
        return HttpResponse('Post does not exist anymore')

    try:
        prev_entry = current_entry.get_previous_by_created()
    except:
        prev_entry = None
    
    try:
        next_entry = current_entry.get_next_by_created()
    except:
        next_entry = None

    comments = Comments.objects.filter(Entry=current_entry).order_by('created')
    
    context={
        'page_title':page_title,
        'current_entry':current_entry,
        'prev_entry':prev_entry,
        'next_entry':next_entry,
        'comments':comments
    }
    return render(request, 'read.html', context)

@login_required(login_url = '/login/')
def write_form(request):
    page_title = '블로그 글 쓰기 화면'
    
    categories = Categories.objects.all()
    context={
        'page_title':page_title,
        'categories':categories
    }
    return render(request, 'write_form.html', context)



def add_post(request):
    
    # 글 제목 처리
    if request.POST.has_key('title') == False:
        return HttpResponse('Missing title of the post')
    else:
        if len(request.POST['title']) == 0:
            return HttpResponse('Title must be longer than one letter')
        else:
            entry_title = request.POST['title']

    # 글 본문 처리
    if request.POST.has_key('content') == False:
        return HttpResponse('Missing content of the post')
    else:
        if len(request.POST['content']) == 0:
            return HttpResponse('Content must be longer than one letter')
        else:
            entry_content = request.POST['content']

    # 글 갈래 처리
    if request.POST.has_key('category') == False:
        return HttpResponse('Must choose category')
    else:
        try:
            entry_category = Categories.objects.get(id=request.POST['category'])
        except:
            return HttpResponse('Invaild category')

    # 글 꼬리표 처리
    
    if request.POST.has_key('tags') == True:
        tags = map(lambda str: str.strip(), unicode(request.POST['tags']).split(','))
        tag_list = map(lambda tag: TagModel.objects.get_or_create(Title=tag)[0], tags)
    else:
        tag_list = []
    #계정확인   &  이미지 업로드
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
	    entry_user = request.user
            entry_image=request.FILES['image']
	    new_entry = Entries(User = entry_user, Title=entry_title, Content=entry_content, Category=entry_category, Image=entry_image)
    	else:
	    entry_user = request.user
            new_entry = Entries(User = entry_user, Title=entry_title, Content=entry_content, Category=entry_category)
    
    #꼬리표 임시추가 
    try:
        new_entry.save()
    except:
        return HttpResponse('Error: incomplete save for tag')
    
    # 꼬리표 추가
    for tag in tag_list:
        new_entry.Tags.add(tag)
        
    # 최종 저장.
    if len(tag_list) > 0:
        try:
            new_entry.save()
        except:
            return HttpResponse('Error: incomeplete saving')
    return redirect('/')
    #return HttpResponse(' Successfully saved post number %s' % new_entry.id)



def add_comment(request):    
    # 댓글 본문 처리
    if request.POST.has_key('content') == False:
        return HttpResponse('Missing content')
    else:
        if len(request.POST['content']) == 0:
            return HttpResponse('Content must be longer than one letter')
        else:
            cmt_content = request.POST['content']

    # 댓글 달 글 확인
    if request.POST.has_key('entry_id') == False:
        return HttpResponse('Missing targat to comment')
    else:
        try:
            entry = Entries.objects.get(id=request.POST['entry_id'])
        except:
            return HttpResponse('Post does not exsit anymore')

    try:
        new_cmt = Comments( User=request.user, Content=cmt_content, Entry=entry)
        new_cmt.save()
        entry.Comments += 1
        entry.save()
	return redirect('/entry/%s' %request.POST['entry_id'])
	#return HttpResponse('Successfully added comment')
    except:
        return HttpResponse('Error: while adding comment to server')
    return HttpResponse('Err`or: End of the program. Didnt happened anything')

def get_comments(request, entry_id=None, is_inner=False):    
    try:
        current_entry = Entries.objects.get(id=int(entry_id))
    except:
        return HttpResponse('그런 글이 존재하지 않습니다.')
        
    comments = Comments.objects.filter(Entry=current_entry).order_by('created')

    if is_ajax(request):
        with_layout = False
    else:        
        with_layout = True
    
    context={
    	'current_entry':current_entry,
        'comments':comments,
        'with_layout':with_layout
    }
    return render(request,'comments_only.html',context)

def is_ajax(request):
    if dir(request).count('is_ajax') > 0:
        return request.is_ajax()
    else:
        return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'



