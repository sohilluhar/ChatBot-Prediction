import csv

from django.http import HttpResponseRedirect
from django.shortcuts import render

import diseaseprediction
count=0
sym=[]
chatrec=[]
clearchat=True

with open('templates/Testing.csv', newline='') as f:
    reader = csv.reader(f)
    symptoms = next(reader)
    symptoms = symptoms[:len(symptoms) - 1]

def clear(req):
    global chatrec
    global sym
    chatrec=[]
    sym=[]
    print('inside clear')
    return HttpResponseRedirect('/')

def addchat(req):
    if 'sym' in req.POST:
        sym.append(req.POST.get('sym'))
        global symptoms
        symptoms.remove(req.POST.get('sym'))
        ans = {
            'type': 'ans',
            'msg': req.POST.get('sym')
        }

    else:

        ans = {
            'type': 'ans',
            'msg': req.POST.get('ans')
        }

    chatrec.append(ans)

    return HttpResponseRedirect('/')

def home(req):
    predict = 'false'
    if len(chatrec)==0:
        ques1 = {
            'type': 'ques',
            'sym': 'false',
            'msg': 'Hey, I am your helper what is your name'
        }

        chatrec.append(ques1)

    if len(sym) == 5:
        name = chatrec[1]
        disease = diseaseprediction.dosomething(sym)
        ques2 = {
            'type': 'ques',
            'sym': 'false',
            'predict':'true',
            'msg': name['msg']+' You may have '+str(disease[0])
        }
        predict='true'
        chatrec.append(ques2)
    elif (len(chatrec) >= 2):


            ques2 = {
                'type': 'ques',
                'sym': 'true',
                'msg': 'Symptoms '+str(len(sym)+1)
            }
            chatrec.append(ques2)
    return render(req,'index.html',{'chat':chatrec,'symptoms':symptoms,'predict':predict})