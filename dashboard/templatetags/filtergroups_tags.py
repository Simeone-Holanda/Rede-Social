from django import template

register = template.Library()

@register.filter('name_group')
def name_group(likes,user_id):
    for like in likes:
        print(like.id)
        if user_id == like.author.id:
            return True
    return False