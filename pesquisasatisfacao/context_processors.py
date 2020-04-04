from pesquisasatisfacao.core.models import Group

def groups(request):
    groups = Group.objects.all()
    return{
        'groups': groups
    }
