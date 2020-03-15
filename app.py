from flask import Flask , request, render_template,redirect
from datetime import date
import time
import pyrebase
import requests

app = Flask(__name__)
Config = {
    "apiKey": "AIzaSyBXGNqL3GK1IPVEfaypZ91g8BPDWl-Gi5o",
    "authDomain": "iiit-kalyani-69031.firebaseapp.com",
    "databaseURL": "https://iiit-kalyani-69031.firebaseio.com",
    "projectId": "iiit-kalyani-69031",
    "storageBucket": "iiit-kalyani-69031.appspot.com",
    "messagingSenderId": "444311857308",
    "appId": "1:444311857308:web:84e2046c7debb0b9cda559",
    "measurementId": "G-T860YFH80F"
  }

firebase = pyrebase.initialize_app(Config)
db = firebase.database()  

@app.route('/')

def index():
    today=date.today()
    return render_template('base.html',today=today)

@app.route('/register')

def register():
  
  name= request.args.get("handle")

  today=date.today()

  to = db.child("Handle").get()

  Handle = to.val()

  flag=0

  for i in Handle.values():
    if name==i:

      flag=1

      break
  if flag==0: 

     db.child("Handle").push(name)

     return render_template('register.html',name=name,today=today)

  else:

    name = "Already"   

    return render_template('register.html',name=name,today=today)

@app.route('/Daily')


def daily():
  
  id = 745

  index = "C" #A.B,C,D 
  
  url = "https://codeforces.com/contest/"+str(id)+"/problem/"+index
  
  url_prob = "https://iiit-kalyani-69031.firebaseio.com/Problem.json"

  problem = requests.get(url_prob).json()

  myprob = {'id': id,'index':index}
  # print(myprob)
  if myprob not in problem.values():
    db.child("Problem").push({"id":id,"index":index})
  ''' 
  link = "https://codeforces.com/api/problemset.problems"
   
  r = requests.get(link).json()
  

  Total_problems =  r['result']['problems'][0]['contestId']

  for i in range(0,Total_problems+1):
    if i == id:
      tags = r['result']['problems'][i]['tags']
      
  print(tags)
'''
  return render_template('daily.html',url=url)


@app.route('/Previous')

def previous():

  url = "https://iiit-kalyani-69031.firebaseio.com/Problem.json"

  r = requests.get(url).json()

  problem_list =[]

  for i in r.values():

      id = i['id']

      index = i['index']

      problem_list.append("https://codeforces.com/contest/"+str(id)+"/problem/"+index)
      

  return render_template('previous.html' , problem_list=problem_list , len = len(problem_list))

if __name__ == "__main__":
    app.run(debug=True)