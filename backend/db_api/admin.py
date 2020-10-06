# importing required libraries
from django.contrib import admin
from .models import Customer, BookCollection
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

# modifying the admin panel of Django
class CustomUserAdmin(UserAdmin):
	"""Define admin model for custom User model with no username field."""
	fieldsets = (
		(None, {'fields': ('email', 'password')}),
		(_('Personal info'), {'fields': ('firstname', 'country')}),
		(_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
										'groups', 'user_permissions')}),
		(_('Important dates'), {'fields': ('last_login', 'date_joined')}),
	)
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email', 'password1', 'password2'),
		}),
	)
	list_display = ('email', 'firstname', 'country')
	search_fields = ('email', 'firstname', 'country')
	ordering = ('email',)

# Register your models here.
admin.site.register(Customer, CustomUserAdmin)
admin.site.register(BookCollection)