from django.contrib import admin

from person.models import Client

#class UserAdmin(admin.ModelAdmin):
#    model = User

class ClientAdmin(admin.ModelAdmin):
    model = Client
    list_display = ('id', 'first_name', 'last_name', 'company_name', 'city', 'email', 'phone_number')
    search_fields = ('first_name', 'last_name', 'company_name', 'city', 'email', 'phone_number')
    list_filter = ('company_name', 'city', 'postcode')
    date_hierarchy = 'created'
    list_display_links = ('id', 'first_name', 'last_name', 'company_name')
    
    actions_on_bottom = True

admin.site.register(Client, ClientAdmin)
