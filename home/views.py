from django.contrib.auth.models import User, auth
from django.contrib import messages
import pandas as pd
import csv
import os
import datetime
from .predict import prod
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse
from django.views.decorators.csrf import csrf_exempt
import home.models as homeling
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import *
from twilio.rest import Client as Clientelle
from twilio.twiml.messaging_response import MessagingResponse
import requests
import json
from django.templatetags.static import static
import base64
from heyoo import WhatsApp
from joblib import dump, load
import numpy as np
# Create your views here.

account_sid = 'ACe5b4d5166816d11c745a003dd9a282b6'
auth_token = 'ba5ba937994122f7017ff2fd6350d79f'
clientelle = Clientelle(account_sid, auth_token)

messenger = WhatsApp('EAAW9q4zCEWMBAFSuq3ce5pEq0KDoKnn0oWqSDUExH6oJIcoPISEZCD1QakT87RljU1BZASMhggXXOkTigdaAuS5NcvOzJmSyrZAZBqd4p862O2BL6puMWuxoHZCFvv8AzmzXfqyZClzNw1PotbX0NyZAnZAHCMXyljMRrjZABggwFv8XZACQOErZB6VJo0nfThgZAvIDWFqx1qztRNsxjFSWeU3Ko5YAY03hwC8ZD',  phone_number_id='109461665230077')

VERIFY_TOKEN = "23189345712"

head = {'Authorization' : 'Bearer EAAW9q4zCEWMBAFSuq3ce5pEq0KDoKnn0oWqSDUExH6oJIcoPISEZCD1QakT87RljU1BZASMhggXXOkTigdaAuS5NcvOzJmSyrZAZBqd4p862O2BL6puMWuxoHZCFvv8AzmzXfqyZClzNw1PotbX0NyZAnZAHCMXyljMRrjZABggwFv8XZACQOErZB6VJo0nfThgZAvIDWFqx1qztRNsxjFSWeU3Ko5YAY03hwC8ZD'}

def call():
    cally = clientelle.calls.create(
                        twiml='<Response><Say>Please Check the platform there is a client who is in distress!</Say></Response>',
                        to='+263784873574',
                        from_='+18154966506'
                    )

    print(cally.sid)

def home(request):
    clients = Client.objects.all()
    for cli in clients:
        if Animal.objects.all().filter(user=cli.user):
            Animal.objects.all().filter(user=cli.user).update(book=cli.book)





    return render(request, 'Medilab/index.html')

def admin(request):
    return redirect('admin/')

def logout(request):
	
	auth.logout(request)
	
	return redirect('login')

def appointment_reg(request):
    user = request.user
    animals = Animal.objects.all().filter(user=user)
    context = {'animals': animals, 'user': user}
    return render(request, 'Medilab/logs/appointments.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
           
                auth.login(request, user)
                return redirect('appointment')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('login')
    else:
        return render(request, 'Medilab/pages-login.html')

def meetTest(request, meetID):
    attempted_user = request.user
    booking = Appointment.objects.get(pk=meetID)
    context = {'booking': booking.id, 'attempted_user': attempted_user}
    return render(request, 'Medilab/logs/meetroom.html', context)

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        location = request.POST['location']
        phone = request.POST['phone']
        email_address = request.POST['email_address']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email_address).exists():
                messages.info(request, 'Email Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email_address, first_name=first_name, last_name=last_name, is_staff=False)
                user.save();
                client = Client.objects.create(user=user, location=location, phone=phone)
                client.save();
                return redirect('login')
    else:
        return render(request, 'Medilab/pages-register.html')

def treatment(request):
    if request.method == 'POST':
        name = request.POST['name']
        cost = request.POST['cost']

        treat = Treatment.objects.create(name=name, cost=cost)
        treat.save();

    else:
        treats = Treatment.objects.all().filter(user=request.user)
        context = {'treats': treats, 'user': user}
        return render(request, 'Medilab/logs/treatmentsReg.html', context)


def receipt(request):

    user = request.user

    receipts = Sales.objects.all().filter(user=request.user, paid=True)

    context = {'receipts': receipts, 'user': user}

    return render(request, 'Medilab/logs/salesView.html', context)

def invoice(request):

    if request.method == 'POST':

        saleID = request.POST['saleID']

        sale = Sales.objects.get(id=saleID)

        sale.paid = True

        sale.save()

        user = request.user

        invoices = Sales.objects.all().filter(user=request.user, paid=False)

        messages.info(request, 'Paid Successfully!!!')

        context = {'invoices': invoices, 'user': user}

        return render(request, 'Medilab/logs/invoicesView.html', context)


    user = request.user

    invoices = Sales.objects.all().filter(user=request.user, paid=False)

    context = {'invoices': invoices, 'user': user}

    return render(request, 'Medilab/logs/invoicesView.html', context)


def appointment(request):
    if request.method == 'POST':
        message = request.POST['message']
        animal = request.POST['animal']
        date =  request.POST['date']   

        animal = Animal.objects.get(tag=animal)

        doctor = Doctor.objects.get(speciality=animal.breed)

        doctor = Client.objects.get(user=doctor.user)



        user = request.user
        book = Appointment.objects.create(message=message, animal=animal, date=date, user=user, doctorphone=doctor.phone)
        animal.save();
        user.save();
        user = request.user
        appointments = Appointment.objects.all().filter(user=user)
        context = {'appointments': appointments, 'user': user, 'doctor': doctor}
        return render(request, 'Medilab/logs/appointmentView.html', context)

    else:
            cli = Client.objects.get(user=request.user)
            if cli.clientType == "Farmer":


                user = request.user
                appointments = Appointment.objects.all().filter(user=user)
                context = {'appointments': appointments, 'user': user}
                return render(request, 'Medilab/logs/appointmentView.html', context)
            if cli.clientType == "Officer":

                user = request.user
                appointments = Appointment.objects.all()
                context = {'appointments': appointments, 'user': user}
                return render(request, 'Medilab/logs/appointmentViewAdmin.html', context)
            
            if cli.clientType == "Doctor":

                user = request.user
                appointments = Appointment.objects.all()
                context = {'appointments': appointments, 'user': user}
                return render(request, 'Medilab/logs/appointmentViewAdmin.html', context)

def calling(request):
    call()
    return render(request, 'Medilab/logs/Calling.html')


def appointmentAdmin(request):
    if request.method == 'POST':
        tag = request.POST['id']

        if Appointment.objects.get_or_create(animal=tag):
            status = request.POST['status']
            book = Appointment.objects.update_or_create(animal=tag, status=status)
            book.save()

    else:
        animal = Appointment.objects.all()
        animal = {'treats': treats, 'user': user}
        return render(request, 'Medilab/logs/appointments_admin.html', context)

def sales(request):
    if request.method == 'POST':
        user = request.POST['user']
        treatment = request.POST['treatment']  

        sale = Sales.objects.create(user=user, treatment=treatment)
        sale.save();

    else:
        animal = Sales.objects.all()
        animal = {'treats': treats, 'user': user}
        return render(request, 'Medilab/logs/sales.html', context)

def salesAdmin(request):
    if request.method == 'POST':
        user = request.POST['user']
        treatment = request.POST['treatment']  
        status = request.POST['status']  

        sale = Sales.objects.create(user=user, treatment=treatment, status=status)
        sale.save();

    else:
        animal = Sales.objects.all()
        animal = {'treats': treats, 'user': user}
        return render(request, 'Medilab/logs/sales_admin.html', context)

def prediction(request):
    save_path = "saved_model/"
    model_name = "model"

    if request.method == 'POST':
        Age = request.POST['age']
        SystolicBP = request.POST['systolicBP']
        DiastolicBP = request.POST['diastolicBP']
        bs = request.POST['BS']
        bodytemp = request.POST['BodyTemp']

        report = Report.objects.create( user = request.user, age = Age, systolicBP = SystolicBP, diastolicBP = DiastolicBP, bs =bs, bodytemp = bodytemp)
        report.save();

        patientSympts = [Age, SystolicBP, DiastolicBP, bs, bodytemp]
        patientSympts = np.array([patientSympts])
        print(patientSympts)
        result = ""

        try:
            # Load Trained Model
            GDRAT_abs_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), str(save_path + model_name + ".joblib"))
            clf = load(str(GDRAT_abs_path))
            result = clf.predict(patientSympts)
            print(result)
            
        except Exception as e:
            print(e)
            result = e

        suggestion = "Please click the button below to make a call, so that the doctors will respond to you shortly"

        if result == ['low']:
            suggestion ="Your symptoms shows you are at low risk, you can request for a call if you are in need for further assistance"
        
        context = {'result': result, 'suggestion' : suggestion}
        return render(request, 'Medilab/logs/diseases_predict.html', context)
    else:

        return render(request, 'Medilab/logs/diseases_predict.html')
 

class HelloView(APIView):

    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        print(incoming_message)


        sms(request)



        return HttpResponse()


@csrf_exempt
def sms(request):
    if request.method == 'POST':

        incoming_message = json.loads(request.body.decode('utf-8'))

        profile = ""
        print(incoming_message)
        print("the_incoming_message")
        income = incoming_message['entry']
        entry = income[-1]
        for message in entry['changes']:
            valu = message['value']

            if 'messages' in valu:

                for contactlist in valu['contacts']:

                    number = contactlist['wa_id']

                    profile = contactlist['profile']['name']

                for messag in valu['messages']:

                    if messag['type'] == 'text':

                        msg = messag['text']['body']





                        msgid = messag['id']

                        datobj = {
                                  "messaging_product": "whatsapp",
                                  "status": "read",
                                  "message_id": msgid
                                }

                        respo = requests.post('https://graph.facebook.com/v15.0/103807519292715/messages', json = datobj, headers = {'Authorization' : 'Bearer EAARIezJjAOUBANzxdBA84grisZCjFR73zgzMufMMNGgo8elnmJc9ZBZCjGCZBB9v1axZCi88vmu5FerAugos1hPNimQ5HsZAgPRcJXZBXZBnDj1zOUh9hjHjMMKV08o753C4kEft6LZA5h7F8OTMHv72PRosfroHRdgaUY43qZA6ISeqmZAaLK2EmRZBZCdY7AN2V2IiFsSJRpAglkZADkeGsUs2OKXT1ZBp3iUWZCwZD'} )

                        print(respo.text)



                        tabol(number, msg, profile)

                    if messag['type'] == 'image':

                        msg = messag['image']['caption']

                        msgid = messag['id']

                        media_id = messag['image']['id']

                        datobj = {
                                  "messaging_product": "whatsapp",
                                  "status": "read",
                                  "message_id": msgid
                                }

                        respo = requests.post('https://graph.facebook.com/v15.0/103807519292715/messages', json = datobj, headers = {'Authorization' : 'Bearer EAARIezJjAOUBANzxdBA84grisZCjFR73zgzMufMMNGgo8elnmJc9ZBZCjGCZBB9v1axZCi88vmu5FerAugos1hPNimQ5HsZAgPRcJXZBXZBnDj1zOUh9hjHjMMKV08o753C4kEft6LZA5h7F8OTMHv72PRosfroHRdgaUY43qZA6ISeqmZAaLK2EmRZBZCdY7AN2V2IiFsSJRpAglkZADkeGsUs2OKXT1ZBp3iUWZCwZD'} )

                        print(respo.text)

                        r = requests.get(f"https://graph.facebook.com/v14.0/{media_id}", headers=head)

                        print(r.json()["url"])


                        media_url = r.json()["url"]

                        r = requests.get(media_url, headers=head)

                        print(r)

                        img = r.content

                        #tabol(number, msg, profile, media_url)

                    if messag['type'] == 'interactive':

                        msgid = messag['id']

                        if messag['interactive']['type'] == 'list_reply':

                            msg = messag['interactive']['list_reply']['id']



                            datobj = {
                                  "messaging_product": "whatsapp",
                                  "status": "read",
                                  "message_id": msgid
                                }

                            respo = requests.post('https://graph.facebook.com/v15.0/103807519292715/messages', json = datobj, headers = {'Authorization' : 'Bearer EAARIezJjAOUBANzxdBA84grisZCjFR73zgzMufMMNGgo8elnmJc9ZBZCjGCZBB9v1axZCi88vmu5FerAugos1hPNimQ5HsZAgPRcJXZBXZBnDj1zOUh9hjHjMMKV08o753C4kEft6LZA5h7F8OTMHv72PRosfroHRdgaUY43qZA6ISeqmZAaLK2EmRZBZCdY7AN2V2IiFsSJRpAglkZADkeGsUs2OKXT1ZBp3iUWZCwZD'} )

                            print(respo.text)

                            tabol(number, msg, profile)
                        if messag['interactive']['type'] == 'button_reply':

                            msg = messag['interactive']['button_reply']['id']



                            datobj = {
                                  "messaging_product": "whatsapp",
                                  "status": "read",
                                  "message_id": msgid
                                }

                            respo = requests.post('https://graph.facebook.com/v15.0/103807519292715/messages', json = datobj, headers = {'Authorization' : 'Bearer EAARIezJjAOUBANzxdBA84grisZCjFR73zgzMufMMNGgo8elnmJc9ZBZCjGCZBB9v1axZCi88vmu5FerAugos1hPNimQ5HsZAgPRcJXZBXZBnDj1zOUh9hjHjMMKV08o753C4kEft6LZA5h7F8OTMHv72PRosfroHRdgaUY43qZA6ISeqmZAaLK2EmRZBZCdY7AN2V2IiFsSJRpAglkZADkeGsUs2OKXT1ZBp3iUWZCwZD'} )

                            print(respo.text)

                            tabol(number, msg, profile)


def tabol(number, mesg, profile, media=None):

    print("now here now")



    main = ("HI *"+ str(profile)+"* \n\nWelcome to Smart Lives Services CHATBOT \n\n"
        "Below is our main menu NB: Click the links below each category or section to get access to that section's menu \n\n ")

    watnum = number[3:]
    print(watnum)
    msg = mesg

    watnum = "0" + watnum

    print(watnum)

    member = Client.objects.filter(phone=watnum).first()



    print(member.phone)

    careerg = "careerguide"

    print(msg)
    msg = msg.lower()

    if str(msg) == "hi":

        if member is not None :


            print("Check Now")

            #respons = messenger.send_image(image="https://i.imgur.com/Fh7XVYY.jpeg", recipient_id=number,)
            #print(respons)

            datobj = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": number,
                "type": "interactive",
                "interactive": {
                    "type": "list",
                    "body": {
                    "text": main
                    },
                    "footer": {
                    "text": "Visit wenextafrica.org"
                    },
                    "action": {
                    "button": "Responces",
                    "sections": [
                        {
                        "title": "Menu",
                        "rows": [
                            {
                            "id": "animalis",
                            "title": "Animals",
                            "description": "Get access to your animal listings"
                            },
                            {
                            "id": "appointair",
                            "title": "Appointments",
                            "description": "View or Book appointments with the veterinary"
                            },
                            {
                            "id": "reciptair",
                            "title": "Receipts",
                            "description": "View all the receipts"
                            },
                            {
                            "id": "subscriptsair",
                            "title": "Subscriptions",
                            "description": "View all the subscriptions you have made"
                            }
                        ]
                        },

                    ]
                    }
                }
                }




            respo = requests.post('https://graph.facebook.com/v15.0/103807519292715/messages', json = datobj, headers = {'Authorization' : 'Bearer EAARIezJjAOUBANzxdBA84grisZCjFR73zgzMufMMNGgo8elnmJc9ZBZCjGCZBB9v1axZCi88vmu5FerAugos1hPNimQ5HsZAgPRcJXZBXZBnDj1zOUh9hjHjMMKV08o753C4kEft6LZA5h7F8OTMHv72PRosfroHRdgaUY43qZA6ISeqmZAaLK2EmRZBZCdY7AN2V2IiFsSJRpAglkZADkeGsUs2OKXT1ZBp3iUWZCwZD'} )

            print(respo.text)

        else:

            #Change to default

            datobj = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": number,
                "type": "interactive",
                "interactive": {
                    "type": "list",
                    "body": {
                    "text": main
                    },
                    "footer": {
                    "text": "Visit wenextafrica.org"
                    },
                    "action": {
                    "button": "Responces",
                    "sections": [
                        {
                        "title": "Menu",
                        "rows": [
                            {
                            "id": "animalis",
                            "title": "Animals",
                            "description": "Get access to your animal listings"
                            },
                            {
                            "id": "appointair",
                            "title": "Appointments",
                            "description": "View or Book appointments with the veterinary"
                            },
                            {
                            "id": "reciptair",
                            "title": "Receipts",
                            "description": "View all the receipts"
                            },
                            {
                            "id": "subscriptsair",
                            "title": "Subscriptions",
                            "description": "View all the subscriptions you have made"
                            }
                        ]
                        },

                    ]
                    }
                }
                }



            respo = requests.post('https://graph.facebook.com/v15.0/103807519292715/messages', json = datobj, headers = {'Authorization' : 'Bearer EAANvXaI9edsBAOfN0KKiZC03CHV6t3JpafoAn2aL8wBQIgaaaHEmZBnCK1T2MQvrkShGbQ9T0GiPdQHN1lcxBvq5TQmYc7ZAtHT1SIVDOANYPfsK3Sw9OXohSZBBZAQvt9mS3KRd0w1a1dMB6dIlvsUhj0W1hIwOtt6FC78I4tyhZCZAiYWSGCXQeVzL07f44sZB1n6ZC6j5moQZDZD'} )

            print(respo.text)

    if "age=" in str(msg):
        msgstop = 0
        msgstart = msg.index("age=", msgstop)
        msgstop = msg.index(",", msgstart)
        msgRealStart = msgstart + 4
        msgRealStop = msgstop - 1
        age = msg[msgRealStart:msgRealStop]

        print(age)

        msgsyststop = 0
        msgsyststart = msg.index("systolicbp=", msgsyststop)
        msgsyststop = msg.index(",", msgsyststart)
        msgRealStart = msgsyststart + 11
        msgRealStop = msgsyststop - 1
        systolicbp = msg[msgRealStart:msgRealStop]

        print(systolicbp)

        msgdiaststop = 0
        msgdiaststart = msg.index("diastolicbp=", msgdiaststop)
        msgdiaststop = msg.index(",", msgdiaststart)
        msgRealStart = msgdiaststart + 12
        msgRealStop = msgdiaststop - 1
        diastolicbp = msg[msgRealStart:msgRealStop]

        print(diastolicbp)

        msgbsstop = 0
        msgbsstart = msg.index("bs=", msgbsstop)
        msgbsstop = msg.index(",", msgbsstart)
        msgRealStart = msgbsstart + 3
        msgRealStop = msgbsstop - 1
        bs = msg[msgRealStart:msgRealStop]

        print(bs)

        msgbodytempstop = 0
        msgbodytempstart = msg.index("bodytemp=", msgbodytempstop)
        msgbodytempstop = msg.index(",", msgbodytempstart)
        msgRealStart = msgbodytempstart + 3
        msgRealStop = msgbodytempstop - 1
        bodytemp = msg[msgRealStart:msgRealStop]

        print(bodytemp)

        report = Report.objects.create( user = member.user, age = age, systolicBP = systolicbp, diastolicBP = diastolicbp, bs =bs, bodytemp = bodytemp)
        report.save();

        patientSympts = [age, systolicbp, diastolicbp, bs, bodytemp]
        patientSympts = np.array([patientSympts])
        print(patientSympts)
        result = ""

        try:
            # Load Trained Model
            GDRAT_abs_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), str(save_path + model_name + ".joblib"))
            clf = load(str(GDRAT_abs_path))
            result = clf.predict(patientSympts)
            print(result)
            
        except Exception as e:
            print(e)
            result = e

        suggestion = "It seems like you are not feeling well please press the below button to request for a call"

        if result == ['low']:
            suggestion ="It seems you are not feeling well please press the button below to reach out to our doctors"

        datobj = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": number,
                "type": "interactive",
                "interactive": {
                    "type": "button",
                    "body": {
                    "text": suggestion
                    },
                    "footer": {
                    "text": "Visit wenextafrica.org"
                    },
                    "action": {
                    "buttons": [
                            {
                            "type": "reply",
                            "reply": {
                                "id": "calling",
                                "title": "Call"
                            }
                            }
                        ]
                    }
                }
                }        

        respo = requests.post('https://graph.facebook.com/v15.0/103807519292715/messages', json = datobj, headers = {'Authorization' : 'Bearer EAARIezJjAOUBANzxdBA84grisZCjFR73zgzMufMMNGgo8elnmJc9ZBZCjGCZBB9v1axZCi88vmu5FerAugos1hPNimQ5HsZAgPRcJXZBXZBnDj1zOUh9hjHjMMKV08o753C4kEft6LZA5h7F8OTMHv72PRosfroHRdgaUY43qZA6ISeqmZAaLK2EmRZBZCdY7AN2V2IiFsSJRpAglkZADkeGsUs2OKXT1ZBp3iUWZCwZD'} )

        print(respo.text)

    if str(msg) == "calling":

        call()

        firstinfo = "call successfully requested, the doctor will call you soon\n\n "

        datobj = {
              "messaging_product": "whatsapp",
              "recipient_type": "individual",
              "to": number,
              "type": "text",
              "text": {
                  "body": firstinfo
              }
              }

        respo = requests.post('https://graph.facebook.com/v15.0/103807519292715/messages', json = datobj, headers = {'Authorization' : 'Bearer EAARIezJjAOUBANzxdBA84grisZCjFR73zgzMufMMNGgo8elnmJc9ZBZCjGCZBB9v1axZCi88vmu5FerAugos1hPNimQ5HsZAgPRcJXZBXZBnDj1zOUh9hjHjMMKV08o753C4kEft6LZA5h7F8OTMHv72PRosfroHRdgaUY43qZA6ISeqmZAaLK2EmRZBZCdY7AN2V2IiFsSJRpAglkZADkeGsUs2OKXT1ZBp3iUWZCwZD'} )

        print(respo.text)



    if str(msg) == "animalis":

        animals = Animal.objects.all().filter(user=member.user)

        firstinfo = "View the listing of all the cattle you have registered \n\n "


        for animaly in animals:

            animalsingle= "Tag: "+ str(animaly.tag) + "," + "\n BREED: "+ animaly.breed   + "\n Sex: "+ animaly.sex  + "\n Weight: "+ str(animaly.weight)  + "\n Years: "+ animaly.years  + " \n\n"

            firstinfo = firstinfo + animalsingle



        datobj = {
              "messaging_product": "whatsapp",
              "recipient_type": "individual",
              "to": number,
              "type": "text",
              "text": {
                  "body": firstinfo
              }
              }

        respo = requests.post('https://graph.facebook.com/v15.0/103807519292715/messages', json = datobj, headers = {'Authorization' : 'Bearer EAARIezJjAOUBANzxdBA84grisZCjFR73zgzMufMMNGgo8elnmJc9ZBZCjGCZBB9v1axZCi88vmu5FerAugos1hPNimQ5HsZAgPRcJXZBXZBnDj1zOUh9hjHjMMKV08o753C4kEft6LZA5h7F8OTMHv72PRosfroHRdgaUY43qZA6ISeqmZAaLK2EmRZBZCdY7AN2V2IiFsSJRpAglkZADkeGsUs2OKXT1ZBp3iUWZCwZD'} )

        print(respo.text)

    if str(msg) == "appointair":

        appointments = Appointment.objects.all().filter(user=member.user)

        firstinfo = "View the listing of all the appointments you have booked with veterinary \n\n "

        for appointee in appointments:

            stat = ""

            if appointee.status == 1:
                stat = "approved"
            else:
                stat = "pending"

            appoinmentsingle= "Date: " + appointee.date + "\n Message: "+ appointee.message + "," + "\n Status: "+ stat   + " \n\n"

            firstinfo = firstinfo + appoinmentsingle



        datobj = {
              "messaging_product": "whatsapp",
              "recipient_type": "individual",
              "to": number,
              "type": "text",
              "text": {
                  "body": firstinfo
              }
              }

        respo = requests.post('https://graph.facebook.com/v15.0/103807519292715/messages', json = datobj, headers = {'Authorization' : 'Bearer EAARIezJjAOUBANzxdBA84grisZCjFR73zgzMufMMNGgo8elnmJc9ZBZCjGCZBB9v1axZCi88vmu5FerAugos1hPNimQ5HsZAgPRcJXZBXZBnDj1zOUh9hjHjMMKV08o753C4kEft6LZA5h7F8OTMHv72PRosfroHRdgaUY43qZA6ISeqmZAaLK2EmRZBZCdY7AN2V2IiFsSJRpAglkZADkeGsUs2OKXT1ZBp3iUWZCwZD'} )

        print(respo.text)


    if str(msg) == "reciptair":
        receipts = Sales.objects.all().filter(user=member.user, paid=True)

        firstinfo = "View the listing of all the receipts \n\n "

        for receiptee in receipts:

            receiptsingle= "Animal Tag: " + str(receiptee.animal.tag) + "\n Date: "+ receiptee.date + "," + "\n Description: "+ receiptee.description   + "\n Treatment Name: " + receiptee.treatment.name   + "\n Cost: "+ str(receiptee.treatment.cost)  + " \n\n"

            firstinfo = firstinfo + receiptsingle



        datobj = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "text",
            "text": {
                "body": firstinfo
            }
            }

        respo = requests.post('https://graph.facebook.com/v15.0/103807519292715/messages', json = datobj, headers = {'Authorization' : 'Bearer EAARIezJjAOUBANzxdBA84grisZCjFR73zgzMufMMNGgo8elnmJc9ZBZCjGCZBB9v1axZCi88vmu5FerAugos1hPNimQ5HsZAgPRcJXZBXZBnDj1zOUh9hjHjMMKV08o753C4kEft6LZA5h7F8OTMHv72PRosfroHRdgaUY43qZA6ISeqmZAaLK2EmRZBZCdY7AN2V2IiFsSJRpAglkZADkeGsUs2OKXT1ZBp3iUWZCwZD'} )

        print(respo.text)

        