from django.contrib import admin
from project.models import Project

class ProjectAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "title",)
    prepopulated_fields = {"project_slug": ("title",)}  # new

admin.site.register(Project, ProjectAdmin)