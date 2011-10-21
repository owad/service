from django.contrib import admin
from product.models import Product, Comment

class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ('id', 'name', 'producent', 'serial', 'status', 'max_cost', 'warranty', 'user', 'client', 'created', 'updated')
    search_fields = ('id', 'name', 'producent', 'serial', 'status')
    list_filter = ('producent', 'user', 'client')
    ordering = ('-created', )
    date_hierarchy = 'created'
    list_display_links = ('id', 'name')
    actions_on_bottom = True

class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ('product', 'note', 'type', 'user', 'hardware', 'software', 'transport', 'created')
    search_fields = ('note', 'type')
    list_filter = ('product', 'user', 'type')
    date_hierarchy = 'created'
    ordering = ('-created', )
    list_display_links = ('product', 'note')
    actions_on_bottom = True

admin.site.register(Comment, CommentAdmin)
admin.site.register(Product, ProductAdmin)
