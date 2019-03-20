import requests
import bs4
from bs4 import BeautifulSoup
import re
from models.job_db import Job_db

def scrape_job_page(url):
    """scrape the full job page"""

    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    job_info = {}

    for script in soup(["script", "style"]):
        script.extract()

    try:
        info = soup.find(name='div', attrs={'class': 'jobsearch-DesktopStickyContainer'})
        job_info['position'] = info.find(name='h3').text
        job_info['company'] = soup.find(attrs={'class': 'jobsearch-DesktopStickyContainer-companyrating'}).find_all(name='div')[0].text
        #description = soup.find(attrs={'class': 'jobsearch-JobComponent-description'}).get_text()
        description = soup.find(attrs={'class': 'jobsearch-JobComponent-description'}).get_text()
        job_info['description'] = description
        location_info = soup.find(name='div', attrs={'class': 'jobsearch-DesktopStickyContainer-companyrating'}).text.split('-')[1].split(' ')
        location = ' '.join([i for i in location_info if not i.isdigit()])
        job_info['location'] = location
        date = soup.find(attrs={'class': 'jobsearch-JobMetadataFooter'}).text
        days_ago = re.search('[0-9+]+ [dayshourago+]+', date).group(0)
        day = days_ago.split()
        if day[1][0] == 'h':
            day = 1
        day = int(day[0][:2])
        job_info['date_post'] = day
        return job_info
    except:
        pass
    return None

def scrape_links(url):
    """Get all links from listing page"""

    jobs_page = requests.get(url)
    soups = BeautifulSoup(jobs_page.text, "html.parser")

    all_job_list = []
    job_obj = {}
    for div in soups.find_all(name='div', attrs={'class':'row'}):
        for a in div.find_all(name='a', attrs={'data-tn-element':'jobTitle'}):
            job_link = "https://www.indeed.com/" + a['href']
            job_obj['job_link'] = job_link
            job_page = scrape_job_page(job_link)
            if job_page:
                job_obj.update(job_page)
                all_job_list.append(job_obj)
            job_obj = {}
    return all_job_list

def get_jobs_list(total_jobs):
    """get total jobs"""

    min_pages = total_jobs // 50
    page_ct = 0
    all_jobs = []

    url = "https://www.indeed.com/jobs?q=software+engineer&l=San+Francisco,+CA&limit=50&fromage=15&radius=25&start="

    for i in range(min_pages):
        url_list = url + str(page_ct)
        jobs_per_link = scrape_links(url_list)
        all_jobs.extend(jobs_per_link)
        page_ct += 50

    for job in all_jobs:
        new_job = Job_db(
            company = job['company'],
            location = job['location'],
            position = job['position'],
            description = job['description'],
            link = job['job_link']
        )
        new_job.date_post = job['date_post']
        new_job.save()


if __name__ == "__main__":
    get_jobs_list(101)
