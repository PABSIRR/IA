from datetime import datetime, timedelta
import plotly
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
def checker(lister, days):
    present = datetime.now()
    bob = []
    for c in lister:
        date_obj = datetime(c[2], c[1], c[0])
        if(abs((present-date_obj).days) < days):
            bob.append(c)
    
    return bob

def grapher():
    fig = go.Figure(
        data = [go.Bar(y=[2,1,3])],
        layout_title_text="A figure displayed"
    )
    return fig

def scatter_year_amount(year_list):
    coc  = []
    bob = {}
    for year in year_list:
        if year in bob:
            bob[year] += 1
        else:
            bob[year] = 1
    for year,amount in bob.items():
        coc.append([year, amount])
    df = pd.DataFrame(coc, columns=['year', 'amount'])
    print(df)
    fig = px.bar(df, x='year', y='amount')

    return fig.to_html(full_html=False)

def scatter_month_amount(month_list, daY_list):
    """
    coc  = []
    bob = {}
    for month in month_list:
        if month in bob:
            bob[month] += []
        else:
            bob[year] = 1
    for year,amount in bob.items():
        coc.append([year, amount])
    """
    coc = []
    for c in range(len(month_list)):
        bob = [month_list[c], daY_list[c], 1]
        if bob in coc:
            t = coc.index(bob)
            coc[t][2] += 1
        else:
            coc.append([month_list[c],daY_list[c],1])
    df = pd.DataFrame(coc, columns=['month', 'day', 'amount'])
    print(df)
    fig = px.scatter(df, x='month', y='day', size='amount')

    return fig.to_html(full_html=False)

def scatter_month_amount_color(month_list, daY_list):
    """
    coc  = []
    bob = {}
    for month in month_list:
        if month in bob:
            bob[month] += []
        else:
            bob[year] = 1
    for year,amount in bob.items():
        coc.append([year, amount])
    """
    coc = []
    for c in range(len(month_list)):
        bob = [month_list[c], daY_list[c], 1]
        if bob in coc:
            t = coc.index(bob)
            coc[t][2] += 1
        else:
            coc.append([month_list[c],daY_list[c],1])
    df = pd.DataFrame(coc, columns=['month', 'day', 'amount'])
    print(df)
    fig = px.scatter(df, x='month', y='day', color='amount')

    return fig.to_html(full_html=False)