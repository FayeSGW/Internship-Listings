import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import re

headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})

def main():
    global companies
    global titles
    global links
    companies = []
    titles = []
    links = []

    Glassdoor()
    Finn()

    jobsdict = {"Company": companies, "Title": titles, "Link": links}

    jobsDF = pd.DataFrame(jobsdict)
    uniquejobsDF = jobsDF.drop_duplicates()
    print(uniquejobsDF)
    

def Glassdoor():
    url = "https://www.glassdoor.com/Job/norway-internship-jobs-SRCH_IL.0,6_IN180_KO7,17.htm?industryNId=10013"

    page = requests.get(url)

    soup = bs(page.content, "html.parser")

    jobs = soup.find_all("li", class_ = "react-job-listing")

    
    for job in jobs:
        a = job.find_all("a")
        company = a[1].get_text()
        title = a[2].get_text()
        link = a[0]["href"]

        companies.append(company)
        titles.append(title)
        links.append(link)


def Finn():
    baseurl = "https://www.finn.no/job/fulltime/search.html?location=1.20001.20061&occupation=0.23"
    urls = ["https://www.finn.no/job/fulltime/search.html?location=1.20001.20061&occupation=0.23"]

    page = requests.get(baseurl)
    soup = bs(page.content, "html.parser")

    pages = soup.find_all("a", class_ = "pagination__page")

    for i in range(len(pages)):
        url = baseurl + "&page=" + str(i+1)
        urls.append(url)

    for url in urls:
        newpage = requests.get(url)
        newsoup = bs(newpage.content, "html.parser")
        jobs = newsoup.find_all("div", class_ = "ads__unit__content")

        for job in jobs:
            title = job.find("div", class_ = "ads__unit__content__keys")
            company = job.find("div", class_ = "ads__unit__content__list").get_text()
            link = job.find("a", class_ = "ads__unit__link")["href"]

            
            if title == None:
                pass
            else:
                title = title.get_text()
                internptn = re.search(r"\bintern\b", title, re.IGNORECASE)
                internshipptn = re.search(r"\binternship\b", title, re.IGNORECASE)
                if internptn or internshipptn:
                    titles.append(title)
                    companies.append(company)
                    links.append(link)

        
        



    
           




if __name__ == "__main__":
    main()