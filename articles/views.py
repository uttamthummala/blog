from django.shortcuts import render, redirect
from django.shortcuts import  get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Article
from .forms import ArticleForm
from django.db.models import Q
from django.contrib.auth import logout
from django.shortcuts import redirect
   

@login_required
def user_logout(request):
    logout(request)
    messages.success(request,"login Succesfull")
    return redirect('login') 

def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('dashboard')  
        else:
            messages.error(request, 'Invalid login credentials.')
    return render(request, 'login.html')

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            print("form is valid")
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
        else:
            messages.error(request, form.errors)
        
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


@login_required
def dashboard(request):
    articles_list = Article.objects.all()
    #get user
    

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request,"Post Succesfull")
            return redirect('dashboard')
        else:
            messages.error(request,form.errors)
 
    else:
        
        query = request.GET.get('q')
        filter_option = request.GET.get('filter_option')  
        articles = Article.objects.all()
        filter_mapping = {
            'title': 'title__icontains',
            'content': 'content__icontains',
            'tags': 'tags__icontains',
            'author': 'author__username__icontains',
        }

        # Check if the selected filter option is valid
        if filter_option in filter_mapping and query is not None:
            articles_list = articles.filter(**{filter_mapping[filter_option]: query})

        form = ArticleForm()

    # Pagination
    paginator = Paginator(articles_list, 3)  
    page = request.GET.get('page')

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    return render(request, 'dashboard.html',  {'articles': articles, 'form': form})

@login_required
def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    print(request.user.is_staff)
    return render(request, 'article_detail.html', {'article': article})
@login_required
def edit_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request,"Post Edited Succesfully")
            # Redirect to the updated article detail page
            return redirect('article_detail', article_id=article_id)
    else:
        form = ArticleForm(instance=article)

    return render(request, 'edit_article.html', {'form': form, 'article': article})
@login_required
def delete_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    article_title = article.title  

    if request.method == 'POST':
        article.delete()
        messages.success(request, f'The article "{article_title}" has been deleted.')
        return redirect('dashboard')

    return render(request, 'delete_article.html', {'article': article})


