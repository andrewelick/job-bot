import time
import textwrap
from bs4 import BeautifulSoup
from requests import get


#Function that checks Indeed.com for the jobs that match the user desc and location
def indeed_search(keywords, zipcode, job_radius, job_posted):

    #Go to Indeed Url using the users preferences and parse the page
    indeed_url= "https://www.indeed.com/jobs?as_and="+keywords+"&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&as_src=&salary=&radius="+job_radius+"&l="+zipcode+"&fromage="+job_posted+"&limit=50&sort=date&psf=advsrch"
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

            #Find container holding all the job description info
            indeed_description_container = indeed_soup2.find('div', class_='jobsearch-JobComponent-description').text
            indeed_description_container = textwrap.fill(indeed_description_container, 100)
        except:
            continue

        try:
            print (indeed_job_title)
            print (indeed_job_company)
            print (indeed_description_container)
        except Exception as error:
            print (error)

        return
        #Wait some time after gathering job information
        time.sleep(1.5)

#Function that checks Ziprecruiter.com for relevant job postings
def zip_search(keywords, zipcode):

    #Ziprecruiter Url
    zip_url = "https://www.ziprecruiter.com/candidate/search?radius=25&days="+zip_posted+"&search="+keywords+"&location="+zipcode
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

            #Find job description
            zip_job_description = zip_job_desc_container.find('div', class_='jobDescriptionSection').text.strip()
            zip_job_description = textwrap.fill(zip_job_description, 100)

            print (zip_job_title)
            print (zip_job_company)
            print (zip_job_description)
            print ("")
        except:
            continue

        return
        time.sleep(1.5)

#Function that checks Monster.com for job postings
def monster_search(keywords, zipcode, monster_radius, job_posted):

    #Url for Monster.com main job search
    monster_url = "https://www.monster.com/jobs/search/?q="+keywords+"&intcid=skr_navigation_nhpso_searchMain&rad="+monster_radius+"&where="+zipcode+"&tm="+monster_posted
    print (monster_url)
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

        #Go to each individual job posting page
        monster_response2 = get(monster_link)
        monster_soup2 = BeautifulSoup(monster_response2.text, 'html.parser')
        type(monster_soup2)

        try:
            #Find Job title and company
            monster_job_title_company = monster_soup2.find('div', class_='heading').find('h1').text.strip()

            #Find job description
            monster_job_description = monster_soup2.find('div', class_='details-content').text.strip()
            monster_job_description = textwrap.wrap(monster_job_description, 100)

            print (monster_job_title_company)
            print (monster_job_description)
        except:
            continue
        return

#Function to handle user inputs and format them so that each website can use them correctly
def user_input_handler(keywords, zipcode, job_radius, job_posted):

    #Adjust job radius to work with each website
    if job_radius == 5:
        indeed_radius = "5"
        zip_radius = "5"
        monster_radius = "5"
    elif job_radius == 10:
        indeed_radius = "10"
        zip_radius = "10"
        monster_radius = "10"
    elif job_radius == 15:
        indeed_radius = "15"
        zip_radius = "25" #No 15 mile radius for ziprecruiter, bumping up to 25 miles
        monster_radius = "20" #No 15 mile radius for Monster, bumping to 20 miles
    elif job_radius == 25:
        indeed_radius = "25"
        zip_radius = "25"
        monster_radius = "30" #No 25 mile radius for Monster, bumping to 30 miles
    elif job_radius == 50:
        indeed_radius = "50"
        zip_radius = "50"
        monster_radius = "50"
    elif job_radius == 100:
        indeed_radius = "100"
        zip_radius = "100"
        monster_radius = "100"
    else:
        indeed_radius = ""
        zip_radius = "5000"
        monster_radius = "200"

    #Format the job_posted time to work with each website
    if job_posted == 0: #Within 24 hours
        indeed_posted = "1"
        zip_posted = "1"
        monster_posted = "1"
    elif job_posted == 1: #Last 3 days
        indeed_posted = "3"
        zip_posted = "5" #No 3 day option, pushing up to 5 days
        monster_posted = "3"
    elif job_posted == "2": #Last 7 Days
        indeed_posted = "7"
        zip_posted = "10" #No 7 day option, pushing up to 10 days
        monster_posted = "7"
    else: #Anytime
        indeed_posted = "any"
        zip_posted = ""
        monster_posted = ""


    indeed_search(keywords, zipcode, indeed_radius, indeed_posted)
keywords= "software developer"
zipcode = "38017"
job_radius = 5
job_posted = 0

user_input_handler(keywords, zipcode, job_radius, job_posted)
