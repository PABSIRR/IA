from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
# Create your models here.


class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value':self.min_value, 'max_value':self.max_value}
        defaults.update(**kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


def default_start_time():
    now = datetime.now()
    start = now.replace(hour=22, minute=0, second=0, microsecond=0)
    return start if start > now else start + timedelta(days=1)

class Entry(models.Model):
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

class Info(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.DO_NOTHING)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    start = models.TimeField(blank=True, default=default_start_time)
    end = models.TimeField(blank=True, default=default_start_time)
    day = IntegerRangeField(min_value=0, max_value=31)
    month = IntegerRangeField(min_value=0,max_value=12)
    year = models.IntegerField()
    
    class Meta:
        verbose_name_plural = 'data'

    def __str__(self):
        return self.text

