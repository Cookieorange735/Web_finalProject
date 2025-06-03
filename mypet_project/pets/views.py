from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone

from .models import Pet
from .forms import PetForm

# 註冊帳號
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# 領養寵物
@login_required
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

# 檢視寵物狀態（主畫面）
@login_required
def view_pet(request):
    pet = getattr(request.user, 'pet', None)
    if not pet:
        return redirect('adopt_pet')

    update_pet_status(pet)

    # 根據清潔度改變狀態
    status = 'bath' if pet.cleanliness < 30 else 'normal'

    return render(request, 'pets/view_pet.html', {
        'pet': pet,
        'status': status
    })

# 餵食
@login_required
def feed_pet(request):
    pet = request.user.pet
    pet.update_status()
    pet.hunger = max(pet.hunger - 20, 0)
    pet.happiness = min(pet.happiness + 5, 100)
    pet.save()
    return redirect('view_pet')

# 清潔
@login_required
def clean_pet(request):
    pet = request.user.pet
    pet.update_status()
    pet.cleanliness = min(pet.cleanliness + 20, 100)
    pet.save()
    return redirect('view_pet')

# 玩耍
@login_required
def play_with_pet(request):
    pet = request.user.pet
    pet.update_status()
    pet.happiness = min(pet.happiness + 10, 100)
    pet.hunger = min(pet.hunger + 10, 100)
    pet.cleanliness = max(pet.cleanliness - 10, 0)
    pet.save()
    return redirect('view_pet')

# 更新寵物狀態（依時間衰減）
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

# 提供 JSON 給前端 JS 使用（即時更新）
@login_required
def pet_status(request):
    pet = request.user.pet
    update_pet_status(pet)
    return JsonResponse({
        'hunger': pet.hunger,
        'happiness': pet.happiness,
        'cleanliness': pet.cleanliness
    })
