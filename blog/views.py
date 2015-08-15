# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from blog.models import *
from django.shortcuts import render,redirect,render_to_response
from blog.forms import ImageUploadForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext

import md5

def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/write/')
    return render(request,'login.html', context_instance=RequestContext(request))

def index(request, page=1):

    per_page = 10
    start_pos = (page - 1) * per_page
    end_pos = start_pos + per_page
    
    page_title = '블로그 글 목록 화면'
    
    entries = Entries.objects.select_related().all().order_by('-created')[start_pos:end_pos]

    context={
        'page_title':page_title,
        'entries':entries,
        'current_page':page
    }
    return render(request, 'main.html', context)

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
    # 글쓴이 이름 처리
    if request.POST.has_key('name') == False:
        return HttpResponse('Missing name')
    else:
        if len(request.POST['name']) == 0:
            return HttpResponse('Name must be exist')
        else:
            cmt_name = request.POST['name']

    # 비밀번호
    if request.POST.has_key('password') == False:
        return HttpResponse('Missing password')
    else:
        if len(request.POST['password']) == 0:
            return HttpResponse('Password must be longer than one letter')
        else:
            cmt_password = md5.md5(request.POST['password']).hexdigest()

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
        new_cmt = Comments(Name=cmt_name, Password=cmt_password, Content=cmt_content, Entry=entry)
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
    return render(request,'comments.html',context)

def is_ajax(request):
    if dir(request).count('is_ajax') > 0:
        return request.is_ajax()
    else:
        return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'



