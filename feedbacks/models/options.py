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
from feedbacks.models.questions import Question
from .sources import Source
from .sources import SourceType

class Option(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class OptionAdmin(ModelAdmin):
    list_display = ['id', 'display_option', 'display_question']

    @display(
        description="Option",
        # label={
        #     QuestionType.SELECT: "warning",
        #     QuestionType.TEXT: "success",
        # },
    )

    def display_option(self, instance: Option):
        if instance.text:
            return instance.text

        return None

    @display(
        description="Question",
        # label={
        #     QuestionType.SELECT: "warning",
        #     QuestionType.TEXT: "success",
        # },
    )

    def display_question(self, instance: Option):
        if instance.question:
            return instance.question

        return None
    
class SubOptionsInline(admin.TabularInline):
    # from feedbacks.models.Options import Options
    verbose_name = "Questions Radio Button Option"
    verbose_name_plural = "Questions Radio Button Options"
    model = Option
