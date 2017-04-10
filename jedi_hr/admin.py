from django.contrib import admin

# Register your models here.
from jedi_hr.models import Jedi, Candidate, Planet, Quiz, Question


class QuizAdminInline(admin.TabularInline):
    model = Question


class QuizAdmin(admin.ModelAdmin):
    inlines = [QuizAdminInline]


admin.site.register(Jedi)
admin.site.register(Candidate)
admin.site.register(Planet)
admin.site.register(Quiz, QuizAdmin)
