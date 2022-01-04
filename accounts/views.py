from .models import User
from django.shortcuts import redirect, render
from django.contrib import auth, messages


def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')
    
    username = request.POST.get('username')
    password = request.POST.get('password')

    user_exist = auth.authenticate(username=username, password=password)

    if not user_exist:
        # manda uma mensagem de erro
        messages.error(request, "Usuário não existe.")
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user_exist)
        messages.success(request, "Usuário logado!")
        return redirect('dashboard')

def cadastro(request):
    if request.method != 'POST':
        return render(request, 'accounts/cadastro.html')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    username = request.POST.get('username')
    email = request.POST.get('email')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')
    
    bio = request.POST.get('bio')
    new_bio = bio.replace('\n','<br />')

    username_exist = User.objects.filter(username=username).exists()
    email_exist = User.objects.filter(email=email).exists()
    first_name_exist = User.objects.filter(first_name=first_name).exists()

    if username_exist:
        messages.error(request, "Erro no cadastro, usuário ja existe!")
        return redirect('cadastro')
    if email_exist:
        messages.error(request, "Erro no cadastro, email ja existe!")
        return redirect('cadastro')
    if first_name_exist:
        messages.error(request, "Erro no cadastro, first name ja existe!")
        return redirect('cadastro')
    if password1 != password2:
        messages.error(request, "Erro no cadastro, senhas não são iguais!")
        return redirect('cadastro')

    user = User.objects.create_user(
                username=username, email=email,
                first_name= first_name, last_name = last_name,
                password=password1, bio=new_bio,foto='/avatar-sem-foto.png'
                )
    user.save()
    messages.success(request, "Usuário Cadastrado!")
    return redirect('login')




def logout(request):
    auth.logout(request)
    return redirect('login')
