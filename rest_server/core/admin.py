from django.contrib import admin
from .models import OneWordAnswerType, OneWordAnswerAnswer
from .models import SingleChoiceQuestion, SingleChoiceOptions, SingleChoiceAnswer
from .models import MultiChoiceQuestion, MultiChoiceOptions, MultiChoiceAnswers
# Register your models here.


admin.site.register(OneWordAnswerType)
admin.site.register(OneWordAnswerAnswer)
admin.site.register(SingleChoiceQuestion)
admin.site.register(SingleChoiceOptions)
admin.site.register(SingleChoiceAnswer)
admin.site.register(MultiChoiceQuestion)
admin.site.register(MultiChoiceOptions)
admin.site.register(MultiChoiceAnswers)
