import urllib.request
import sys
import re

def main(args):    
    usage = "Usage: extor.py logfile IP_column# date_column#"
    if '-h' in args or '--help' in args:
    	print("extor.py: check log to identify TOR relays in past connections")
    	print(usage)
    elif len(args) < 4: 
	    print("Invalid number of arguments provided")
	    print(usage)
    else:
        try:
        	f = open(args[1])
        except:
        	print('Could not open file ' + args[1])
        	print(usage)
        	sys.exit(1)
        with open(args[1]) as f:
            log = f.readlines()
            if log:
                   for line in log:
                        try:
                        	ip = line.split()[int(args[2])-1]
                        	date = line.split()[int(args[3])-1]
                        except:
                        	print("Please specify correct column number for IP and date")
                        	print(usage)
                        	sys.exit(1)
                        ipregx = re.compile('([0-9]{1,3}\.){3}[0-9]{1,3}')
                        dateregx = re.compile('([0-9]{1,4}(\/|\-|\.)){2}[0-9]{1,4}') 
                        ip = ipregx.match(ip)
                        date = dateregx.match(date)
                        if (date is not None) and (ip is not None):
                        	date = re.split('\/|-|\.', date[0])
                        	if len(date[2]) == 4:
                        		date = date[2] + '-' + date[1] + '-' + date[0]
                        	else:
                        		date = '-'.join(date)
                        	try:
                        	    req = urllib.request.urlopen('https://metrics.torproject.org/exonerator.html?ip=' + ip[0] + '&timestamp=' + date + '&lang=en)')
                        	except:
                        	    print("Could not connect to API")
                        	    sys.exit(1)
                        else:
                        	print("Could not find IP and/or date in specified column")
                        	sys.exit(1)
                        torp = req.read().decode(req.headers.get_content_charset())
                        if "Result is positive" in torp:
                        	print(line.rstrip('\n') + " <--- TOR relay")
                        else:
                        	print(line.rstrip('\n'))
            else:
            	print("Could not read any data from " + args[1])
        f.close()

if __name__ == '__main__':
	main(sys.argv)
