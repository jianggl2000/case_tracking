import requests
import sys
import re
from bs4 import BeautifulSoup 

from multiprocessing import Pool
import argparse

import numpy
import datetime

def init_arg(parser):
    parser.add_argument('--start',"--my", type=int, default=2191580000, help='Start id')
    parser.add_argument('--range', "-n", type=int, default=500, help='Search range')
    parser.add_argument('--loc', type=str, default='MSC', help='Process location, default is MSC')
    parser.add_argument('--type', type=str, default='I-485', help='Petition type, default is I-485')
    parser.add_argument('--seq', action='store_true',help='Start with sequential version')
    parser.add_argument('-v', action='store_true',help='print all status')
    parser.add_argument('-verr', action='store_true',help='print all error message')
    opt = parser.parse_args()
    return vars(opt)

class USCIS(object):

    def __init__(self, parser):
        self.opt = init_arg(parser)
        
    def getstatus(self,num):
        header = {"User-Agent":"User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}
        r= requests.post('https://egov.uscis.gov/casestatus/mycasestatus.do',headers=header,data={"changeLocale":"","appReceiptNum":num,   "initCaseSearch":"CHECK STATUS"})
        try:
            s=BeautifulSoup(r.content,"lxml")
            rs = s.find('div',"current-status-sec").text
            rs = rs.replace("Your Current Status:","")
            rs = re.sub(r'[\t\n\r+]',"",rs)
            rs_info = s.find('div', "rows text-center").text
            fpfee = fptaken = trans = rej = RFIE = 0
            fpschedule = interviewReady = interviewScheduled = interviewCompleted = InterviewCanceled = 0
            approved = denied = terminated = rev = other = 0
            if client.opt['type'] in rs_info:
                if "Fingerprint Fee Was Received" in rs or "Case Was Received" in rs:
                    fpfee = 1
                elif "Fingerprints Were Taken" in rs:
                    fptaken = 1
                elif "Case Was Transferred" in rs:
                    trans = 1
                elif "Rejected" in rs:
                    rej = 1
                elif "Request for Initial Evidence" in rs:
                    RFIE = 1
                elif "xxxxx" in rs:
                    fpschedule = 1
                elif "Ready to Be Scheduled for An Interview" in rs:
                    interviewReady = 1
                elif "Interview Was Scheduled" in rs:
                    interviewScheduled = 1
                elif "Interview Was Completed" in rs:
                    interviewCompleted = 1
                elif "xxxxxxx" in rs:
                    InterviewCanceled = 1
                elif "Case Was Approved" in rs:
                    approved = 1
                elif "Denied" in rs:
                    denied = 1
                elif "Withdrawal" in rs:
                    terminated = 1
                elif "Produced" in rs or "Delivered" in rs or "Mailed To Me" in rs or "Picked" in rs:
                    rev = 1
                else:
                    other = 1
                
                if self.opt["v"]:
                    print("\t\t{}: {}".format(num,rs.strip()))
                elif other == 1:
                    print("\t\t{}: {}".format(num,rs.strip()))
            return numpy.array([fpfee, fptaken, trans, rej, RFIE, other, fpschedule, interviewReady, interviewScheduled, interviewCompleted, InterviewCanceled, approved, denied, terminated, rev])
        except Exception as e:
            if self.opt["verr"]:
                print(e)
        return 0


    def multiprocess(self,nums):
        p = Pool(10) # if this value is too big, USCIS would block your ip
        rs = p.map(self.getstatus, nums) # run multi processor version
        p.terminate()
        p.join()
        rec = numpy.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        for v in rs:
            rec += v
        print(f"\nReceived: {rec[0]}; Fingerprinted: {rec[1]}; Transferred: {rec[2]}; Rejected: {rec[3]}; RFIE: {rec[4]}; Others: {rec[5]}; Total: {sum(rec)}/{client.opt['range']} ")
        Log.write(f"Received: {rec[0]}; Fingerprinted: {rec[1]}; Transferred: {rec[2]}; Rejected: {rec[3]}; RFIE: {rec[4]}; Others: {rec[5]}; Total: {sum(rec)}/{client.opt['range']} ")
        if sum(rec[7:])>0:
            print(f"Interview Ready: {rec[7]}; interview Scheduled: {rec[8]}; interview Completed: {rec[9]}; Interview Canceled: {rec[10]} ")
            print(f"approved: {rec[11]}; denied: {rec[12]}; terminated: {rec[13]}; Delivered: {rec[14]}\n")
            Log.write(f"Interview Ready: {rec[7]}; interview Scheduled: {rec[8]}; interview Completed: {rec[9]}; Interview Canceled: {rec[10]} ")
            Log.write(f"approved: {rec[11]}; denied: {rec[12]}; terminated: {rec[13]}; Delivered: {rec[14]}\n")
        else:
            print("\n")
            Log.write("\n")
    
    def sequential(self,nums):
        rec = numpy.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        for i in nums:
            rs = self.getstatus(i)
            rec += rs
        print(f"\nReceived: {rec[0]}; Fingerprinted: {rec[1]}; Transferred: {rec[2]}; Rejected: {rec[3]}; RFIE: {rec[4]}; Others: {rec[5]}; Total: {sum(rec)}/{client.opt['range']}")
        Log.write(f"Received: {rec[0]}; Fingerprinted: {rec[1]}; Transferred: {rec[2]}; Rejected: {rec[3]}; RFIE: {rec[4]}; Others: {rec[5]}; Total: {sum(rec)}/{client.opt['range']} ")
        if sum(rec[7:]) > 0:
            print(f"Interview Ready: {rec[7]}; interview Scheduled: {rec[8]}; interview Completed: {rec[9]}; Interview Canceled: {rec[10]}")
            print(f"approved: {rec[11]}; denied: {rec[12]}; terminated: {rec[13]}; Delivered: {rec[14]}\n")
            Log.write(f"Interview Ready: {rec[7]}; interview Scheduled: {rec[8]}; interview Completed: {rec[9]}; Interview Canceled: {rec[10]} ")
            Log.write(f"Approved: {rec[11]}; denied: {rec[12]}; terminated: {rec[13]}; Delivered: {rec[14]}\n")
        else:
            print("\n")
            Log.write("\n")

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    client = USCIS(args)
    
    CurTime = "\t\t#################### "+ datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")+ " # "+ client.opt['type'] +" # "+ client.opt['loc'] + str(client.opt['start']) +" ####################\n"
    Log = open("log."+ client.opt['type'] +".txt","a")
    Log.write(CurTime)
    
    print(f"Search {client.opt['range']} cases BEFORE {client.opt['loc']}{client.opt['start']}, ", end='')
    search_list = []
    for i in range(client.opt["range"]):
        search_item = f"{client.opt['loc']}{client.opt['start']-client.opt['range']+i}"
        search_list.append(search_item)
    print(f"from {search_list[0]} to {search_list[-1]}, for {client.opt['type']}")
    if client.opt["seq"]:
        client.sequential(search_list)
    else:
        client.multiprocess(search_list)
        
    print(f"Search for {client.opt['range']} cases AFTER {client.opt['loc']}{client.opt['start']}, ", end='')
    search_list = []
    for i in range(client.opt["range"]):
        search_item = f"{client.opt['loc']}{client.opt['start']+i}"
        search_list.append(search_item)
    print(f"from {search_list[0]} to {search_list[-1]}, for I485")
    if client.opt["seq"]:
        client.sequential(search_list)
    else:
        client.multiprocess(search_list)
    
    Log.close()
