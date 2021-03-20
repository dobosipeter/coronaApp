# using the free tier of Gramzivi's COVID-19 data API from rapidapi.com
import json
import time
from datetime import timedelta, datetime
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


def get_last_seven_days_by_country_code_and_week(country_code, target_day):
    """ Get information about the given week of a country, plot the data. """
    # Add the first day to the week
    week = [target_day]
    weekly_data = []
    # Get the previous six days.
    for i in range(1, 7):
        week.append((datetime.strptime(target_day, "%Y-%m-%d") - timedelta(days=i)).strftime("%Y-%m-%d"))

    # Get the data for the week.
    print("Getting data for the seven days, this will take a couple of seconds.")

    for day in week:
        print("Currently getting data for {}".format(day))
        weekly_data.append(get_daily_data_by_country_code(day, country_code))
        # still have to wait for the api
        time.sleep(2)

    # The dates of the data
    dates = get_data_from_dict(weekly_data, "date")
    cut_dates = []
    for i in range(len(dates)):
        cut_dates.append(dates[i][5:])

    dates.reverse()
    cut_dates.reverse()
    # The list of provinces from the timeframe
    provinces = get_data_from_dict(weekly_data, "provinces")
    # The list of actual provinces, in the previous one they were in a list each.
    act_prov = []
    for province in provinces:
        act_prov.append(province[0])

    # The list of confirmed cases in the given timeframe.
    confirmed = get_data_from_dict(act_prov, "confirmed")
    confirmed.reverse()

    # Visualize the data
    visualization.plot(cut_dates, confirmed)
    visualization.show()

    # plotting goes here (probably outside this loop)
    # ideas to plot:
    # number of confirmed cases, deaths, recovery, country vs the world, maybe percentages?
    # dont forget that the response data contains the day it was requested for!
    # maybe define a method for building the data you need to plot?
    # datas = getstuff(parameter): for data in weekly_data return data[parameter]
    # idk how to use plot yet, but probably something like plot(datas, week)


def get_data_from_dict(list_of_dicts, parameter):
    """ Return a list of the given parameters from a given list of dictionaries """
    ret_list = []
    for item in list_of_dicts:
        ret_list.append(item[parameter])

    return ret_list
