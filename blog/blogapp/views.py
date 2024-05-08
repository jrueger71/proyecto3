# from django.shortcuts import render, get_object_or_404, redirect
# from .models import Post, Comment
# from .forms import PostForm, CommentForm

# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.decorators import login_required  # Importa el decorador
# from .models import Post, Comment
# from .forms import CommentForm




from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .models import Post, Comment, Article
from .forms import CommentForm, PostForm
from .forms import SignUpForm


def post_list(request):
    posts = Post.objects.order_by('-date_posted')
    return render(request, 'blogapp/post_list.html', {'posts': posts})

def acerca_de(request):
    return render(request, 'blogapp/about.html')

def contacto(request):
    return render(request, 'blogapp/contact.html')

def login(request):
    return render(request, 'registration/login.html')

def nuevo_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogapp/post_list.html')
    else:
        form = PostForm()
    return render(request, 'blogapp/admin.html', {'form': form})


@login_required  # Aplica el decorador
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blogapp/post_detail', pk=pk)
    else:
        form = CommentForm()
    return render(request, 'blogapp/post_detail.html', {'post': post, 'form': form})




def home(request):
    articles = Article.objects.all()
    return render(request, 'home.html', {'articles': articles})

@login_required
def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    comments = article.comments.all()  # Obtiene todos los comentarios asociados a este artículo
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.save()
            return redirect('article_detail', article_id=article_id)
    else:
        form = CommentForm()
    return render(request, 'article_detail.html', {'article': article, 'comments': comments, 'form': form})

#class CustomLoginView(LoginView):
#    template_name = 'login.html'


# def signup(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')
#     else:
#         form = SignUpForm()
#     return render(request, 'registration/signup.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('blogapp/post_list')  # Redirige a donde quieras después del registro exitoso
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})