"""
Prathidhwani Kandhalu
Nov 13th, 2016
Implementation of features to prevent fraudulent payment requests from untrusted
users.
"""

import sys

"""
The data structure for the user network of PayMo is a dictionary, userNetwork,
where the key is the user ID of a PayMo user and the value is a set of user ID
with whom the user ID in the key has had transactions with.
"""
userNetwork={}

def buildInitialUserNetwork(batchPaymentFilePath):
    """
    :batchPaymentFilePath: str
    Will be used to build initial user network using "batch_payment.txt"
    """
    with open(batchPaymentFilePath) as f:
        next(f)
        for line in f:
            userA, userB = lineParser(line)
            processTransaction(userA, userB)
        f.close()

def lineParser(line):
    """
    :line: string
    :rtype: tuple(int)
    Utility function that parses through line and returns the two IDs
    """
    line=line.split(",")
    userA=int(line[1])
    userB=int(line[2])
    return userA, userB

def processTransaction(userA, userB):
    """
    :userA: int
    :userB: int
    :rtype: bool
    Processs and records each transaction in the user network
    If a particular user has not used PayMo previously, the user is first
    put in the network.
    If userA and userB are first degree connections, i.e. a transaction has
    occurred in the past between the two users, return False
    Else, record the transaction in userNetwork and return True
    """
    if userA not in userNetwork:
        userNetwork[userA]=set()
    if userB not in userNetwork:
        userNetwork[userB]=set()
    if isFirstDegreeConnection(userA, userB):
        return False
    userNetwork[userA].add(userB)
    userNetwork[userB].add(userA)
    return True

#FEATURE 1
def isFirstDegreeConnection(userA, userB):
    """
    :userA: int
    :userB: int
    :rtype: bool
    Implements Feature 1
    Returns True if there has been a transaction between userA and userB, ie. userA and userB are friends
    False otherwise
    """
    if userA not in userNetwork:
        return False
    if userB not in userNetwork:
        return False
    if userB in userNetwork[userA]:
        return True
    return False

#FEATURE 2
def isWithinTwoDegrees(userA, userB):
    """
    :userA: int
    :userB: int
    :rtype: bool
    Implements Feature 2
    Returns True if userA and userB are friends (ie. first degree friends) OR
                    userA and userB are second degree friends
    False otherwise
    """
    if userA in userNetwork and userB in userNetwork:
        if userB in userNetwork[userA]:     #check if userB is first degree connection
            return True
        for each in userNetwork[userA]:     #check if userB is second degree connection
            if userB in userNetwork[each]:
                return True
    return False
    
#FEATURE 3
def isWithinFourDegrees(userA, userB):
    """
    :userA: int
    :userB: int
    :rtype: bool
    Implements Feature 3
    Returns True if userA and userB are friends (ie. first degree friends) OR
                    userA and userB are second degree friends OR
                    userA and userB are third degree friends OR
                    userA and userB are fourth degree friends
    False otherwise
    """
    secondDegree=set()
    thirdDegree=set()
    fourthDegree=set()
    if userA in userNetwork and userB in userNetwork:
        if userB in userNetwork[userA]:             #check if 1st degree connections
            return True
        
        for each in userNetwork[userA]:
            secondDegree.update(userNetwork[each])  #get and check 2nd degree connections
        if userB in secondDegree:
            return True
        
        for each in secondDegree:
            thirdDegree.update(userNetwork[each])   #get and check 3rd degree connections
        if userB in thirdDegree:
            return True
        
        for each in thirdDegree:
            fourthDegree.update(userNetwork[each])  #get and check 4th degree connections
        if userB in fourthDegree:
            return True
    return False

def feature1Output(streamPaymentFilePath, outputFile):
    output=open(outputFile, 'w')
    with open(streamPaymentFilePath) as f:
        next(f)
        for line in f:
            userA, userB = lineParser(line)
            if isFirstDegreeConnection(userA, userB):
                output.write("trusted\n")
            else:
                output.write("unverified\n")
            processTransaction(userA, userB)
    output.close()
   
def feature2Output(streamPaymentFilePath, outputFile):
    output=open(outputFile, 'w')
    with open(streamPaymentFilePath) as f:
        next(f)
        for line in f:
            userA, userB = lineParser(line)
            if isWithinTwoDegrees(userA, userB):
                output.write("trusted\n")
            else:
                output.write("unverified\n")
            processTransaction(userA, userB)
        f.close()
    output.close()

def feature3Output(streamPaymentFilePath, outputFile):
    output=open(outputFile, 'w')
    with open(streamPaymentFilePath) as f:
        next(f)
        for line in f:
            userA, userB = lineParser(line)
            if isWithinFourDegrees(userA, userB):
                output.write("trusted\n")
            else:
                output.write("unverified\n")
            processTransaction(userA, userB)
        f.close()
    output.close()
    
#############
if __name__=='__main__':
    batch=sys.argv[1]
    stream=sys.argv[2]

    print "Building initial network"
    buildInitialUserNetwork(batch)
    print "Done building initial network\nProcessing stream for Feature 1"
    feature1Output(stream, sys.argv[3])
    print "Done processing for Feature 1"

    print "\nRebuilding initial network for Feature 2"    
    userNetwork={}
    buildInitialUserNetwork(batch)
    print "Done building initial network\nProcessing stream for Feature 2"
    feature2Output(stream, sys.argv[4])
    print "Done processing for Feature 2"

    print "\nRebuilding initial network for Feature 3"   
    userNetwork={}
    buildInitialUserNetwork(batch)
    print "Done building initial network\nProcessing stream for Feature 3"
    feature3Output(stream, sys.argv[5])
    print "Done processing for Feature 3"
    print "\n\nDone overall :)"
