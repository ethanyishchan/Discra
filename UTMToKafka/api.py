from urllib2 import Request, urlopen, URLError,base64
import ssl
import urllib
import requests
import sched, time
import json
import sys
import datetime

airports_url = 'https://tmiserver.arc.nasa.gov/api/v0/airports'
ops_url = 'https://tmiserver.arc.nasa.gov/api/v0/operations'
pos_url = 'https://tmiserver.arc.nasa.gov/api/v0/positions'
msg_url = 'https://tmiserver.arc.nasa.gov/api/v0/messages'


def initAuth(req):
    pass

def getPositions(gufi, limit=9999):
    '''
    Gets the position for a particular flight

    Inputs:
    - gufi: string representing the global flight identifier for the particular drone flight
    - limit: number of positions we want to receive from the call

    Outputs:
    - response: from the UTM server
    '''
    username  = "stanford"
    password = "KarNeva1!"
    gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1) 
    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')

    request = Request(pos_url + '/' + gufi + '?limit='+str(limit))
    request.add_header("Authorization", "Basic %s" % base64string)
    response = urlopen(request, context=gcontext).read()
    return response

def postPosition(pos_file):
    username  = "stanford"
    password = "KarNeva1!"
    gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1) 
    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    pos_plan_json = json.loads(open(pos_file, 'r').read())
    #print type(pos_plan_json)
    pos_plan_json['speed'] = 20
    #pos_plan_json['longitude'] = -121.436098184554
    #pos_plan_json['location'] = '{\"type\"Point\"'
    #print pos_plan_json
    # cafile = "NASA.cer"
    # r = requests.post(ops_url, verify=False, json= op_plan_json, auth={username, password})
    r = requests.post(pos_url, verify=False,json= pos_plan_json,auth=(username, password))
    print r.status_code
    return r.json()


def postOperation(oper_file):
    username  = "stanford"
    password = "KarNeva1!"
    gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1) 
    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    op_plan_json = json.loads(open(oper_file, 'r').read())
    # cafile = "NASA.cer"
    # r = requests.post(ops_url, verify=False, json= op_plan_json, auth={username, password})
    r = requests.post(ops_url, verify=False,json= op_plan_json,auth=(username, password))
    print r.status_code
    return r.json()
    # print r.response()

def getMessages():  
    username  = "stanford"
    password = "KarNeva1!"
    gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1) 
    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')

    request = Request(msg_url)
    request.add_header("Authorization", "Basic %s" % base64string)
    response = urlopen(request, context=gcontext).read()
    return response

def postMessage(msg_file):
    username  = "stanford"
    password = "KarNeva1!"
    gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1) 
    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    msg_plan_json = json.loads(open(msg_file, 'r').read())
    r = requests.post(msg_url, verify=False,json= msg_plan_json,auth=(username, password))
    print r.status_code
    return r.json()

#print getPositions('88fca443-5722-410f-ae3e-444a18480892') #original
#print getPositions('9ed438d6-20ad-4b4b-b52c-c3ef9d8ac973', 1000) #new
#print getPositions('15b21b39-c2fe-4044-862d-39ab7e39858f', 1000) #hardcoded
#print getMessages()
#print postMessage('test_message.json')
#print postOperation('test_flight_1.json')

def postPositionsForever():
    s = sched.scheduler(time.time, time.sleep)
    def do_something(sc): 
        print "Doing stuff..."
        print postPosition('positions.json')
        #print postPosition('positions copy.json')
        sc.enter(5, 1, do_something, (sc,))

    s.enter(1, 1, do_something, (s,))
    s.run()

if __name__ == '__main__':
    #print postOperation('test_flight_1.json')
    #asys.exit()
    postPositionsForever()
    pos = getPositions('0814aad1-8b3f-4a85-a31c-b9809f562aa7', 10000)
    print pos
    sys.exit()
    pos = getPositions('3d64802e-97d5-444c-ac21-d1a5decb69dd', 10000)
    print pos
    pos = getPositions('fc7df749-a26f-426c-ac6c-25f1c98ca399', 10000)
    print pos