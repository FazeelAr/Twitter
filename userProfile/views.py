from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Profile
# Create your views here.

from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from .models import Profile
from tweet.models import Tweet  # Import your Tweet model

def profile_view(request, username):
    user_obj = get_object_or_404(User, username=username)
    
    try:
        profile = user_obj.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user_obj)
    
    # Get all tweets by this user, ordered by most recent first
    tweets = Tweet.objects.filter(user=user_obj).order_by('-created_at')
    
    context = {
        'profile_user': user_obj,
        'profile': profile,
        'tweets': tweets,  # Add tweets to the context
    }
    
    return render(request, 'userProfile/profile_view.html', context)


from .forms import ProfileForm

@login_required
def edit_profile(request, username):
    profile = get_object_or_404(Profile, user__username=username)

    if request.user != profile.user:
        return redirect('userProfile:profile_view', username=username)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('userProfile:profile_view', username=username)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'userProfile/edit_profile.html', {'form': form, 'profile': profile})
