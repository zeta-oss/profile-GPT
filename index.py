from flask import Flask,render_template,jsonify,request
import os,json,openai,re

from bs4 import BeautifulSoup
import requests

import base64




app=Flask(__name__)
print((base64.b64decode("c2stdE94YnVRblRrRGk5MkQxdkJEbkpUM0JsYmtGSk5zTkNHWWI2THB6NVRiN1BkMFBs").decode('ascii')))
openai.api_key=base64.b64decode("c2stdE94YnVRblRrRGk5MkQxdkJEbkpUM0JsYmtGSk5zTkNHWWI2THB6NVRiN1BkMFBs").decode('ascii')


def create_job_summary(job_title):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"As a recruiter, write a blog on the requirements for job position: {job_title}",
        temperature=1.0,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.6,
        presence_penalty=0.6
    )
    return response["choices"][0]["text"]
    
def summaryize_job(summary):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"As a job seeker, summarize this job profile : {summary}",
        temperature=1.0,
        max_tokens=300,
        top_p=1.0,
        frequency_penalty=0.6,
        presence_penalty=0.6
    )
    return response["choices"][0]["text"]

    

def check_positive(txt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"As a recruiter, just mark this job profile: {txt} as 'good' or 'bad'",
        temperature=1.0,
        max_tokens=10,
        top_p=1.0,
        frequency_penalty=0.6,
        presence_penalty=0.6
    )
    return response["choices"][0]["text"]

def create_summary(name,linkedin,summary,job)->str:
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"As a recruiter, rate the job profile for {name} with his job summary: {summary} for job position:{job}",
        temperature=1.0,
        max_tokens=600,
        top_p=1.0,
        frequency_penalty=0.6,
        presence_penalty=0.6
    )
    print(response)
    return response["choices"][0]["text"]
    
def extract_linkedin_page(linkedin_url,position):
    r=requests.get(linkedin_url,headers= {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"})
    data=BeautifulSoup(r.content,'html.parser') 
    return rate_linkedin_page(data.prettify(),position)

def rate_linkedin_page(linkedin_scrapped,position):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"As a recruiter, just mark the Linkedin html page {linkedin_scrapped} as 'good' or 'bad' for job position: {position}",
        temperature=1.0,
        max_tokens=10,
        top_p=1.0,
        frequency_penalty=0.6,
        presence_penalty=0.6
    )
    print(response)
    return response["choices"][0]["text"]

def parse_json()->list:
    with open("data/data.json","r") as f:
        data=json.loads(f.read())
        empdata=[]
        for d in data["data_emp"]:
            empdata.append(d)
        return empdata


def find_job(empdata,position,name="")->list:
    if(name.strip()==""):
        data_pos=[]
       # print(position)
        for i in empdata:
           # print(i["title"])
            if(i["title"].lower().strip().count(position.strip())>=1):
                data_pos.append(i)
        return data_pos
    else:
        data_name=[]
        for i in empdata:
            print(i["name"])
            if(i["name"].lower().strip().count(name.strip())>=1):
                data_name.append(i)
        return data_name
        
@app.route("/referal-cand/<position>/<name>",methods=["GET"])
def index1(name,position):
    empdata=parse_json()
    data_ret=find_job(empdata,position,name)
    data_ret_fin=[]
   # user_data={"name":"","title":"","summary":"","url":""}
    for i in data_ret:
        user_data={"name":"","title":"","summary":"","url":""}
        user_data["name"]=i["name"]
        user_data["title"]=position
        user_data["summary"]=i["summary"]
        user_data["url"]=i["url"]
        resp=generate_profile(user_data)
        mtch=re.search(r'^\d+.\d+$',resp)
        strmtch=""
        if(mtch):
            strmtch=f"Rating: {mtch.group()}"
        res=check_positive(resp)
        strmtch+=res
        if(res.lower().count("yes") or res.lower().count("good")):
            col_pos=1
        else:
            col_pos=0
        if(strmtch.strip()==""):
            strmtch="Better you look into it more thoroughly"
        data_ret_fin.append({i["name"]:[summaryize_job(i["summary"]),i["url"],position,strmtch,col_pos,extract_linkedin_page(i["url"],position)]})
    print(data_ret_fin)
    cjs=create_job_summary(position)
    cjsres="           ".join([x for x in cjs.split(".")])
    
    return render_template("index.html",data_ret=data_ret_fin,summ=cjsres)

@app.route("/search-cand/<position>",methods=["GET"])
def index2(position):
    empdata=parse_json()
    #print(empdata)
    data_ret=find_job(empdata,position,"")
    
    data_ret_fin=[]
    for i in data_ret:
        data_ret_fin.append({i["name"]:[i["summary"],i["url"],position]})
        user_data={"name":"","title":"","summary":"","url":""}
        user_data["name"]=i["name"]
        user_data["title"]=position
        user_data["summary"]=i["summary"]
        user_data["url"]=i["url"]
        resp=generate_profile(user_data)
        mtch=re.search(r'^\d+.\d+$',resp)
        strmtch=""
        if(mtch):
            strmtch=f"Rating: {mtch.group()}"
        res=check_positive(resp)
        strmtch+=res
        if(res.lower().count("yes") or res.lower().count("good")):
            col_pos=1
        else:
            col_pos=0
        if(strmtch.strip()==""):
            strmtch="Better you look into it more thoroughly"
        data_ret_fin.append({i["name"]:[summaryize_job(i["summary"]),i["url"],position,strmtch,col_pos,extract_linkedin_page(i["url"],position)]})
    cjs=create_job_summary(position)
    cjsres="            ".join([x for x in cjs.split(".")])
    
    return render_template("index.html",data_ret=data_ret_fin,summ=cjsres)

@app.route("/experience",methods=["GET"])
def index3():
    profile_data=request.args.get("prof_data")
    i=profile_data.split(";")
    user_data={"name":"","title":"","summary":"","url":""}
    user_data["name"]=i[0]
    user_data["title"]=i[1]
    user_data["summary"]=i[2]
    user_data["url"]=i[3]
    resp=generate_profile(user_data)
    
    return render_template("experience_summ.html",data=resp)

def generate_profile(json_data)->str:
    linkedin_url=json_data["url"]
    summary=json_data["summary"]
    title=json_data["title"]
    name=json_data["name"]
    return create_summary(name,linkedin_url,summary,title)

if __name__=="__main__":
    app.run("0.0.0.0",8082,debug=False)
