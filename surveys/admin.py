from django.contrib import admin
from .models import Survey, Question, Option, Answer

# Registrar los modelos para que aparezcan en el admin de Django
admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Answer)
