# using the free tier of Gramzivi's COVID-19 data API from rapidapi.com
import json
import time
from datetime import date, timedelta
import requests
import visualization


def get_total(flag=False):
    """ Print the current total worldwide data and draw the relevant charts. If flag is set, just return the data for
    usage in another method. """
    # region api_usage
    # This region sets up the information necessary to communicate with the api.
    url = "https://covid-19-data.p.rapidapi.com/totals"

    headers = {
        'x-rapidapi-key': "79a3faf042msh5370fe793f1dfabp123310jsnc4b60e1d6d0a",  # pls don't get me banned
        'x-rapidapi-host': "covid-19-data.p.rapidapi.com"
    }

    # Send the request and save the result.
    response = requests.request("GET", url, headers=headers)
    # endregion
    # Convert the json response into a dictionary we can use.
    data = json.loads(response.text[1:-1])

    # region flag_logic
    # If the flag is set, this method is invoked inside another one to get the worlddata,
    # to be used in another piechart. In this case there is no need to print or draw anything.
    if flag:
        return data
    # If the flag is not set, the method is invoked regularly.
    # Thus we need to print the formatted data and draw the chart.
    else:
        print("The number of confirmed cases: {}.\nThe number of recovered: {}.\nThe number of critical: {}.\nThe "
              "mumber "
              "of deaths: {}.\nLast updated: {}.\n".format(data['confirmed'], data['recovered'], data['critical'],
                                                           data['deaths'], data['lastUpdate']))

        # region visualization
        # Draw the chart with the given data.
        visualization.pie_visualize("World Data", ('Sick', 'Dead', 'Recovered'),
                                    [data['confirmed'], data['deaths'], data['recovered']], ['red', 'grey', 'green'],
                                    (0, 0, 0))
        # endregion
    # endregion


def get_latest_country_data_by_code(countrycode):
    """ Print the latest country data for a given country and draw the relevant charts. """
    # region api_usage
    # This region sets up the information necessary to communicate with the api.
    url = "https://covid-19-data.p.rapidapi.com/country/code"

    querystring = {"code": countrycode}

    headers = {
        'x-rapidapi-key': "79a3faf042msh5370fe793f1dfabp123310jsnc4b60e1d6d0a",
        'x-rapidapi-host': "covid-19-data.p.rapidapi.com"
    }

    # Send the request and save the result.
    response = requests.request("GET", url, headers=headers, params=querystring)
    # endregion

    # Convert the json response into a dictionary we can use.
    if len(response.text) == 2:
        raise Exception("Illegal country code")
    data = json.loads(response.text[1:-1])
    # Print the countrydata.
    print("The name of the country: {}\nThe number of confirmed cases: {}.\nThe number of recovered: {}.\nThe number "
          "of critical: {}.\nThe mumber "
          "of deaths: {}.\nLast updated: {}.\n".format(data['country'], data['confirmed'], data['recovered'],
                                                       data['critical'],
                                                       data['deaths'], data['lastUpdate']))

    # region worlddata
    # We need to get the world data, in order to display it on the diagrams below. On the free tier
    # of the api, I can only make one request per second. Because of that I have to wait a bit, before this request
    # is sent, otherwise I'll get back a 429. Waiting one second should be enough, but sometimes it isn't so we wait
    # for two seconds.
    time.sleep(2)
    # Get the worlddata.
    world_data = get_total(True)
    # endregion

    # region visualizations
    # Draw the charts with the given data.
    visualization.pie_visualize(data['country'], ('Sick', 'Dead', 'Recovered'),
                                [data['confirmed'], data['deaths'], data['recovered']], ['red', 'grey', 'green'],
                                (0, 0, 0))
    visualization.pie_visualize('{} and the world'.format(data['country']), (data['country'], 'Rest of the World'),
                                [data['confirmed'] + data['critical'],
                                 world_data['confirmed'] + world_data['critical']],
                                ['blue', 'orange'], (0.1, 0))
    # endregion


def get_daily_data_by_country_code(day, country_code):
    """ Get the daily report for a given country. """
    url = "https://covid-19-data.p.rapidapi.com/report/country/code"

    querystring = {"date": day, "code": country_code}

    headers = {
        'x-rapidapi-key': "79a3faf042msh5370fe793f1dfabp123310jsnc4b60e1d6d0a",
        'x-rapidapi-host': "covid-19-data.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response.text[1:-1])

    return data


def get_last_seven_days_by_country_code(country_code):
    """ Get information about the last seven days of a country, plot the data. """
    today = date.today()
    week = [today.strftime("%Y-%m-%d")]
    weekly_data = []
    for i in range(1, 7):
        week.append((today - timedelta(days=i)).strftime("%Y-%m-%d"))
    
    for day in week:
        print("Getting data for the last seven days, this will take a couple of seconds.")
        print("Currently getting data for {}".format(day))
        weekly_data.append(get_daily_data_by_country_code(day, country_code))
        # still have to wait for the api
        time.sleep(2)

        # plotting goes here (probably outside this loop)
        # ideas to plot:
        # number of confirmed cases, deaths, recovery, country vs the world, maybe percentages?
        # dont forget that the response data contains the day it was requested for!
        # maybe define a method for building the data you need to plot?
        # datas = getstuff(parameter): for data in weekly_data return data[parameter]
        # idk how to use plot yet, but probably something like plot(datas, week)
    
    today_string = today.strftime("%Y-%m-%d")
