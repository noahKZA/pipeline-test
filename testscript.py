#!/usr/bin/env python
# A basic ZAP Python API example which spiders and scans a target URL

import time
from pprint import pprint
from zapv2 import ZAPv2

target = 'http://zero.webappsecurity.com/'
apikey = 'bav0q7pv2ejaclej4hqsnd7r14' # Change to match the API key set in ZAP, or use None if the API key is disabled
context_naam = "TestContext"

#
# By default ZAP API client will connect to port 8080
zap = ZAPv2(apikey=apikey)
# Use the line below if ZAP is not listening on port 8080, for example, if listening on port 8090
# zap = ZAPv2(apikey=apikey, proxies={'http': 'http://127.0.0.1:8090', 'https': 'http://127.0.0.1:8090'})

# Import authentication script used in context
#zap.script.load("Test_authentication", "authentication", "Oracle Nashorn", "test.js")

#set selenium PhantomJS
#zap.selenium.set_option_phantom_js_binary_path('D:\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe', apikey=apikey)

#import context with authentication script
zap.context.import_context(contextfile = context_naam, apikey=apikey)
zap.context.set_context_in_scope(context_naam ,True, apikey=apikey)

#set forced user
zap.forcedUser.set_forced_user(2,0,apikey=apikey)
zap.forcedUser.set_forced_user_mode_enabled(True,apikey=apikey)

# Proxy a request to the target so that ZAP has something to deal with
print('Accessing target {}'.format(target))
zap.urlopen(target)
# Give the sites tree a chance to get updated
time.sleep(2)

print('Spidering target {}'.format(target))
scanid = zap.spider.scan(target)
# Give the Spider a chance to start
time.sleep(2)
while (int(zap.spider.status(scanid)) < 100):
    # Loop until the spider has finished
    print('Spider progress %: {}'.format(zap.spider.status(scanid)))
    time.sleep(2)

print ('Spider completed')

#Also ajax spider that has to run
# print(f'Ajax spider going to work now on {target}')
# scanid = zap.ajaxSpider.scan(target)
# time.sleep(2)
# while zap.ajaxSpider.status != 'stopped':
#     #Loop until the spider has finished
#     print('Ajax spider is busy')
#     time.sleep(4)

# print ('Ajax spider completed')
    

while (int(zap.pscan.records_to_scan) > 0):
      print ('Records to passive scan : {}'.format(zap.pscan.records_to_scan))
      time.sleep(2)

print ('Passive Scan completed')

print ('Active Scanning target {}'.format(target))
scanid = zap.ascan.scan(target)
while (int(zap.ascan.status(scanid)) < 100):
    # Loop until the scanner has finished
    print ('Scan progress %: {}'.format(zap.ascan.status(scanid)))
    time.sleep(5)

print ('Active Scan completed')

# Report the results

print ('Hosts: {}'.format(', '.join(zap.core.hosts)))
print ('Alerts: ')
pprint (zap.core.alerts())

with open ('report.html', 'w' ) as f:
    f.write(zap.core.htmlreport(apikey=apikey))
