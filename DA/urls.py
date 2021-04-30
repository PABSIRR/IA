from django.urls import path

from . import views

app_name = 'DA'

urlpatterns=[
    #Home Page
    path('', views.index, name='index'),

    #View all Entries
    path('entries/', views.entries, name='entries'),

    #New entry(data)
    path('new_data/<int:entry_id>', views.add_data, name='new_data'),

    #View data
    path('data/', views.view_all_data, name='data'),

    #Individual Entry
    path('entries/<int:entry_id>/', views.entry,name="entry"),

    #New Topic
    path('new_entry/', views.new_entry, name="new_entry"),

    #Edit Entry
    path('edit_data/<int:data_id>', views.edit_data, name='edit_data'),

    #Delete data
    path('delete_data/<int:data_id>', views.delete_data, name='delete_data'),

    #View unique post data
    path('entries/<int:entry_id>/data', views.view_some_data, name="entry_data"),

    #View graphs??? One for now
    path('entries/<int:entry_id>/graph', views.graph, name="graph"),
]