from django.shortcuts import render,render_to_response,redirect
from django.contrib import admin
from django.forms import ModelForm
from django.utils.html import format_html
from django.utils import timezone

from providers.models import Provider,Category,Content,Package,Item
from consumers.models import Consumer,Consumer_profile
from .tasks import send_email



class ItemsInline(admin.TabularInline):
    model = Item

    def get_queryset(self, request):
        """Limit Pages to those that belong to the request's user."""
        qs = super(ItemsInline, self).get_queryset(request)
        packs = []
        for q in qs:
            if request.user == q.package.provider:
                packs.append(q.package)
        if request.user.is_superuser:
            # It is mine, all mine. Just return everything.
            return qs
        # Now we just add an extra filter on the queryset and
        # we're done. Assumption: Page.owner is a foreignkey
        # to a User.
        return qs.filter(package__in=packs)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):

        field = super(ItemsInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'item':
            if request.user.is_superuser:
                field.queryset = field.queryset.all()
            else:
                field.queryset = field.queryset.filter(provider__exact = request.user)
        return field


class PackageAdmin(admin.ModelAdmin):
    list_display = ('package_name','location','business_type','scheduled_date','status')
    readonly_fields = ('status',)
    inlines = [ItemsInline,]
    search_fields = ('package_name','provider__category__category')
    actions = ['make_published']

    def make_published(self, request, queryset):
        form = None
        now = timezone.now()
        to = ['lakshmineelima04@gmail.com',]

        for package in queryset:
            if package.status == 'p':
                print "already published"
            else:
                # return render_to_response('admin/payment.html')
                categories = Package.category(package)
                profiles = Consumer_profile.objects.filter(category__in=categories)

                # consumer = Consumer_profile.get_consumers(profiles)
                # print users
                # print "******"*8
                if (package.scheduled_date > now):
                    send_email.apply_async(args=[to,package,profiles],eta=package.scheduled_date)
                else:
                    send_email.apply_async(args=[to,package,profiles],eta=timezone.now())
        queryset.update(status='b')
    make_published.short_description = "To be published selected packages"
    make_published.allow_tags = True

    def get_queryset(self, request):
        """Limit Pages to those that belong to the request's user."""
        qs = super(PackageAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            # It is mine, all mine. Just return everything.
            return qs
        # Now we just add an extra filter on the queryset and
        # we're done. Assumption: Page.owner is a foreignkey
        # to a User.
        return qs.filter(provider=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        field = super(PackageAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        user = request.user
        if db_field.name == 'provider':
            kwargs['initial'] = request.user.id
        return super(PackageAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

class ContentAdmin(admin.ModelAdmin):
    list_display = ('category','image','video','created','updated')
    search_fields = ('category__category',)


    readonly_fields = ('image_preview','video_preview')

    def image_preview(self, obj):
        image = getattr(obj, 'image', '')
        return format_html(u'<img src="{}" />', image.url)

    def video_preview(self, obj):
        video = getattr(obj, 'video', '')
        return format_html(u"<video width='250' height='240' controls><source src='{}' type='video/mp4'></video>", video.url)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'provider':
            kwargs['initial'] = request.user.id
        return super(ContentAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

    def get_queryset(self, request):
        """Limit Pages to those that belong to the request's user."""
        qs = super(ContentAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            # It is mine, all mine. Just return everything.
            return qs
        # Now we just add an extra filter on the queryset and
        # we're done. Assumption: Page.owner is a foreignkey
        # to a User.
        return qs.filter(provider=request.user)


class ProviderAdmin(admin.ModelAdmin):
    fields = ('user', 'name', 'created', 'updated')

admin.site.register(Provider)
admin.site.register(Content,ContentAdmin)
admin.site.register(Package,PackageAdmin)
admin.site.register(Category)

