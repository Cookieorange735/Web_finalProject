from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import Pet
from .forms import PetForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # 註冊成功跳轉登入頁
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def adopt_pet(request):
    if hasattr(request.user, 'pet'):
        return redirect('view_pet')  # 已經有寵物就不能再養了

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
    pet = getattr(request.user, 'pet', None)
    return render(request, 'pets/view_pet.html', {'pet': pet})

@login_required
def feed_pet(request):
    pet = request.user.pet
    pet.hunger = max(pet.hunger - 20, 0)
    pet.happiness = min(pet.happiness + 5, 100)
    pet.save()
    return redirect('view_pet')

@login_required
def clean_pet(request):
    pet = request.user.pet
    pet.cleanliness = min(pet.cleanliness + 20, 100)
    pet.save()
    return redirect('view_pet')

@login_required
def play_with_pet(request):
    pet = request.user.pet
    pet.happiness = min(pet.happiness + 10, 100)
    pet.hunger = min(pet.hunger + 10, 100)
    pet.save()
    return redirect('view_pet')

# def pet_status(request):
#     pet = Pet.objects.get(owner=request.user)
#     pet.update_status()  # 每次查詢狀態時自動更新
#     return render(request, "pet_status.html", {"pet": pet})