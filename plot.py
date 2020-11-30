from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

import util

def plotDaily(
        filename    = None,
        US          = True,
        places      = util.TEST_STATES,
        cases       = True,
        day         = util.TEST_DATE,
        dark_mode   = True
    ):
    column = 'Province_State' if US else 'Country/Region'
    df = util.loadData(US=US, cases=cases).groupby(column).sum().reset_index()
    
    if dark_mode: plt.style.use('dark_background')

    colors = plt.cm.Reds(np.linspace(0.35, 0.65, len(places)))

    values = []
    for place in places:
        cumulative_data = df[df[column] == place]
        start_column = cumulative_data.columns.get_loc(util.START_DATE)
		# convert total counts to daily counts
        counts = cumulative_data.iloc[:, start_column:].diff(axis=1)
        values.append(int(counts[day]))

    plt.bar(places, values, color=colors)

    label = 'Cases' if cases else 'Deaths'
    plt.title(f'{label}, {day}')
    plt.ylabel(f'{label}')

    filename = filename if filename else f"{label}_{day.replace('/', '-')}.png"
    plt.savefig(filename)
    plt.close()

def plotCaseMap(
        filename    = None,
        US          = True,
        day         = util.TEST_DATE,
        dark_mode   = True
    ):
    df = util.loadData(US=US)
    dates = list(df.columns)
    column = 'Province_State' if US else 'Country/Region'
    df = df.groupby(column)[dates].agg('sum')

    df['Cases'] = df.diff(axis=1)[day]
    if US:
        df['State'] = [util.STATE_TO_ABBREV.get(x, None) for x in list(df.index)]
    else:
        df['Country'] = df.index

    global_scopes = ['world', 'europe', 'africa', 'asia', 'south america', 'north america']

    fig = px.choropleth(
        df,
        locations               = 'State'       if US else 'Country',
        locationmode            = 'USA-states'  if US else 'country names',
        scope                   = 'usa'         if US else global_scopes[0],
        color                   = 'Cases',
        hover_name              = 'State'       if US else 'Country',
        # projection              = 'miller',
        color_continuous_scale  = 'Peach',
        template                = 'plotly_dark' if dark_mode else None,
        title                   = f"{'US' if US else 'Global'} Daily Cases, {day}",
        width                   = 1000,
        # height                  = 500,
        range_color             = [0,3000]
        )

    if filename is None:
        filename = 'usa_chart.png' if US else 'global_chart.png'

    fig.update_layout(margin={'l': 0, 'r': 0, 't': 70, 'b': 20}, title={'font': {'size': 20}, 'x':0.5})
    fig.write_image(filename, engine='kaleido')

def plotTimeSeries(
        filename    = None,
        US          = True,
        places      = util.TEST_STATES,
        cases       = True,
        num_days    = 7,
        end_date    = None,
        dark_mode   = True
    ):
    column = 'Province_State' if US else 'Country/Region'
    df = util.loadData(US=US, cases=cases).groupby(column).sum().reset_index()

    if dark_mode: plt.style.use('dark_background')

    colors = plt.cm.Oranges(np.linspace(0.35, 0.65, len(places)))

    offset = getOffset(df, end_date) if end_date else 0

    x_values = None
    for index, place in enumerate(places):
        cumulative_data = df[df[column] == place]
        start_column = cumulative_data.columns.get_loc(util.START_DATE)
        # convert total counts to daily counts
        counts = cumulative_data.iloc[:, start_column:].diff(axis=1)
        x_values = list(counts.columns[-(num_days + offset):len(counts.columns) - offset])
        y_values = [int(counts[col]) for col in x_values]

        plt.plot(x_values, y_values, label=place, color=colors[index], linewidth=2)

    label = 'Cases' if cases else 'Deaths'
    plt.title(f'Daily {label}, Last {num_days} Days')
    # control the number of date tick marks
    skip = max(num_days // 5, 1)
    plt.xticks(x_values[::skip])
    plt.xlabel('Date')
    plt.ylabel(f'{label}')
    plt.legend()
    filename = filename if filename else f'{label}_last_{num_days}.png'
    plt.savefig(filename)
    plt.close()

def getOffset(df, end_date):
    end = datetime.strptime(end_date, '%m/%d/%y')
    last_column = datetime.strptime(df.columns[-1], '%m/%d/%y')
    return max(0, (last_column - end).days)

if __name__ == '__main__':
    yesterday = ((datetime.today() - timedelta(days=1))
        .strftime('%m/%d/%y')
        .replace('/0','/')
        .lstrip('0'))

    plotDaily()
    plotDaily(cases=False)
    plotDaily(US=False, places=util.TEST_COUNTRIES)

    plotCaseMap()
    plotCaseMap(US=False)

    plotTimeSeries(filename='state-line-chart-test.png')
    plotTimeSeries(filename='country-line-chart-test.png', US=False,
        places=['US', 'India', 'Brazil'], num_days=100)
