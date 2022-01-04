from django.urls import path
from . import views

urlpatterns = [
    path('',views.dashboard, name='dashboard'),
    path('create-post/',views.create_post, name='createpost'),
    path('delete-post/<int:post_id>/',views.delete_post, name='deletepost'),
    path('profile/<str:username>/',views.profile, name='profile'),
    path('profile/<int:user_id>/follow',views.follow_user, name='follow_user'),
    path('profile/<int:user_id>/unfollow',views.unfollow_user, name='unfollow_user'),

    path('create-comment/<int:post_id>/<str:username>/',views.create_comment, name='createcomment'),
    path('delete-comment/<int:comment_id>/',views.delete_comment, name='deletecomment'),

    path('like-post/<int:post_id>/<str:username>/',views.like_post, name='likepost'),

    path('editar-bio/<int:user_id>/',views.load_screen_bio, name='loadScreenBio'),

    path('notifications/',views.notifier, name='notifications'),
    path('msg-viewed/<int:notification_id>/<str:status>/',views.update_status_notification, name='updateNotifications'),
    path('delete-notification/<int:notification_id>',views.delete_notification, name='deletenotifications'),
    ]