from django.contrib import admin

from djangoNobel.models import SportStructure, SportStructureImage, Tag, Category, Rating, Comment

# Register your models here.
admin.site.register(SportStructure)
admin.site.register(SportStructureImage)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Rating)
admin.site.register(Comment)

