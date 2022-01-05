from accounts.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Comment, Like, Notification, Post, Follower


@login_required(redirect_field_name='login')
def dashboard(request):
    """ Método responável por redenriza a tela de dashboard com os posts dos seguidores. """
    fllws = Follower.objects.filter(user_profile=request.user.id)
    posts = []
    for flw in fllws:
        posts_flw = Post.objects.filter(author=flw.follower.id)
        posts += posts_flw 
    return render(request ,'dashboard/home.html', {"user": request.user, "posts": posts})


@login_required(redirect_field_name='login')
def create_post(request):
    """ Método responável por redenriza a tela de criação do post e criar-los. """

    current_user = request.user
    if request.method != 'POST':
        return render(request,'dashboard/createpost.html')

    msg = request.POST.get('text')
    post = Post.objects.create(text=msg,author=current_user)
    post.save()
    return redirect('dashboard')


@login_required(redirect_field_name='login')
def delete_post(request, post_id: int):
    """
    Método responsável por deletar postagens

    param:
        post_id: id do post que será deletado.
    
    return: 
        redireciona a pagina para a home
    """
    Post.objects.filter(id=post_id).delete()
    return redirect('dashboard')


@login_required(redirect_field_name='login')
def profile(request,username: str):
    """ 
        Método responável por redenriza a tela de perfil do usuario logado ou qualquer outro a plataforma.

        Param:
            username: nome de usuario que está entrando em um determinado perfil, 
                      seja dele ou de outra pessoa da plataforma.

    """
    
    visiting_user = User.objects.get(username=username)
    posts = Post.objects.filter(author=visiting_user.id)
    followers = Follower.objects.filter(user_profile=visiting_user)
    followers = [flw.follower for flw in followers.all()]
    user = request.user
    visiting_user.bio = visiting_user.bio.split('<br />')

    return render(request,'dashboard/profile.html', {"user": user,"visiting_user":visiting_user,"posts":posts,"followers":followers})



@login_required(redirect_field_name='login')
def create_comment(request, post_id: int ,username: str):
    """ Método responsável por criar um comentario em uma postagem. """

    text = request.POST.get('text')
    user = User.objects.get(username=username)
    post = Post.objects.get(id=post_id)
    comment = Comment.objects.create(text=text, author=user, post_id=post)
    comment.save()
    if user.username != post.author.username:
        Notification.objects.create(message=f"{username} Comentou sua publicação", status=True, author=post.author)
    return redirect('dashboard')


@login_required(redirect_field_name='login')
def delete_comment(request, comment_id: int):
    """ Método responsável por deletar um comentario feito por você ou é uma postagem sua. """

    Comment.objects.filter(id=comment_id).delete()
    return redirect('dashboard')


@login_required(redirect_field_name='login')
def like_post(request, post_id: int, username: str):
    """ Responsavel por verificar se o usuario já deu like na postagem.
        
        [NOTE]:Este método recebe um POST da função like no arquivo JS na base.

        Param:
            post_id: id do post que recebera o like
            username: nome de usuario logado atualmente
    """

    author = User.objects.get(username=username)
    post = Post.objects.get(id=post_id)
    for like in post.likes.all():
        if like.author.username==username:
            Like.objects.filter(id=like.id).delete()
            return JsonResponse({'liked': False,'count_likes':len(post.likes.all())}) 

    Like.objects.create(post_id=post, author=author)
    if request.user.username != post.author.username:
        Notification.objects.create(message=f"{username} Curtiu sua publicação", status=True, author=post.author)
    
    return JsonResponse({
        'liked': True,
        'count_likes':len(post.likes.all())})


def load_screen_bio(request,user_id : int):
    """ Método responsável por redenrizar a tela de bibliografia. """
    user = User.objects.get(id=user_id)
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        bio = request.POST.get('bio')
        new_bio = bio.replace('\n','<br />')

        user = User.objects.get(id=user_id)

        username_exist = User.objects.filter(username=username).exists()
        email_exist = User.objects.filter(email=email).exists()
        first_name_exist = User.objects.filter(first_name=first_name).exists()

        if username_exist and username != user.username:
            messages.error(request, "Erro, usuário ja existe!")
            return redirect('loadScreenBio', user_id=user_id)
        if email_exist and email != user.email:
            messages.error(request, "Erro, email ja existe!")
            return redirect('loadScreenBio', user_id=user_id)
        if first_name_exist and first_name != user.first_name:
            messages.error(request, "Erro, first name ja existe!")
            return redirect('loadScreenBio', user_id = user_id)
        if request.FILES:
            user.foto = request.FILES['foto-perfil']

        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        user.bio = new_bio
        user.save()
        return redirect('profile',username=user.username)

    return render(request,'dashboard/edit_bio.html', {"user":user})
    


def notifier(request):
    """ Método responsável por renderizar a tela de notificações. """
    user = request.user
    return render(request,'dashboard/notifications.html', {"user":user})


def update_status_notification(request, notification_id: int, status : str):
    """ Método responsável por atualiza o status da notificação. """

    notification = Notification.objects.get(id=notification_id)

    if status == 'true':
        notification.status = True
    else:
        notification.status = False

    notification.save()
    return JsonResponse({
           'status': status,
        })


def delete_notification(request, notification_id: int):
    """ Método responsável por deletar uma notificação. """
    Notification.objects.filter(id=notification_id).delete()
    return redirect('notifications')


def follow_user(request, user_id):
    """ Verificar se o usuario existe e ver se isso pode ser uma falha. """
    user_profile = User.objects.get(id=user_id)
    current_user = request.user
    print(current_user.username + " vai seguir " + user_profile.username)
    Follower.objects.create(status=True,user_profile=user_profile,follower=current_user)
    return redirect('profile',username=user_profile.username)


def unfollow_user(request, user_id):
    """ Verificar se o usuario existe e ver se isso pode ser uma falha. """
    user_profile = User.objects.get(id=user_id)
    current_user = User.objects.get(id=request.user.id)
    Follower.objects.filter(user_profile=user_profile,follower=current_user).delete()
    print("deletado o seguidor " + current_user.username + " de " + user_profile.username )
    return redirect('profile',username=user_profile.username)



    