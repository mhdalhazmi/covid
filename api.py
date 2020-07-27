import requests
import pandas as pd
import time



def daily_report_countries(country_code='sa'):
    url = "https://covid-19-data.p.rapidapi.com/country/code"

    querystring = {"format":"json","code":country_code}

    headers = {
        'x-rapidapi-host': "covid-19-data.p.rapidapi.com",
        'x-rapidapi-key': "46345e418cmsh542642b3ab38d2fp12ab20jsne42343ea4346"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.json()

def get_daily_report_countries(df_final):
    for index,row in df_countries_info[0:25].iterrows():
        country_code = row["alpha2code"]
        longitude = row["longitude"]
        latitude = row["latitude"]
        if country_code:
            df_daily_cases = daily_report_countries(country_code)
            #print(df_daily_cases)
            #input()
            if "country" in df_daily_cases[0].keys():
                country = df_daily_cases[0]["country"]
            else:
                country = "none"
            print(country)
            if "confirmed" in df_daily_cases[0].keys():
                confirmed = df_daily_cases[0]["confirmed"]
            else:
                confirmed = 0

            if "recovered" in df_daily_cases[0].keys():
                recovered = df_daily_cases[0]["recovered"]
            else:
                recovered = 0

            if "lastUpdate" in df_daily_cases[0].keys():
                update = df_daily_cases[0]["lastUpdate"]
            else:
                update = 0

            if "deaths" in df_daily_cases[0].keys():
                deaths = df_daily_cases[0]["deaths"]
            else:
                deaths = 0

            if "critical" in df_daily_cases[0].keys():
                critical = df_daily_cases[0]["critical"]
            else:
                critical = 0


            info = {'Country': country, 'Country Code': country_code,
                    'Confirmed Cases': confirmed, 'Critical Cases': critical,
                    'Recovered Cases': recovered, 'Deaths': deaths,
                    'Last Updated': update, 'Longitude': longitude,
                    'Latitude': latitude
                   }
            df_final=df_final.append(info, ignore_index = True)

        time.sleep(2)
    df_final["Confirmed Cases"]= df_final["Confirmed Cases"].astype(float)
    df_final["Recovered Cases"]= df_final["Recovered Cases"].astype(float)
    df_final["Critical Cases"]= df_final["Critical Cases"].astype(float)
    df_final["Deaths"]= df_final["Deaths"].astype(float)
    return df_final

def get_total_cases():
    url = "https://covid-19-data.p.rapidapi.com/totals"
    querystring = {"format":"json"}
    headers = {
        'x-rapidapi-host': "covid-19-data.p.rapidapi.com",
        'x-rapidapi-key': "46345e418cmsh542642b3ab38d2fp12ab20jsne42343ea4346"
        }
    response = requests.request("GET", url, headers=headers, params=querystring)

    df_total_stats = pd.DataFrame(response.json())
    return df_total_stats

def countries_info():
    # Make API request to get information about countries
    url = "https://covid-19-data.p.rapidapi.com/help/countries"

    querystring = {"format":"json"}

    headers = {
        'x-rapidapi-host': "covid-19-data.p.rapidapi.com",
        'x-rapidapi-key': "46345e418cmsh542642b3ab38d2fp12ab20jsne42343ea4346"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.json()

def get_news():

    url = "https://covid-19-news.p.rapidapi.com/v1/covid"
    querystring = {"lang":"en","media":"True","q":"covid"}
    headers = {
        'x-rapidapi-host': "covid-19-news.p.rapidapi.com",
        'x-rapidapi-key': "46345e418cmsh542642b3ab38d2fp12ab20jsne42343ea4346"
        }
    response = requests.request("GET", url, headers=headers, params=querystring)
    news = response.json()['articles']
    df_news = pd.DataFrame(news, columns= ['title','summary', 'link', 'language', 'clean_url'])
    #df_news = df_news[df_news['clean_url'] == 'cdc.gov']

    return df_news


countries_list =countries_info()
df_countries_info = pd.DataFrame(countries_list)
time.sleep(2)
columns = [ 'Country', 'Country Code',
            'Confirmed Cases', 'Critical Cases',
            'Recovered Cases', 'Deaths',
            'Last Updated', 'Longitude',
            'Latitude',
           ]
df_final = pd.DataFrame(columns = columns)
df_final=get_daily_report_countries(df_final)
df_final.to_csv('df_final.csv')
df_total_stats = get_total_cases()
df_total_stats.to_csv('df_total_stats.csv')
df_news = get_news()
df_news.to_csv('df_news.csv')
