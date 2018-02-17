import requests
from numpy import append
import bs4
from bs4 import BeautifulSoup

import pandas as pd
import time

# #Cities
# max_results_per_city = 100 # pages of results per city
# city_set = ["Boston%2C+ma","Concord%2C+nh","Portsmouth%2C+nh","Nashua%2C+nh","Manchester%2C+nh","Worcester%2C+ma"]#,"Portland%2C+or","Seattle%2C+wa","Denver%2C+co","Hartford%2C+ct","New+Haven%2C+ct","Providence%2C+ri","Portland%2C+me"]

# #job titles
# job_title_set = ["mechanical+engineer","product+engineer","mechanical+design+engineer","design+engineer","engineer", "automatin engineer", "automations engineer"]

# #job type
# job_type_set = ["fulltime","contract"]

# #experience level
# exp_set = ["entry_level"]#,"mid_level"]

# url_set = []

# for city in range(0, len(city_set), 1):
#     for job_title in range(0, len(job_title_set), 1):
#         for job_type in range(0, len(job_type_set),1):
#            for exp in range(0, len(exp_set),1):
#                for page in range(0, max_results_per_city, 10):
#                    url_set.append("https://www.indeed.com/jobs?q=" + job_title_set[job_title] + "&l=" + city_set[city] +"&jt=" + job_type_set[job_type] + "&explvl=" + exp_set[exp] + "&sort=date&radius=25&start=" + str(page))

# #Columns for formatting
# columns = ["url", "job_title", "company_name", "location", "summary", "date", "exp_lvl", "job_type", "job_url" , "job_comp_loc"]
# sample_df = pd.DataFrame(columns = columns)

# #Scraping code
# for url in url_set:
#     page = requests.get(url)
#     time.sleep(1)  #ensuring at least 1 second between page grabs
#     soup = BeautifulSoup(page.text, "lxml")

#     for div in soup.find_all(name="div", attrs={"class":"row"}):
#         #specifying row num for index of job posting in dataframe
#         num = (len(sample_df) + 1) 
        
#         #creating an empty list to hold the data for each posting
#         job_post = [] 
        
#         #append url
#         job_post.append(url) 
        
#         #grabbing job title
#         for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
#                 job_post.append(a["title"])
        
#         #grabbing company name
#         company = div.find_all(name="span", attrs={"class":"company"}) 
#         if len(company) > 0: 
#             for b in company:
#                 job_post.append(b.text.strip()) 
#         else: 
#             sec_try = div.find_all(name="span", attrs={"class":"result-link-source"})
#             for span in sec_try:
#                 job_post.append(span.text) 
        
#         #grabbing location name
#         c = div.findAll("span", attrs={"class": "location"}) 
#         for span in c: 
#             job_post.append(span.text) 
    
#         #grabbing summary text
#         d = div.findAll("span", attrs={"class": "summary"}) 
#         for span in d:
#             job_post.append(span.text.strip()) 
        
# #         # #grabbing salary
# #         # try:
# #         #     job_post.append(div.find("nobr").text) 
# #         # except:
# #         #     try:
# #         #         div_two = div.find(name="div", attrs={"class":"sjcl"}) 
# #         #         div_three = div_two.find("div") 
# #         #         job_post.append(div_three.text.strip())
# #         #     except:
# #         #         job_post.append("Nothing_found")
        
#         #grabbing post date
#         e = div.find_all(name="span", attrs={"class":"date"})
#         if len(e) > 0: 
#             for f in e:
#                 job_post.append(f.text) 
#         else: 
#             job_post.append("Sponsored?")
        
#         #experience level from url
#         if exp_set[0] in url:
#             job_post.append("Entry-level")
        
#         # if exp_set[1] in url:
#         #     job_post.append("Mid-level")
        
#         #job type from url
#         if job_type_set[0] in url:
#             job_post.append("Full-time")

#         if job_type_set[1] in url:
#             job_post.append("Contract")
        
#         #job link url
#         for f in div.find_all('a', attrs={"data-tn-element":"jobTitle"},href=True):
#             job_post.append("https://www.indeed.com" + str(f['href']))

#         #makeshift fix for job_post being too short (ex: url doesn't really exist)
#         while len(job_post) < 9:
#             job_post.append("data_is_junk")

#         #concatenate job, company, location
#         job_post.append(str(job_post[1] + "." + str(job_post[2] + "." + str(job_post[3]))))
        
#         #add job_post to data frame
#         sample_df.loc[num] = job_post
        
# #saving sample_df as a local csv file — define your own local path to save contents 
# sample_df.to_csv('Indeed_Scrape.csv', encoding="utf-8")

#reading csv with index_col = 0, otherwise I get an additional
#unnamed column of separate index values
scrape_data = pd.read_csv('Indeed_Scrape.csv')

#removing characters so that elimination works correctly later
scrape_data['job_title'] = scrape_data['job_title'].str.replace(r"\(.*\)","")
scrape_data['company_name'] = scrape_data['company_name'].str.replace(r"\(.*\)","")
scrape_data['location'] = scrape_data['location'].str.replace(r"\(.*\)","")
scrape_data['job_comp_loc'] = scrape_data['job_comp_loc'].str.replace(r"\(.*\)","")

#print(scrape_data.job_title)

#eliminating undesired jobs
search_job_title_for = ['quality','software','senior','sr ','professor','intern','co-op','technician','chief','cloud','data scientist','full stack','reliability','firmware',
'manufactur','network','principal','principle','real estate','sales','verification','president','maintenance','mgr','manager',
'city','civil','api platform','big data','big data','back end','clerk','content writer','data engineer','education researcher','highway','helpdesk','interior designer','lead','nanny',
'administrator','plumber','secretary','labor','recruiter','technical support','wireless modem','wordpress']
scrape_data = scrape_data[~scrape_data.job_title.str.contains('|'.join(search_job_title_for), case = False)]

#removing jobs that I applied to
applied_already = ['Energy Efficiency Associate.Energy Solutions.Boston, MA 02108 ']
scrape_data = scrape_data[~scrape_data.job_comp_loc.str.contains('|'.join(applied_already), case = False)]

#removing jobs on my blacklist (unqualified, terrible, etc.) **C
blacklist = ['Engineering Specialist II - Canton, MA.Siemens AG.Canton, MA']
scrape_data = scrape_data[~scrape_data.job_comp_loc.str.contains('|'.join(blacklist))]

#removing invalid results **choose whatever column is before job_comp_loc
search_junk = ["data_is_junk"]
scrape_data = scrape_data[~scrape_data.job_url.str.contains('|'.join(search_junk))]

#Reducing columns
columns_2 = ["job_title", "company_name", "location", "summary", "date", "exp_lvl", "job_type", "job_url" , "job_comp_loc"]
scrape_data = scrape_data[columns_2]

#removing old job posts note: DO THIS BEFORE REMOVING DUPLICATES
search_date = ["30"]
scrape_data = scrape_data[~scrape_data.date.str.contains('|'.join(search_date), case = False)]

#Attempt to organize data by job post date. Oldest duplicates first to capture 'true' age. Doesn't work. Does put text at top though.
scrape_data = scrape_data.sort_values('date', ascending = False)

# #before drop_duplicates is run
# scrape_data.to_csv('Indeed_Scrape_pre_drop.csv', index=False)

#dropping any duplicate rows:
scrape_data = scrape_data.drop_duplicates(subset=["job_title","company_name","location"], keep='first')
scrape_data.to_csv('Indeed_Scrape_nodupe.csv', index=False)

#sorting
scrape_data = scrape_data.sort_values('job_title')

#outputting quality list to csv
scrape_data.to_csv('Indeed_Scrape_polished.csv', index=False)