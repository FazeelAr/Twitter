from django.shortcuts import render, redirect

# Create your views here.
from .models import Tweet, Comment, Like
from .forms import TweetForm, UserRegisterationForm
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
# Like a tweet
from django.http import JsonResponse
from django.views.decorators.http import require_POST



def home(request):
    return render(request,'layout.html')

def index(request):
    return render(request,'tweet/index.html')

def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request,'tweet/tweet_list.html',{
        'tweets':tweets
    })

@login_required
def tweet_create(request):
    form = None
    if request.method == 'POST':
        form = TweetForm(request.POST,request.FILES)
        if form.is_valid():
            tweet=form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()
        return render(request,'tweet/tweet_form.html',{
            'form':form
        })

@login_required
def tweet_edit(request,tweet_id):
    tweet = get_object_or_404(Tweet,pk=tweet_id,
                               user = request.user)
    if request.method == 'POST':
        form = TweetForm(request.POST,request.FILES,
                         instance=tweet)
        if form.is_valid():
            tweet = form.save(commit= False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
        return render(request,'tweet/tweet_form.html',{
            'form':form
        })

@login_required
def tweet_delete(request,tweet_id):
    tweet = get_object_or_404(Tweet,pk = tweet_id, user = request.user)
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
    
    else:
        return render(request,'tweet/tweet_confirm_delete.html',{
            'tweet':tweet
        })
    

def register(request):
    if request.method == 'POST':
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request,user)
            return redirect('tweet_list')
    else:
        form = UserRegisterationForm()
    return render(request, 'registration/register.html',{
        'form':form
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('tweet_list')  # or wherever you want
        else:
            # Authentication failed
            return render(request, 'registration/login.html', {'error': 'Invalid username or password.'})
    
    return render(request, 'registration/login.html')

def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return render(request, 'registration/logout.html')  # or wherever you want



@require_POST
def like_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    like_exists = Like.objects.filter(user=request.user, tweet=tweet).exists()
    
    if like_exists:
        Like.objects.filter(user=request.user, tweet=tweet).delete()
        liked = False
    else:
        Like.objects.create(user=request.user, tweet=tweet)
        liked = True
    
    return JsonResponse({
        'liked': liked,
        'like_count': tweet.like_count  # Uses the @property from the Tweet model
    })
# Add a comment
def add_comment(request, tweet_id):
    tweet = Tweet.objects.get(id=tweet_id)
    Comment.objects.create(
        user=request.user,
        tweet=tweet,
        text=request.POST.get('comment_text')
    )
    return redirect('tweet_detail', tweet_id=tweet_id)


def tweet_detail(request, tweet_id):
    tweet = Tweet.objects.get(id=tweet_id)
    comments = tweet.comments.all().order_by('-created_at')
    return render(request, 'tweets/tweet_detail.html', {
        'tweet': tweet,
        'comments': comments,
    })