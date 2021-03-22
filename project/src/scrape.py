import requests
import sys
import os
import pandas
from requests_html import HTML



def url_to_data(*, url: str):
    data = []
    
    request = requests.get(url)
    if request.status_code == 200:
        result = request.text
        
        response_html = HTML(html=result)
        
        table_class = '.imdb-scroll-table'
        table = response_html.find(table_class)[0]
        
        headers_class = 'th'
        headers_names = table.find(headers_class)
        headers = [header.text for header in headers_names]
        
        rows = table.find('tr')
        for row in rows[1:]:
            columns = row.find('td')
            row_data=[]
            for column in columns:
                row_data.append(column.text)

            data.append(row_data)

        return [headers,data]



def data_to_csv(*, headers=None, data=None, year: str):
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DOWNLOAD_DIR = os.path.join(BASE_DIR, 'data')
    
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

    filename=os.path.join(DOWNLOAD_DIR,f'boxofficemojo.com-{year}.csv')

    data_frame = pandas.DataFrame(data, columns=headers)
    data_frame.to_csv(filename, index=False)    



def run(*, start_year=2015, end_year=2021):

    for year in range(start_year, end_year+1):
        url = f'https://www.boxofficemojo.com/year/world/{year}/'
        data= url_to_data(url=url)
        data_to_csv(headers=data[0], data=data[1],year=year)



if __name__ == '__main__':
    
    try:
        start_year = int(sys.argv[1])        
    except:
        start_year = 2018
    try:
        end_year = int(sys.argv[2])
    except:
        end_year = 2021

    run(start_year=start_year,end_year=end_year)