import requests
import bs4
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta


def scrape_job_page(url):

    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    job_info = {}

    for script in soup(["script", "style"]):
        script.extract()

    try:
        info = soup.find(name='div', attrs={'class': 'jobsearch-DesktopStickyContainer'})
        if info:
            job_info['position'] = info.find(name='h3').text
            job_info['company'] = soup.find(attrs={'class': 'jobsearch-DesktopStickyContainer-companyrating'}).find_all(name='div')[0].text
            job_info['description'] = soup.get_text()
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

    min_pages = total_jobs // 50
    page_ct = 0
    all_jobs = []

    url = "https://www.indeed.com/jobs?q=software+engineer&l=San+Francisco,+CA&limit=50&fromage=15&radius=25&start="

    for i in range(min_pages):
        url_list = url + str(page_ct)
        jobs_per_link = scrape_links(url)
        all_jobs.extend(jobs_per_link)
        page_ct += 50
    print(all_jobs)
    print(len(all_jobs))

if __name__ == "__main__":
#    scrape_links("https://www.indeed.com/jobs?as_and=software+engineer&as_phr=&as_any=&as_not=&as_t#tl=&as_cmp=&jt=all&st=&as_src=&salary=&radius=25&l=San+Francisco+Bay+Area%2C+CA&fromage=any&limit=5#0&sort=&psf=advsrch")

    get_jobs_list(101)
