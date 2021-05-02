from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponseRedirect , Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

#from .models import Topic, Entry
#from .forms import TopicForm, EntryForm
from .models import Info, Entry
from .forms import InfoForm, DataForm , EntryForm, DeleteForm
from .datav import graph

from datetime import datetime, timedelta
from .helper import checker, grapher, scatter_year_amount, scatter_month_amount, scatter_month_amount_color
import plotly

# Create your views here.

def check_data_owner(request, data):
    return request.user == data.owner


def get_time_diff(start, end):
    starter = 60*start.hour + start.minute
    ender = 60*end.hour + end.minute
    return ender - starter

def index(request):
    return render(request, 'DA/index.html')

# view all entries(regardless of main val)
@login_required
def entries(request):
    entries = Entry.objects.filter(owner=request.user).order_by('date_added')
    print(request.user)
    context = {'entries':entries}
    return render(request, 'DA/entries.html', context)

# View entry
@login_required
def entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    if not check_data_owner(request, entry):
        raise Http404
    data = entry.info_set.order_by('-date_added')
    times = []
    for c in entry.info_set.all():
        times.append(get_time_diff(c.start, c.end))
    context = {'entry': entry, 'data': data, 'times':times}
    return render(request, 'DA/entry.html', context)

# add a data point
@login_required
def add_data(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    if request.method != 'POST':
        form = InfoForm()
    else:
        #POST request submitted
        form = InfoForm(data=request.POST)
        if form.is_valid() and request.user == entry.owner:
            new_entry = form.save(commit=False)
            new_entry.entry = entry
            new_entry.save()
            print(request.POST['start'])
            return HttpResponseRedirect(reverse('DA:entry', args=[entry_id]))
    context = {'entry':entry,'form':form}
    return render(request, 'DA/new_data.html', context)

# add entry(main topic)
@login_required
def new_entry(request):
    if request.method != 'POST':
        form = EntryForm()
    else:
        #there is some data
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('DA:entries'))
    context = {'form': form}
    return render(request, 'DA/new_entry.html', context)

# Edit data point
@login_required
def edit_data(request, data_id):
    """edit entry"""
    data = Info.objects.get(id=data_id)
    entry = data.entry

    if request.method != 'POST':
        form = InfoForm(instance=data)
    else:
        form = InfoForm(instance=data, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('DA:entry', args=[entry.id]))
    context = {'data': data, 'entry': entry, 'form':form}
    return render(request, 'DA/edit_data.html', context)

# View data from past days
@login_required
def view_all_data(request):
    bob = ""
    if request.method!='POST':
        form = DataForm()
    else:
        form = DataForm(data=request.POST)
        if form.is_valid():
            days = []
            d = form.cleaned_data['days_view']
            bob = d
            elements = Info.objects.all().order_by('-date_added')
            for c in elements:
                if(c.entry.owner == request.user):
                    days.append((c.day, c.month, c.year, c.start, c.end, c.text, c.date_added, c.entry))

                #b = c.entry.owner
                #entries = Info.objects.filter(b=request.user)
                #for e in entries:
                #    days[e.day] = e.month
            print(d)
    context = {'form':form}
    if(len(bob)):
        if(bob =="day"):
            context['days'] = checker(days, 1)
        elif(bob =="year"):
            context['days'] = checker(days, 365)
        elif(bob=="week"):
            context['days'] = checker(days, 7)
        elif(bob=="all"):
            context['days'] = days
        else:
            context['days'] = []
    return render(request, 'DA/data.html', context)


@login_required
def delete_data(request, data_id):
    data = Info.objects.get(id=data_id)
    if request.method != 'POST':
        form = DeleteForm()
    else:
        #there is some data
        form = DeleteForm(data=request.POST)
        if form.is_valid():
            d = form.cleaned_data['del_choice']
            if(d == 'yes'):
                Info.objects.filter(id=data_id).delete()
            else:
                pass
            return HttpResponseRedirect(reverse('DA:entries'))
    context = {'data':data,'form': form}
    return render(request, 'DA/delete_data.html', context)

@login_required
def view_some_data(request, entry_id):
    bob = ""
    if request.method!='POST':
        form = DataForm()
    else:
        form = DataForm(data=request.POST)
        if form.is_valid():
            days = []
            d = form.cleaned_data['days_view']
            bob = d
            entry = Entry.objects.get(id=entry_id)
            data = entry.info_set.order_by('-date_added')
            for c in data:
                if(c.entry.owner == request.user):
                    days.append((c.day, c.month, c.year, c.start, c.end, c.text, c.date_added))

                #b = c.entry.owner
                #entries = Info.objects.filter(b=request.user)
                #for e in entries:
                #    days[e.day] = e.month
            print(d)
    context = {'form':form, 'e_id':entry_id}
    if(len(bob)):
        if(bob =="day"):
            context['days'] = checker(days, 1)
        elif(bob =="year"):
            context['days'] = checker(days, 365)
        elif(bob=="week"):
            context['days'] = checker(days, 7)
        elif(bob=="all"):
            context['days'] = days
        else:
            context['days'] = []
    return render(request, 'DA/entry_data.html', context)

@login_required
def graph(request, entry_id):
    bob = ""
    graph_div = plotly.offline.plot(grapher(), auto_open=False, output_type="div")
    entry = Entry.objects.get(id=entry_id)
    data = entry.info_set.order_by('-date_added')
    day_list, month_list, year_list, da = [] , [] , [] , []
    for c in data:
        if(c.entry.owner == request.user):
            day_list.append(c.day)
            month_list.append(c.month)
            year_list.append(c.year)
            da.append(c.date_added)
    year_graph_scatter = scatter_year_amount(year_list)
    scatter_ma= scatter_month_amount(month_list, day_list)
    scatter_mac = scatter_month_amount_color(month_list,day_list)

    context = {'eid':entry_id,'graph':year_graph_scatter,'graph2':scatter_ma, 'graph3':scatter_mac}
    return render(request, 'DA/graph.html', context)
