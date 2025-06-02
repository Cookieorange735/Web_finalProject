from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import Pet
from .forms import PetForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def adopt_pet(request):
    if hasattr(request.user, 'pet'):
        return redirect('view_pet')
    if request.method == 'POST':
        form = PetForm(request.POST)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.save()
            return redirect('view_pet')
    else:
        form = PetForm()
    return render(request, 'pets/adopt_pet.html', {'form': form})

@login_required
def view_pet(request):
    pet = request.user.pet
    pet.update_status()
    return render(request, 'pets/view_pet.html', {'pet': pet})

@login_required
def feed_pet(request):
    pet = request.user.pet
    pet.update_status()
    pet.hunger = max(pet.hunger - 20, 0)
    pet.happiness = min(pet.happiness + 5, 100)
    pet.save()
    return redirect('view_pet')

@login_required
def clean_pet(request):
    pet = request.user.pet
    pet.update_status()
    pet.cleanliness = min(pet.cleanliness + 20, 100)
    pet.save()
    return redirect('view_pet')

@login_required
def play_with_pet(request):
    pet = request.user.pet
    pet.update_status()
    pet.happiness = min(pet.happiness + 10, 100)
    pet.hunger = min(pet.hunger + 10, 100)
    pet.cleanliness = max(pet.cleanliness - 10, 0)
    pet.save()
    return redirect('view_pet')

def update_pet_status(pet):
    now = timezone.now()
    elapsed = (now - pet.last_updated).total_seconds() // 60  # 每分鐘更新一次

    if elapsed >= 1:
        minutes = int(elapsed)
        pet.hunger = min(pet.hunger + minutes * 1, 100)
        pet.happiness = max(pet.happiness - minutes * 1, 0)
        pet.cleanliness = max(pet.cleanliness - minutes * 1, 0)
        pet.last_updated = now
        pet.save()

@login_required
def view_pet(request):
    pet = request.user.pet
    update_pet_status(pet)
    return render(request, 'pets/view_pet.html', {'pet': pet})

@login_required
def pet_status(request):
    pet = request.user.pet
    update_pet_status(pet)
    return JsonResponse({
        'hunger': pet.hunger,
        'happiness': pet.happiness,
        'cleanliness': pet.cleanliness
    })
