from django.contrib import admin
from product.models import Product, Comment, Courier


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ('id', 'name', 'producent', 'user', 'client', 'status', 'created', 'updated')
    search_fields = ('id', 'name', 'producent', 'serial', 'status')
    list_filter = ('user',)
    ordering = ('-created', )
    date_hierarchy = 'created'
    list_display_links = ('id', 'name')
    actions_on_bottom = True


class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ('id', 'product', 'note', 'type', 'user', 'created')
    search_fields = ('note', 'type')
    list_filter = ('user',)
    date_hierarchy = 'created'
    ordering = ('-created', )
    list_display_links = ('product', 'note')
    actions_on_bottom = True


class CourierAdmin(admin.ModelAdmin):
    model = Courier


admin.site.register(Comment, CommentAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Courier, CourierAdmin)
