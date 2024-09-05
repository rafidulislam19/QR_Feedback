from django.shortcuts import render
# from datetime import date, timedelta
# from django import forms
# from datetime import datetime
# from django.conf import settings
# from django.http import HttpResponse
from feedbacks.forms import CustomerResponseForm
from feedbacks.models.sources import Source
import json
from feedbacks.forms import QuestionForm
from django.shortcuts import render
# from feedbacks.models.questions import Question
# from django.contrib.admin.views.decorators import staff_member_required
# from feedbacks.models.report_download import ReportDownload
# from feedbacks.report_form import ReportDownloadForm
# from feedbacks.management.commands import generate_report
import os



def feedback_request_handler(request, uuid):

    source_data = Source.objects.filter(id=uuid)

    if len(source_data) > 0:
        source_data = source_data[0]
        context = {
            'name': source_data.source_name,
            'id': source_data.id
        }

        # Check the source_type and load the appropriate template
        if source_data.source_type == 'ATM' or 'Branch':
            template_name = 'customer_response_atm.html'

        else:
            # Handle the case where source_type is neither ATM nor Branch
            return render(
                request=request, 
                template_name='error.html', 
                context={
                    'page_title': 'Error',
                    'h3': 'Invalid Source Type',
                    'p': f'The source type "{source_data.source_type}" is not recognized.'
                }
            )

        # print(request.method)

        form = QuestionForm(source_data.source_type)

        if request.method == 'POST':
            # print("POST Request")
            data = json.dumps(request.POST)
            data = json.loads(data)
            
            response = data.copy()
            del response['csrfmiddlewaretoken'] 
            del response['source']
            data['response'] = response

            print(data)

            form = CustomerResponseForm(data)

            if form.is_valid():
                form.save()
                context['page_title'] = 'Service Fulfillment Confirmation'
                # context['form'] = form
                return render(request, 'submitted.html', context=context)
            else:
                print(form.errors)

        context['page_title'] = 'Service Fulfillment Survey'
        context['form'] = form
        return render(request=request, template_name=template_name, context=context)

        
    
    return render(
        request=request, 
        template_name='error.html', 
        context={
            'page_title': 'Resource not found', 
            'h3': 'Resource Not Found!',
            'p': f'Requested - {uuid}'
        }
    )


def http_403_custom(request, *args, **argv):
    return render(
        request=request,
        template_name='error.html',
        context={
            'page_title': '403 Forbidden',
            'h3': '403 Forbidden!',
            'p': 'You do not have permission to access this page. Please contact the administrator if you believe this is an error.'
        }
    )


def http_404_custom(request, *args, **argv):
    return render(
        request=request, 
        template_name='error.html', 
        context={
            'page_title': '404 Not Found',
            'h3': '404 Page Not Found!',
            'p': request.build_absolute_uri ()
        }
    ) 


def http_500_custom(request, *args, **argv):
        return render(
        request=request, 
        template_name='error.html', 
        context={
            'page_title': '500 Internal Server Error',
            'h3': '500 Internal Server Error!',
            'p': request.build_absolute_uri ()
        }
    )



# @staff_member_required
# def download_report_view(request):
#     if request.method == "POST":
#         form = ReportDownloadForm(request.POST)
#         if form.is_valid():
#             report_request = form.save(commit=False)
#             report_request.user = request.user
#             report_request.save()

#             report_path, report_name = generate_report(
#                 start_date=report_request.start_date,
#                 end_date=report_request.end_date,
#                 source_type=report_request.source_type
#             )

#             with open(report_path, 'rb') as f:
#                 response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#                 response['Content-Disposition'] = f'attachment; filename={report_name}'
#                 return response
#     else:
#         form = ReportDownloadForm()

#     return render(request, 'download_report.html', {'form': form})

