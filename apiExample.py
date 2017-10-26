# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 17:48:39 2015

@author: wge
"""
import urllib.request
import json
import datetime

from pprint import pprint
   
    
class GovernmentAPI_Struct():
    def __init__(self, userID, agency):
        now = datetime.datetime.now()        
        self.currentyr = str(now.year)
        self.id = userID        
        if agency=='BEA':
            self.location = "www.bea.gov/api/data/"   
        elif agency=='BLS':
            self.location = "www.bea.gov/api/data/"  
        elif agency=='FED':
            self.location = "www.bea.gov/api/data/"  
        elif agency=='BEA':
            self.location = "www.bea.gov/api/data/"  
        else:
            print("not a known agency")
    
    @staticmethod    
    def __getTopKey(mydict):     
        if isinstance(mydict,dict):
            for key, value in mydict.items():
                return(str(key))               
        else:
            return("")

    @staticmethod        
    def __getAllKeys(mydict):
        mykeys=list()
        if isinstance(mydict,dict):
            for key, value in mydict.items():
                mykeys.append(str(key))              
        return(mykeys)
    
    @staticmethod 
    def __getPara(requestArray,mykey):
        for req in requestArray:
            if req['ParameterName']==mykey:
                return req['ParameterValue']
            #elif req['ParameterName']=='DATASETNAME':
            #    quiry.dataset = req['ParameterValue']
    
    def getReturnData(self,requestResults=None):
        if requestResults==None:
            requestResults=self.requestResults
        requestArray = requestResults['Data']
        outList = {}        
        for req in requestArray:
            outList[req['LineDescription']] = req['DataValue']
        pprint(outList)
        print()
        return outList
        
    def getDatum(self,lineDescription,requestResults=None):
        if requestResults==None:
            requestResults=self.requestResults
        dimensionArray = requestResults['Dimensions']
        dimTuple = ()
        for dim in dimensionArray:
            dimTuple = dimTuple + (dim['Name'],)
        dataArray = requestResults['Data']
        outList = [dimTuple]
        for theData in dataArray:
            metaDataTuple=()
            for dim in dimTuple:
                metaDataTuple = metaDataTuple + (theData[dim],)
            outList.append(metaDataTuple)
        
        pprint(outList)
        print()
        return outList
        
    def getByCode(self, seriesCode, requestResults=None):
        if requestResults==None:
            requestResults=self.requestResults
        requestArray = requestResults['Data']
        for req in requestArray:
            if req['SeriesCode'] == seriesCode:
                print(""+str(req['LineDescription'])+": "+str(req['DataValue']))
                return req['DataValue']            
    
    def getMetaData(self,requestResults=None):
        if requestResults==None:
            requestResults=self.requestResults
        dimensionArray = requestResults['Dimensions']
        dimTuple = ()
        for dim in dimensionArray:
            dimTuple = dimTuple + (dim['Name'],)
        dataArray = requestResults['Data']
        outList = [dimTuple]
        for theData in dataArray:
            metaDataTuple=()
            for dim in dimTuple:
                metaDataTuple = metaDataTuple + (theData[dim],)
            outList.append(metaDataTuple)
        pprint(outList)
        print()
        return outList            
            
    def reportRequest(self):
        print("Requested Method: " + self.__getPara(self.agencyRequest,'METHOD'))
        print("Requested Dataset: " + self.__getPara(self.agencyRequest,'DATASETNAME'))
        print("Requested Year: " + self.__getPara(self.agencyRequest,'YEAR'))
        print("Requested Table: " + self.__getPara(self.agencyRequest,'TABLEID'))
        print("Requested Frequency: " + self.__getPara(self.agencyRequest,'FREQUENCY'))
        print()        
    
    def __getURL(self, instruction):
        apiRequest = 'http://' + self.location + '?&UserID=' + self.id +'&' 
        for command in instruction:
            apiRequest = apiRequest + str(command[0]) + '=' + str(command[1]) + '&'

        #Request                
        response = urllib.request.urlopen(apiRequest)        
        myjson=json.loads(response.read().decode('utf-8'))
        agency = self.__getTopKey(myjson)
        returnObject=myjson[agency]
        return returnObject
            
    def requestData(self, dataset="NIPA",tableID="1",year=None, frequency="A"):
        if year==None:
            year=int(self.currentyr)-1
        instruction = [("METHOD","GetData")]   
        instruction.append(("DatasetName",dataset))
        instruction.append(("TableID",tableID))
        instruction.append(("Frequency",frequency))
        instruction.append(("Year",str(year)))
        #print(instruction)

        #Request procedure        
        returnObject=self.__getURL(instruction)
        agency_request = returnObject['Request']
        self.requestResults = returnObject['Results']
        #print("Requested: " + str(agency_request) + "\n\n")
        #print("Returned Results:" + str(agency_results) + "\n\n")
        request_type = self.__getTopKey(agency_request)
        #result_type = self.__getTopKey(agency_results)
        self.agencyRequest = agency_request[request_type]
        #agency_results = agency_results[result_type]
       
        
        
        
       


userID = "29405140-F42F-4646-9C6C-2A5F6B0AF973"        
beatest = GovernmentAPI_Struct(userID,'BEA')


                
"""
test = "http://www.bea.gov/api/data/?&UserID=29405140-F42F-4646-9C6C-2A5F6B0AF973&method=getparameterlist&datasetname=RegionalData&"

userID = "29405140-F42F-4646-9C6C-2A5F6B0AF973" 
location = "www.bea.gov/api/data/"
method = ("method", "getdatasetlist")
dataset = ("datasetname", "")

instruction = [method, dataset]

apiRequest = 'http://' + location + '?&UserID=' + userID +'&' 
for command in instruction:
    apiRequest = apiRequest + str(command[0]) + '=' + str(command[1]) + '&'
    
   
quiry = GovernmentAPI_Struct()
#apiRequest = 'http://' + location + '?&UserID=' + userID + '&method=' + method + '&datasetname=' + dataset + '&'
print(apiRequest)
print()
response = urllib.request.urlopen(apiRequest)
myjson=json.loads(response.read().decode('utf-8'))
quiry.agency = FindKeys.getTopKey(myjson)
returnObject=myjson[quiry.agency]
agency_request = returnObject['Request']
agency_results = returnObject['Results']
print("Requested: " + str(agency_request) + "\n\n")
print("Returned Results:" + str(agency_results) + "\n\n")
quiry.request_type = FindKeys.getTopKey(agency_request)
quiry.result_type = FindKeys.getTopKey(agency_results)
agency_request = agency_request[quiry.request_type]
agency_results = agency_results[quiry.result_type]
quiry.method = SimpleGov.get(agency_request,'METHOD')
quiry.dataset = SimpleGov.get(agency_request,'DATASETNAME')
print("Requested Method: " + quiry.method)
print("Requested Dataset: " + quiry.dataset)
#print(agency_request[0])
#print(agency_results[0])

#step1 = mjson[agency]
#myrequest = 
#print(struct)
"""
