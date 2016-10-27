from EvoController.evoPyLib.evoPyLib import *
import datetime
import csv
import sys,os,errno,getopt
import numpy as np


helptext = 'genNoiseDisparity.py -v -p serial_port -r raw_output_file -o output_file'

def main():
    #get arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "vp:r:o:", ['verbose','port=','rawoutfile=','outputfile='])
    except getopt.GetoptError:
        print("Useage:")
        print helptext
        sys.exit()

    verbose = False
    port = ''
    rawoutfile = ''
    outputfile = ''


    for opt,arg in opts:
        if opt in ('-v','verbose'):
            verbose = True
        elif opt in ('-p','--port'):
            port = arg.strip()
        elif opt in ('-r', '--rawoutfile'):
            rawoutfile = arg.strip()
        elif opt in ('-o','--outputfile'):
            outputfile = arg.strip()


    #create the evoArray
    array = EvoArray(port)
    try: #EvoArrays need to be safely closed, this ensures that.

            #get 5 min of raw data and store it in rawData
            rawData = []
            endTime = datetime.datetime.now() + datetime.timedelta(minutes=5)#TODO MAKE THIS ACTUALLY 5 minutes
            while(datetime.datetime.now() <= endTime):
                curVals = list(array.getNext())
                rawData.append(curVals)
                if verbose:
                    print curVals

            if verbose:
                print "Raw Data:"
                print rawData

            #write raw data to raw outfile
            with open(rawoutfile,"w") as file:
                writer = csv.writer(file)
                writer.writerows(rawData)
                if verbose:
                    print "Raw Data saved to File."

            #do math to find out the variance of each sensor over the timespan
            sorted = map(list, zip(*rawData))
            if verbose:
                print "Sort values by sensor"
                print sorted
            result = map(np.var,sorted)
            if verbose:
                print result



            #output results to outputfile
            with open(outputfile,"w") as outfile:
                writer = csv.writer(outfile)
                writer.writerow(result)
                print "Final output saved. Test complete."

    except KeyboardInterrupt:
        array.close()
        sys.exit()

if __name__ == '__main__':
    main()
