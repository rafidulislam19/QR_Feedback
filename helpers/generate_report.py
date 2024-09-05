import json
import pandas as pd
from django.core.management.base import BaseCommand
from feedbacks.models.customer_responses import CustomerResponses
from feedbacks.models.sources import Source
from django.conf import settings
import os
from datetime import datetime, timedelta
import pytz
from django.http import HttpResponse
# from log.models.job_logs import (JobLog, 
#                                  JOBLOG_BODY, 
#                                  ERROR, 
#                                  ERROR_MSG, 
#                                  COMPLETED, 
#                                  MAIL_SENT, 
#                                  FILE_UPLOADED,
#                                  EXECUTED_QUERY,
#                                  CREATED_EXCEL)
# from log.models.task_logs import TaskLog

def generate_report(start_date, end_date, source_type):
    REPORT_FOLDER = 'report'
    sources = Source.objects.all()
    # print(sources)
    # Create the report directory if it does not exist
    os.makedirs(os.path.join(settings.LOCAL_FOLDER, REPORT_FOLDER), exist_ok=True)
    customer_responses = []
    REPORT_PATH = os.path.join(settings.LOCAL_FOLDER, REPORT_FOLDER, f'customer_feedback_{source_type}_{datetime.now().strftime("%Y-%m-%d")}.xlsx')
    REPORT_NAME=f'customer_feedback_{source_type}_{datetime.now().strftime("%Y-%m-%d")}.xlsx'

    try:
        for source in sources:
            print(source)
            print(start_date+timedelta(days=-1), end_date+timedelta(days=1))

            queryset_responses = CustomerResponses.objects.filter(
                source=source,
                created__range = [start_date, end_date+timedelta(days=1)]
            )

            log = None

            print(queryset_responses)

            if queryset_responses.exists():
                # log = TaskLog(
                #     name=f'generate_feedback_report',
                #     task_id='001',
                #     jobs=responses.count()
                # )
                # log.save()
                
                # try:
                # joblog = JobLog(
                #     name=f'generate_feedback_report',
                #     task=log,
                # )
                # joblog.save()
                # joblog_description = JOBLOG_BODY.copy()

                for queryset_response in queryset_responses:
                    if queryset_response.source.source_type == source_type:
                        data = queryset_response.response
                        data['response_sent_time'] = queryset_response.created
                        print(data['response_sent_time'])
                        data['id'] = source.source_id              #changes for report column
                        data[f"{source_type.lower()}_name"] = source.source_name
                        data[f"{source_type.lower()}_location"] = source.source_address
                        customer_responses.append(data)
                

        print(f"customer_responses: {customer_responses}")
                
        df = pd.DataFrame(customer_responses)


        if not df.empty:
            # response=[]
            df['response_sent_time'] = df['response_sent_time'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
            # df.sort_values('id').reset_index(drop=True).to_excel(REPORT_PATH, index=True, index_label='SL')    #changes for report sort by atm id
            print(df)
            # print(f"EXCEL: ", excel_file)
            # excel_file.save(resp)
            df.sort_values('id').reset_index(drop=True)

        return df
    
    except Exception as E:
        # joblog_description[ERROR] = True
        # joblog_description[ERROR_MSG] = str(E)
        # joblog.description = json.dumps(joblog_description)
        # joblog.save()
        raise E
    