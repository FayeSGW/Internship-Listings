import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import re

headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})

def main():
    Indeed()

def Glassdoor():
    url = "https://www.glassdoor.com/Job/norway-internship-jobs-SRCH_IL.0,6_IN180_KO7,17.htm?industryNId=10013"

    page = requests.get(url)

    soup = bs(page.content, "html.parser")

    jobs = soup.find_all("li", class_ = "react-job-listing")

    for job in jobs:
        a = job.find_all("a")
        rating = job.find("span", class_ = "job-search-key-srfzj0")
        print(f"Company: {a[1].get_text()}")
        print(f"Job Title: {a[2].get_text()}")
        print(f"Rating: {rating.get_text()} / 5")
        link = a[0]["href"]
        print(f"Link: {link}\n")


def Indeed():
    baseurl = "https://no.indeed.com/jobs?q=it%20intern&l=Oslo?"
    urls = []
    joblst = []
    complst = []
    page = requests.get(baseurl, headers = headers)
    soup = bs(page.content, "html.parser")

    pg_no = soup.find("div", id = "searchCountPages").text.strip()
    if "\xa0" in pg_no:
        page_no = int(pg_no[10:16].replace("\xa0", ""))
    else:
        page_no = int(pg_no[10:13])
  
    for num in range(0, page_no, 10):
        urls.append(baseurl + "&start=" + str(num))

    for url in urls:
        page = requests.get(url, headers = headers)
        soup = bs(page.content, "html.parser")
        jobs = soup.find_all("div", class_ = "cardOutline")

        for job in jobs:
            title = job.find("h2", class_ = "jobTitle").get_text()
            company = job.find("span", class_ = "companyName").get_text()
            match1 = re.search(r"\bintern\b", title, re.IGNORECASE)
            match2 = re.search(r"\binternship\b", title, re.IGNORECASE)
            match3 = re.search(r"\nsales\b", title, re.IGNORECASE)
            if match1 or match2 and not match3:
                joblst.append(title)
                complst.append(company)

    inddict = {"Company": complst, "Title": joblst}
    indDF = pd.DataFrame(inddict)

    unique = indDF.drop_duplicates()
    print(unique)



    
           




if __name__ == "__main__":
    main()