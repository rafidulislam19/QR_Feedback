from django.urls import path
from django.utils.html import format_html
from django.shortcuts import render
from django.db import models
import pandas as pd
# from .generate_report import generate_report
# from .models import DataUpload
from access_management.models import User
from unfold.decorators import display
from unfold.decorators import action
from .sources import SourceType
from unfold.admin import ModelAdmin
from core import settings
from django.core.exceptions import ValidationError
from helpers.generate_report import generate_report
from django.http import HttpResponse
from django.contrib import messages

class SourceType(models.TextChoices):
    ATM = "ATM", "ATM"
    BRANCH = "BRANCH", "Branch"

class ReportDownload(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, 
                             null=True, editable=False)
    source_type = models.CharField(choices=SourceType.choices, max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError('End Date cannot be earlier than Start Date!')
        if (self.end_date - self.start_date).days > 30:
            raise ValidationError('Date range cannot exceed 30 days!')


class ReportDownloadAdmin(ModelAdmin):
    list_display = ['display_username', 'show_source_type', 'display_start_date', 'display_end_date', 'created']

    @display(
        description="Username",
        # label={
        #     QuestionType.SELECT: "warning",
        #     QuestionType.TEXT: "success",
        # },
    )
    def display_username(self, instance: User):
        if instance.user:
            return instance.user

        return None
    
    @display(
        description="Source Type"
        # label=True
    )
    def show_source_type(self, obj):
        return obj.source_type

    @display(
        description="Start Date"
        # label=True
    )
    def display_start_date(self, obj):
        return obj.start_date
    
    @display(
        description="End Date"
        # label=True
    )
    def display_end_date(self, obj):
        return obj.end_date
    
    @display(
        description="Created at"
        # label=True
    )
    def created(self, obj):
        return obj.created
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        # print(obj.start_date)
        # print(obj.end_date)
        super().save_model(request, obj, form, change)
        self.obj = obj

    def generate_excel_report(self, obj):
        df = generate_report(obj.start_date, obj.end_date, str(obj.source_type))
        if df.empty:
            return None
        else:
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename="{obj.source_type}_customer_response_report_{obj.start_date}_to_{obj.end_date}.xlsx"'
  
            with pd.ExcelWriter(response, engine='openpyxl') as writer:
                df.to_excel(writer, index=True, index_label='SL')
            
            return response
        
    def response_add(self, request, obj, post_url_continue=None):
        excel_response = self.generate_excel_report(obj)
        if excel_response is None:
            messages.error(request, "No customer responses found for the selected date range.")
            return super().response_add(request, obj, post_url_continue)
        return excel_response
    
    def response_change(self, request, obj):
        excel_response = self.generate_excel_report(obj)
        if excel_response is None:
            messages.error(request, "No customer responses found for the selected date range.")
            return super().response_change(request, obj)
        return excel_response
