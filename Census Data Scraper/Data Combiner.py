import csv
import pandas as pd
from bs4 import BeautifulSoup
import re


# Open first HTML file and define a "soup" variable to store its HTML content

with open("Bureau of Labor Statistics Data.html", "r") as first_200_counties_html:
    first_200_counties_soup = BeautifulSoup(first_200_counties_html, 'html.parser')


# Make an array to store all the counties in

counties = []

# Append name of all Texas counties to counties array

for table in first_200_counties_soup.find_all("table", class_="catalog"):
    tds = table.find_all("td")
    counties.append(tds[2].text[:len(tds[2]) - 5])



# Extract date from HTML data

def get_date(raw_row):
    raw_row = str(raw_row)
    first_half = raw_row[0:raw_row.find("</th")]
    second_half = raw_row[raw_row.find("</th"):len(raw_row)]
    year = first_half[len(first_half)-4:]
    month = second_half[second_half.find("scope=") + 12:second_half.find("scope=") + 15]
    date = str(year) + "-" + str(month)
    return date



# Extract data and append it to 2D array

data = []
    
for i in range(len(counties)):
    data_tables = first_200_counties_soup.find_all("table", id="table{}".format(i))
    for data_table in data_tables:
        raw_rows = data_table.find_all("tr")
        for raw_row in raw_rows:
            row = []
            row.append(counties[i])
            row.append(get_date(raw_row))
            for variable in raw_row.find_all("td"):
                row.append(variable.text)
            print(row)
            if len(row) == 6:
                data.append(row)
        

# Write 2D data array to CSV

with open("County Employment.csv", "a", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["County", "Name", "Labor Force", "Employment", "Unemployment", "Unemployment Rate"])
    csv_writer.writerows(data)
    csv_file.close()




# Repeat the processes outlined above but with the second file containing the remaining counties

remaining_counties = []

with open("Bureau of Labor Statistics Data 2.html", "r") as remaining_counties_html:
    remaining_counties_soup = BeautifulSoup(remaining_counties_html, 'html.parser')
    

for table in remaining_counties_soup.find_all("table", class_="catalog"):
    tds = table.find_all("td")
    remaining_counties.append(tds[2].text[:len(tds[2]) - 5])
    
remaining_data = []
    
for i in range(1, len(counties)):
    data_tables = remaining_counties_soup.find_all("table", id="table{}".format(i))
    for data_table in data_tables:
        raw_rows = data_table.find_all("tr")
        try: 
            for raw_row in raw_rows:
                row = []
                row.append(remaining_counties[i])
                row.append(get_date(raw_row))
                for variable in raw_row.find_all("td"):
                    row.append(variable.text)
                print(row)
                if len(row) == 6:
                    remaining_data.append(row)
        except:
            print("DONE")
                

with open("County Employment.csv", "a", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerows(remaining_data)
    csv_file.close()