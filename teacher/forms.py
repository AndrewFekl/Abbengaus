from django import forms

class TranslateForm2(forms.Form):
    original_word = forms.CharField(label='Слово на английском', max_length=100)
    translated_word = forms.CharField(label='Перевод слова', max_length=100)

class TranslateForm1(forms.Form):
    original_word = forms.CharField(label='Слово на английском', max_length=100)

class TrainingForm(forms.Form):
    """def __init__(self, choices, *args, **kwargs):
        self.choices = kwargs.pop('choices')
        super(TrainingForm, self).__init__(*args, **kwargs)
        self.fields['answer'].widget = forms.ChoiceField(attrs={'choices': choices})
    answer = forms.ChoiceField()"""

    def __init__(self, round_list, *args, **kwargs):
        super(TrainingForm, self).__init__(*args, **kwargs)
        self.fields['Ответ'] = forms.ChoiceField(choices=tuple([(name, name) for name in round_list]), widget=forms.RadioSelect)



