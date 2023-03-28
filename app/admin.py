from django.contrib import admin

from app.models import Choices, Question

class ChoiceInlince(admin.StackedInline):
    model=Choices
    extra=3
class QuestionAdmin(admin.ModelAdmin):
    fields=['pub_date','question_text']
    inlines=[ChoiceInlince]
    list_display=(
        "question_text",
        "pub_date",
        "was_published_recently"
    )
    list_filter=[
        'pub_date'
    ]
    search_fields=['question_text']
# Register your models here.
admin.site.register(Choices)
admin.site.register(Question,QuestionAdmin)