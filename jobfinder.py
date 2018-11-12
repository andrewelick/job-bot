import time
from bs4 import BeautifulSoup
from requests import get


#Function that checks indeed for the jobs that match the user desc and location
def indeed_search(keyword, zipcode):

    #Go to Indeed Url using the users preferences and parse the page
    indeed_url= "https://www.indeed.com/jobs?as_and="+keywords+"&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&as_src=&salary=&radius=25&l="+zipcode+"&fromage=3&limit=50&sort=date&psf=advsrch"
    indeed_response = get(indeed_url)
    indeed_soup = BeautifulSoup(indeed_response.text, 'html.parser')
    type(indeed_soup)

    #Find container holding all the job listings
    indeed_all_results_container = indeed_soup.find('td', id='resultsCol')
    indeed_all_results = indeed_all_results_container.findChildren('div', class_='row')

    #List that stores each job link so they can each be parsed
    indeed_all_link_list = []

    #Use loop to go through each result and grab link and put into indeed_all_link_list
    for indeed_job in indeed_all_results:
        try:
            indeed_each_heading = indeed_job.find('h2')
            indeed_each_link = indeed_each_heading.find('a')['href']
            indeed_each_link = "https://www.indeed.com"+indeed_each_link
            indeed_all_link_list.append(indeed_each_link)
        except:
            continue

    time.sleep(2)

    #Loop that goes through each job link, goes to the page, and grabs the information needed
    for indeed_link in indeed_all_link_list:

        #Go to job page and parse
        indeed_response = get(indeed_link)
        indeed_soup2 = BeautifulSoup(indeed_response.text, 'html.parser')
        type(indeed_soup2)

        #Find title of job and company
        indeed_job_header_info = indeed_soup2.find('div', class_='jobsearch-DesktopStickyContainer')
        indeed_job_title = indeed_job_header_info.find('h3')
        indeed_job_company = indeed_job_header_info.find('div')
        print (indeed_job_title.text)
        print (indeed_job_company.text)

        #Find container holding all the job description info
        indeed_description_container = indeed_soup2.find('div', class_='jobsearch-JobComponent-description')
        print (indeed_description_container.text)
        return

keywords= "software developer"
zipcode = "38017"
indeed_search(keywords, zipcode)
