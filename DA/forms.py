from django import forms

from . models import Info, Entry

class InfoForm(forms.ModelForm):
    start = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    end = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    class Meta:
        model = Info
        fields = ['text', 'month','day', 'year','start', 'end']
        labels = {'text':'Thoughts on the event', 'month':'Enter month','day':'Enter in day','year':'Enter year','start':'Starting time(in military time)', 'end':'Ending time(in military time)'}
        widgets = {'text': forms.Textarea(attrs={'cols':80})}


Day_Choices = [
    ('day','Day'),
    ('week','Week'),
    ('year','Year'),
    ('all','All'),
]
class DataForm(forms.Form):
    days_view = forms.CharField(label='How many days of data to view?', widget=forms.Select(choices=Day_Choices))

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text':''}   

Delete_Choices = [
    ('yes','yes'),
    ('no','no')
]
class DeleteForm(forms.Form):
    del_choice = forms.ChoiceField(choices=Delete_Choices, widget=forms.RadioSelect)

all_objects = Info.objects.all()
years = []
for obj in all_objects:
    years.append(obj.year)
Year_Choices = [(year, year) for year in years]
Year_Choices_FR = list(set(Year_Choices))

class YearForm(forms.Form):
    year_view = forms.CharField(label='How many days of data to view?', widget = forms.Select(choices=Year_Choices_FR))