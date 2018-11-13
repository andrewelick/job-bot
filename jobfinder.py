import time
from bs4 import BeautifulSoup
from requests import get


#Function that checks Indeed.com for the jobs that match the user desc and location
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
            indeed_add_link = indeed_each_heading.find('a')['href']
            indeed_add_link = "https://www.indeed.com"+indeed_add_link
            indeed_all_link_list.append(indeed_add_link)
        except:
            continue

    time.sleep(2)

    #Loop that goes through each job link, goes to the page, and grabs the information needed
    for indeed_link in indeed_all_link_list:

        #Go to job page and parse
        indeed_response = get(indeed_link)
        indeed_soup2 = BeautifulSoup(indeed_response.text, 'html.parser')
        type(indeed_soup2)

        try:
            #Find title of job and company
            indeed_job_header_info = indeed_soup2.find('div', class_='jobsearch-DesktopStickyContainer')
            indeed_job_title = indeed_job_header_info.find('h3').text
            indeed_job_company = indeed_job_header_info.find('div').text
            print (indeed_job_title)
            print (indeed_job_company)

            #Find container holding all the job description info
            indeed_description_container = indeed_soup2.find('div', class_='jobsearch-JobComponent-description').text
            print (indeed_description_container)
        except:
            continue

        #Wait some time after gathering job information
        time.sleep(1.5)

#Function that checks Ziprecruiter.com for relevant job postings
def zip_search(keyword, zipcode):

    #Ziprecruiter Url
    zip_url = "https://www.ziprecruiter.com/candidate/search?radius=25&days=5&search="+keyword+"&location="+zipcode
    zip_response = get(zip_url)
    zip_soup = BeautifulSoup(zip_response.text, 'html.parser')
    type(zip_soup)

    #Finds main job listing container and finds each indivdual job posting
    zip_all_jobs_container = zip_soup.find('div', id='job_list')
    zip_each_job_container = zip_all_jobs_container.findChildren('article')

    #indivdual job list for ziprecruiter
    zip_all_link_list = []

    #For loop that grabs each link from each job posting and puts URL inside of list
    for zip_each_job in zip_each_job_container:
        zip_add_link = zip_each_job.find('a')['href']
        zip_all_link_list.append(zip_add_link)

    #Loop for each link and gather job information from the page
    for zip_link in zip_all_link_list:

        #Go to indivdual job posting
        zip_response2 = get(zip_link)
        zip_soup2 = BeautifulSoup(zip_response2.text, 'html.parser')
        type(zip_soup2)

        try:
            #Find job description container
            zip_job_desc_container = zip_soup2.find('div', class_='job_description')

            #Zip job title/company/location info
            zip_job_title_container = zip_job_desc_container.find('div', class_='job_header')
            zip_job_title = zip_job_desc_container.find('h1').text.strip()
            zip_job_company = zip_job_desc_container.find('span').text.strip()
            zip_job_location = zip_job_desc_container.find('a', class_='location_text').text.strip()

            print (zip_job_title)
            print (zip_job_company)
            print ("")
            #Find job description
            zip_job_description = zip_job_desc_container.find('div', class_='jobDescriptionSection').text
        except:
            continue

        time.sleep(1.5)

#Function that checks Monster.com for job postings
def monster_search(keyword, zipcode):

    #Url for Monster.com main job search
    monster_url = "https://www.monster.com/jobs/search/?q="+keyword+"&where="+zipcode
    monster_response = get(monster_url)
    monster_soup = BeautifulSoup(monster_response.text, 'html.parser')
    type(monster_soup)

    #Find all job results container, then gather all the job postings
    monster_all_jobs_container = monster_soup.find('div', id='SearchResults')
    monster_all_jobs = monster_all_jobs_container.findChildren('section')

    #List for all monster job urls to be used for indivdual search
    monster_all_link_list = []

    #Loop that goes through each job posting found, extracts its URL, then places it into a list for later use
    for monster_each_job in monster_all_jobs:
        try:
            monster_add_link = monster_each_job.find('a')['href']
            monster_all_link_list.append(monster_add_link)
        except:
            continue

    for monster_link in monster_all_link_list:
        count += 1
        #Go to each individual job posting page
        monster_response2 = get(monster_link)
        monster_soup2 = BeautifulSoup(monster_response2.text, 'html.parser')
        type(monster_soup2)

        try:
            #Find Job title and company
            monster_job_title_company = monster_soup2.find('div', class_='heading').find('h1').text.strip()

            #Find job description
            monster_job_description = monster_soup2.find('div', class_='details-content').text.strip()

        except:
            continue
        return

keywords= "software developer"
zipcode = "38017"
monster_search(keywords, zipcode)
