# using the COVID-19 data API from rapidapi.com
import json
import requests
import  visualization


def get_total():
    url = "https://covid-19-data.p.rapidapi.com/totals"

    headers = {
        'x-rapidapi-key': "79a3faf042msh5370fe793f1dfabp123310jsnc4b60e1d6d0a",  # pls don't get me banned
        'x-rapidapi-host': "covid-19-data.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers)
    data = json.loads(response.text[1:-1])
    print("The number of confirmed cases: {}.\nThe number of recovered: {}.\nThe number of critical: {}.\nThe mumber "
          "of deaths: {}.\nLast updated: {}.\n".format(data['confirmed'], data['recovered'], data['critical'],
                                                       data['deaths'], data['lastUpdate']))

    visualization.visualize("World Data", ('Sick', 'Dead', 'Recovered'), [data['confirmed'], data['deaths'], data['recovered']], ['red', 'grey', 'green'], (0, 0, 0))


def get_latest_country_data_by_code(countrycode):
    #region countrydata
    url = "https://covid-19-data.p.rapidapi.com/country/code"

    querystring = {"code": countrycode}

    headers = {
        'x-rapidapi-key': "79a3faf042msh5370fe793f1dfabp123310jsnc4b60e1d6d0a",
        'x-rapidapi-host': "covid-19-data.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    data = json.loads(response.text[1:-1])
    print("The name of the country: {}\nThe number of confirmed cases: {}.\nThe number of recovered: {}.\nThe number "
          "of critical: {}.\nThe mumber "
          "of deaths: {}.\nLast updated: {}.\n".format(data['country'], data['confirmed'], data['recovered'], data['critical'],
                                                       data['deaths'], data['lastUpdate']))
    #endregion



    #region visualizations
    visualization.visualize(data['country'], ('Sick', 'Dead', 'Recovered'), [data['confirmed'], data['deaths'], data['recovered']], ['red', 'grey', 'green'], (0, 0, 0))
    #visualization.visualize('{} and the world'.format(data['country']), data['confirmed'])
    #endregion

