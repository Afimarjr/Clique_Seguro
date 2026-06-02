from django.contrib import admin
from .models import Categoria, Tutorial, Passo, Progresso

# Permite gerir os passos diretamente dentro da página do Tutorial (super prático!)
class PassoInline(admin.TabularInline):
    model = Passo
    extra = 1

class TutorialAdmin(admin.ModelAdmin):
    list_display = ('title', 'categoria', 'id')
    list_filter = ('categoria',)
    inlines = [PassoInline]

admin.site.register(Categoria)
admin.site.register(Tutorial, TutorialAdmin)
admin.site.register(Passo)
admin.site.register(Progresso)