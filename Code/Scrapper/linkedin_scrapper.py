from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import mysql.connector
from mysql.connector import Error
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import helper
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from socket import gaierror
from webdriver_manager.chrome import ChromeDriverManager
import smtplib
import requests
from bs4 import BeautifulSoup
import json
import traceback

def get_jobs(role, location, no_of_jobs_to_retrieve, all_skills):
    match_threshold=1
    url = "https://www.linkedin.com/jobs/jobs-in-"+location+"?keywords="+role+"&f_JT=F%2CP&f_E=1%2C3&position=1&pageNum=0"
    url = url.replace(' ', '%20')
    print(url)
    k1 = requests.get(url)
    soup1 = BeautifulSoup(k1.content, 'html.parser')
    string1 = soup1.find_all("a",{"class":"base-card__full-link"})
    jobs = []
    job_role = []
    job_details={}
    try:
        for i in range(len(string1)):
            if no_of_jobs_to_retrieve>0:
                job = {}
                job["title"] = string1[i].get_text().replace('\n',' ').replace(' ','')
                job["url"] = string1[i]['href']
                job_details[job["url"]] = [job["title"], ""]
                job_role.append(string1[i].get_text().replace('\n',' ').replace(' ',''))
                no_of_jobs_to_retrieve-=1
                k = requests.get(string1[i]['href']).text
                soup=BeautifulSoup(k,'html.parser')
                str2 = soup.find_all("div", {"class" : "description__text"})
                if len(str2) > 0:
                    str3 = str2[0].get_text()
                job["skills"] = helper.extract_skills(str3, all_skills)
                jobs.append(job)
    except Exception as e:
        traceback.print_exc()
        final_result = {}
        job_details = {}
    return jobs
