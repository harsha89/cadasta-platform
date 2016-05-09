from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.shortcuts import redirect

from ..models import Organization, Project


class OrganizationMixin:
    def get_organization(self, lookup_kwarg='slug'):
        if not hasattr(self, 'org'):
            self.org = get_object_or_404(Organization,
                                         slug=self.kwargs[lookup_kwarg])
        return self.org

    def get_perms_objects(self):
        return [self.get_organization()]


class OrganizationRoles(OrganizationMixin):
    lookup_field = 'username'

    def get_queryset(self):
        self.org = self.get_organization()
        return self.org.users.all()

    def get_serializer_context(self, *args, **kwargs):
        context = super(OrganizationRoles, self).get_serializer_context(
            *args, **kwargs)
        context['organization'] = self.get_organization()
        context['domain'] = get_current_site(self.request).domain
        context['sitename'] = settings.SITE_NAME
        return context


class ProjectMixin:
    def get_project(self):
        return get_object_or_404(
            Project,
            organization__slug=self.kwargs['organization'],
            slug=self.kwargs['project']
        )


class ProjectRoles(ProjectMixin):
    lookup_field = 'username'

    def get_perms_objects(self):
        return [self.get_project()]

    def get_queryset(self):
        self.prj = self.get_project()
        return self.prj.users.all()

    def get_serializer_context(self, *args, **kwargs):
        context = super(ProjectRoles, self).get_serializer_context(
            *args, **kwargs)
        context['project'] = self.get_project()

        return context


class ProjectQuerySetMixin:
    def get_queryset(self):
        if hasattr(self.request.user, 'organizations'):
            orgs = self.request.user.organizations.all()
            if len(orgs) > 0:
                return Project.objects.filter(
                    Q(access='public') | Q(organization__in=orgs)
                )
        return Project.objects.filter(access='public')


class ArchiveMixin:
    def archive(self, archived):
        self.object = self.get_object()
        self.object.archived = archived
        self.object.save()

        return redirect(self.get_success_url())
