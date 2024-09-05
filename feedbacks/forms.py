from django.forms import ModelForm
from feedbacks.models.customer_responses import CustomerResponses
from django import forms
from feedbacks.models.questions import Question
from feedbacks.models.options import Option


class CustomerResponseForm(ModelForm):
    class Meta:
        model = CustomerResponses
        exclude = ['created', 'updated']


class QuestionForm(forms.Form):
    # class Meta:
    #     model = Question
    #     exclude = ['created', 'updated']
    def __init__(self, source_type, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        questions = Question.objects.filter(source_type=source_type)
        for question in questions:
            if question.question_type == 'Radio':
                options = question.options.all()
                choices = [(option.id, option.text) for option in options]
                self.fields[f'question_{question.id}'] = forms.ChoiceField(
                    label=question.text,
                    choices=choices,
                    widget=forms.RadioSelect(attrs={'class': 'radio-option'}),
                    required=True,
                    help_text = question.report_column_name
                )
                print(f"CHOICES: ", choices)
                print(f"FIELDS: ", self.fields)
            elif question.question_type == 'Scoring':
                max_score = question.max_score or 10
                choices = [(score, str(score)) for score in range(max_score + 1)]
                self.fields[f'question_{question.id}'] = forms.ChoiceField(
                    label=question.text,
                    choices=choices,
                    widget=forms.RadioSelect(attrs={'class': 'scoring-option'}),
                    required=True,
                    help_text = question.report_column_name
                )
                print(f"CHOICES: ", choices)
                print(f"FIELDS: ", self.fields)
