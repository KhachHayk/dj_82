from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Scoping, Topic


class ScopingInlineFormset(BaseInlineFormSet):
    def clean(self):
        count_topic = 0
        for form in self.forms:
            if form.cleaned_data.get('main'):
                count_topic += 1
            else:
                continue
        if count_topic == 0:
            raise ValidationError('Выберите основной раздел')
        elif count_topic > 1:
            raise ValidationError('Основной раздел уже выбран')

        return super().clean()


class ScopingInline(admin.TabularInline):
    model = Scoping
    formset = ScopingInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopingInline]


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    pass