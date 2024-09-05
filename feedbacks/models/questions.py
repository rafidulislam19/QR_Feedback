# from uuid import uuid4
# from django import forms
# from django.db import models
# from datetime import datetime
# from django.utils import timezone
# from django.forms import Form, ValidationError
# from django.http import HttpRequest
# from django.contrib import admin
# from unfold.admin import ModelAdmin
# from unfold.decorators import display
# from unfold.decorators import action
# from .sources import Source

# class QuestionType(models.TextChoices):
#     SELECT = "SELECT", "Yes / NO Mark"
#     TEXT = "TEXT", "Text Field"

# class Question(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
#     question = models.CharField(max_length=255, blank=False, null=False)
#     type = models.CharField(choices=QuestionType, max_length=50, blank=False, null=False) # type: ignore
#     source = models.ForeignKey(Source, on_delete=models.CASCADE)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
    
# class QuestionType(models.TextChoices):
#     SELECT = "SELECT", "Yes / NO Mark"
#     TEXT = "TEXT", "Text Field"

# class QuestionAdmin(ModelAdmin):
#     list_display = ['id', 'display_question_type', 'show_source_name', 'created']

#     @display(
#         description="Question Type",
#         label={
#             QuestionType.SELECT: "warning",
#             QuestionType.TEXT: "success",
#         },
#     )
#     def display_question_type(self, instance: Question):
#         if instance.type:
#             return instance.type

#         return None
    
#     @display(
#         description="Source", label=True
#     )
#     def show_source_name(self, obj):
#         return obj.source.source_name
from uuid import uuid4
from django import forms
from django.db import models
from datetime import datetime
from django.utils import timezone
from django.forms import Form, ValidationError
from django.http import HttpRequest
from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.decorators import display
from unfold.decorators import action
from .sources import Source
from .sources import SourceType
# from .options import Option, OptionAdmin

# class QuestionType(models.TextChoices):
#     SELECT = "SELECT", "Yes / NO Mark"
#     TEXT = "TEXT", "Text Field"

# class Question(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
#     question = models.CharField(max_length=255, blank=False, null=False)
#     type = models.CharField(choices=QuestionType.choices, max_length=50, blank=False, null=False)
#     source = models.ForeignKey(Source, on_delete=models.CASCADE)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)


class Question(models.Model):

    QuestionType = [
        ('Radio', 'Radio Buttons'),
        ('Scoring', 'Scoring')
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    text = models.CharField(max_length=255, blank=False, null=False)
    question_type = models.CharField(max_length=10, choices=QuestionType, default='radio')
    max_score = models.PositiveIntegerField(null=True, blank=True, help_text="Max score for scoring questions.")
    source_type = models.CharField(choices=SourceType.choices, max_length=50, blank=False, null=False,  default='ATM')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    report_column_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.text


    
class QuestionAdmin(ModelAdmin):
    list_display = ['id', 'display_question_type', 'show_source_type', 'created']

    @display(
        description="Question Type",
        # label={
        #     QuestionType.SELECT: "warning",
        #     QuestionType.TEXT: "success",
        # },
    )
    def display_question_type(self, instance: Question):
        if instance.question_type:
            return instance.question_type

        return None
    
    @display(
        description="Source Type"
        # label=True
    )
    def show_source_type(self, obj):
        return obj.source_type



        


