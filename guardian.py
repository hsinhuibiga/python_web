#guardian package import
#perm means permission
#import decorators

from guardian.shortcuts import assign_perm, get_perms
from guardian.core import ObjectPermissionChecker

from guardian.decorators import permission_required

#the authority of the global perms
# why to transform pk to int type
#Create guardian database tables by running: python manage.py migrate
# regulate the delete rule
#need to identify the id and pk
class DeletePost(View):
    @method_decorator(permission_required('main.delete_post', (models.Post, 'id', 'pk'), accept_global_perms=True))
    def get(self, request, pk):
        try:
            pk = int(pk)
            cur_post = models.Post.objects.get(pk=pk)
            is_draft = cur_post.is_draft

            url = reverse('main:admin_posts')
            if is_draft:
                url = '{0}?draft=true'.format(url)

            cur_post.delete()

        except models.Post.DoesNotExist:
            raise Http404

        return redirect(url)

#from database migrate the data
#user and group authority

# if not use pk but use jack, we need to get some user information

    from django.contrib.auth.models import User, Group
    >> > jack = User.objects.create_user('jack', 'jack@example.com', 'topsecretagentjack')
    >> > admins = Group.objects.create(name='admins')
    >> > jack.has_perm('change_group', admins)
    False
    >> > from guardian.models import UserObjectPermission
    >> > UserObjectPermission.objects.assign_perm('change_group', jack, obj=admins)
    < UserObjectPermission: admins | jack | change_group >
    >> > jack.has_perm('change_group', admins)
    True

    from django.contrib import admin
    from myapp.models import Author
    from guardian.admin import GuardedModelAdmin

    # Old way:
    # class AuthorAdmin(admin.ModelAdmin):
    #    pass

    # With object permissions support
    class AuthorAdmin(GuardedModelAdmin):
        pass

    admin.site.register(Author, AuthorAdmin)

