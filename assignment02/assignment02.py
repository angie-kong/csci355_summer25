# CSCI 355 Internet Web Technologies
# July 2025
# Angela Kong
# Assignment 02 - Data Scraping, Storage, and Visualization

import OutputUtil as ou
import requests
import html5lib
from bs4 import BeautifulSoup

# function to get next text item from iterator
def next_text(itr):
    return next(itr).text


# function to get next int item from iterator
def next_int(itr):
    return int(next_text(itr).replace(',', ''))


# function to scrape the site
def scrape_covid_data(dict_populations):
    url = 'https://www.worldometers.info/coronavirus/countries-where-coronavirus-has-spread/'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    data = []
    # soup.find_all('td') will scrape every table-data element in the url's table
    itr = iter(soup.find_all('td'))
    # This loop will keep repeating as long as there is data available in the iterator
    while True:
        try:
            country = next_text(itr)
            confirmed = next_int(itr)
            deaths = next_int(itr)
            continent = next_text(itr)
            if country.startswith('Japan'):
                country = 'Japan'
            if country in dict_populations:
                population = dict_populations[country]
                pct_deaths = round(100*(deaths/population), 2)
                pct_cases = round(100*(confirmed/population), 2)
                href = "https://en.wikipedia.org/wiki/" + country
                a_attributes = 'href="' + href + '" target="_blank"'
                country_element = ou.create_element(ou.TAG_A, country, a_attributes)
                data.append([country_element, continent, population, confirmed, pct_cases, deaths, pct_deaths])
            else:
                print("Country not found in population data", country)
        # StopIteration error is raised when there are no more elements left for iteration
        except StopIteration:
            break
    # Sort the data by the number of confirmed cases
    # data.sort(key=lambda row: row[1], reverse=True)
    return data


# function to scrape website to get country populations
def scrape_population_data():
    url = 'https://www.worldometers.info/world-population/population-by-country/'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    dict_populations = {}
    itr = iter(soup.find_all('td'))
    while True:
        try:
            junk1 = next_text(itr)
            country = next_text(itr).strip()
            population = next_int(itr)
            junk4 = next_text(itr)
            junk5 = next_text(itr)
            junk6 = next_text(itr)
            junk7 = next_text(itr)
            junk8 = next_text(itr)
            junk9 = next_text(itr)
            junk10 = next_text(itr)
            junk11 = next_text(itr)
            junk12 = next_text(itr)
            dict_populations[country] = population
        # StopIteration error is raised when there are no more elements left for iteration
        except StopIteration:
            break
    return dict_populations


def main():
    dict_populations = scrape_population_data()
    # print(dict_populations)
    data = scrape_covid_data(dict_populations)
    # print(data)
    headers = ['Country', 'Continent', 'Population', 'Cases', '% Cases', 'Deaths', '% Deaths']
    alignments = ["l", "l", "r", "r", "r", "r", "r"]
    types = ["S", "S", "N", "N", "N", "N", "N"]
    file_name = "assignment02.html"
    title = "Assignment 02<br>COVID Data<br>Angela Kong"
    ou.write_html_file(file_name, title, headers, types, alignments, data, True)
    ou.write_xml_file('assignment02.xml', 'COVID_data', headers, data, True)
    ou.write_tt_file('Assignment02.txt', 'COVID_data', headers, data, alignments)


if __name__ == "__main__":
    main()