import requests
import bs4
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
#from models.engine import db_storage
#storage = db_storage.DBStorage()
#storage.reload()



def find_keywords(description):
    """match keywords"""

    d_list = description.replace(",", " ").replace("(", " ").replace(")", " ").split()
    keywords = {"python", "javascript", "html", "css", "ruby", "bash",
                "linux", "unix", "rest", "restful", "api", "aws",
                "cloud", "svn", "git", "junit", "testng", "java", "php",
                "agile", "scrum", "nosql", "mysql", "postgresdb", "postgres",
                "shell", "scripting", "mongodb", "puppet", "chef", "ansible",
                "nagios", "sumo", "nginx", "haproxy", "docker", "automation",
                "jvm", "scikit-learn", "tensorflow", "vue", "react", "angular",
                "webpack", "drupal", "gulp", "es6", "jquery", "sass", "scss",
                "less", "nodejs", "node.js", "graphql", "postgresql", "db2",
                "sql", "spring", "microservices", "kubernates", "swagger",
                "hadoop", "ci/cd", "django", "elasticsearch", "redis", "c++",
                "c", "hive", "spark", "apache", "mesos", "gcp", "jenkins",
                "azure", "allcloud", "amqp", "gcp", "objective-c", "kotlin"
                "kafka", "jira", "cassandra", "containers", "oop", "redis",
                "memcached", "redux", "bigquery", "bigtable", "hbase", "ec2",
                "s3", "gradle", ".net", "riak", "shell", "hudson", "maven",
                "j2ee", "oracle", "swarm", "sysbase", "dynamodb", "neo4",
                "allcloud", "grunt", "gulp", "apex", "rails", "mongo", "apis",
                "html5", "css3", "rails", "scala", "rasa", "soa", "soap",
                "microservices", "storm", "flink", "gitlab", "ajax",
                "micro-services", "oop", "saas", "struts", "jsp", "freemarker",
                "hibernate", "rlak", "solidity", "heroku", "ecs", "gce",
                "scripting", "perl", "c#", "golang", "xml", "newrelic",
                "grafana", "helm", "polymer", "closure", "backbone",
                "atlassian", "angularjs", "flask", "scikitlearn", "theano",
                "numpy", "scipy", "panda", "tableau", "gensim", "rpc",
                "graphql", "iaas", "paas", "azure", "es", "solr", "http", "iot",
                "kinesis", "lambda", "typescript", "gradle", "buck", "bazel"}

    found = [s for s in d_list if s.lower() in keywords]
    if "Go" in d_list:
        found.append("Go")
    if found:
        return set(found)
    return None

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
        description = soup.find(attrs={'class': 'jobsearch-JobComponent-description'}).get_text()
        job_info['description'] = description
        all_keys = find_keywords(description)
        job_info['skills_matched'] = (all_keys, len(all_keys))
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
        jobs_per_link = scrape_links(url)
        all_jobs.extend(jobs_per_link)
        page_ct += 50
    print(job_info)
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

#def get_location():
#    """get location"""

if __name__ == "__main__":
    get_jobs_list(101)
