#!/usr/bin/env python
killAllHumans = 0
# original Author: Kyle L.
# modified by: Brian M.
version = '2013-07-03'
print ':: Agilent 53132A TIC Live Logger '+version

# Initializes Agilent 9343C, does setup, writes to GPS & station SNRs to CSV File
import datetime     # For current date
import time         # For process runtime
import visa as v    # For instrument interface
import sys          # For system calls

#pyvisa change
rm = v.ResourceManager('@py')

# Options
bridge = '192.168.44.133'   # GPIB Bridge IP
delay = 1.0                 # Time between queries
doFancyPlot = False

#print sys.argv
# Pull argv
#if len(sys.argv) != 2:
#    print ':: ERR - no GPIB location specified. try:'
#    print '   ./logtic 5'
#    print '   to log TIC values from GPIB 5 on the GPIB Bridge'
#    sys.exit(1)
#try:
#    int(sys.argv[1])
#    gpib = sys.argv[1]
#except:
#    print ':: ERR - could not understand input'

# Initialize Variables
gpib = '3' # manual override
run = True
now = datetime.datetime.now().isoformat()[0:19]
outFile = 'gpib_'+gpib+'_'+now+'_TIClog.csv'

# Startup TIC
try: tic = rm.open_resource('TCPIP::192.168.44.133::gpib0,3')
#try: tic = v.instrument('TCPIP::192.168.1.21::gpib0,'+gpib)
except:
	print '   error -> Could not find instrument at',hsaIP
	sys.exit(1)

#should initilialize TIC here, but am skipping for now...
#hsa.write('*rst')
#hsa.write(':system:configure:gps on')
#hsa.write(':system:configure:gpsinfo on')

# Startup Log
log = open(outFile,'w')
log.write('TIC '+now+'\n')

# Screen Output
print ':: Logging to',outFile
print '   ' + tic.ask('*idn?')

if doFancyPlot:
    #3d Plot stuff
    import numpy as np
    import matplotlib.pyplot as plt
    measurements = []
    plt.ion()
    #fig = plt.figure()
while run:
    # Detect and write
    try:

        start = time.time()
        tint = float(tic.ask(':FETCH:TINT?'))
        log.write(str(tint)+'\n')
        if doFancyPlot:
            measurements += [tint]
            #print derp
            if len(measurements) > 3:
                plt.plot(measurements)
                plt.grid(True)
                plt.draw()

        print '   Loop time: %1.3f\t Time Interval: %3.1f' % (time.time()-start,tint*1e9)
        sleeptime = delay - (time.time() - start)
        if sleeptime > 0: time.sleep(sleeptime)
    except KeyboardInterrupt:
        print '  exiting...'
        run = False
if doFancyPlot:
    plt.ioff()
    plt.show()
log.close()
tic.close()
