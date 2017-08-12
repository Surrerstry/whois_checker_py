import pythonwhois
import datetime
import re
from time import sleep


targets = ['surrerstry.pl',
			   'google.com',
			   'yahoo.com',
			   ]


domains = dict()
[domains.update({item:''}) for item in targets]

for domain in domains:
	try:
		domains[domain] = pythonwhois.get_whois(domain)
		sleep(1)
	except:
		pass

request_limit_exceeded = 0

res = dict()
for domain in domains:
	for information in domains[domain]:
		if information=='raw':
			if domains[domain][information][0].find('renewal date') != -1:
				res.update({domain:':'""+domains[domain][information][0]})
			elif domains[domain][information][0].find('request limit exceeded') != -1:
				res.update({domain:':request limit exceeded'})
				request_limit_exceeded += 1
		if information=='expiration_date':
			res.update({domain:domains[domain][information][0]})

res2 = dict()
for item in res:
	if isinstance(res[item], datetime.datetime):
		res2.update({item:res[item] - datetime.datetime.now()})
	if isinstance(res[item], str):
		if res[item].find('request limit exceeded') != -1:
			res2.update({item:datetime.timedelta(0)})
			continue
		tmp = res[item][res[item].find('renewal date:')+13:]
		tmp2 = re.search('\d\d\d\d', tmp)
		res2.update({item:datetime.datetime.strptime(tmp[tmp2.span()[0]:tmp2.span()[0]+19], '%Y.%m.%d %H:%M:%S') - datetime.datetime.now()})

report = []
report.append('--------------------------------------------------')
report.append('First Stage: Domains that failed: '+str(domains.keys()^res2.keys()))
report.append('Second Stage: Failed {} out of {} remaining'.format(request_limit_exceeded, len(res)))
report.append('Raport generated at: '+str(datetime.datetime.now()))
report.append('- - - - - - - - - - - - - - - - - - - - - - - - - ')

for item in sorted(res2, key=res2.get):
	report.append('{:<19} : {}'.format(str(res2[item])[:-7], item))

report.append('--------------------------------------------------')

for item in report:
	print(item)

filename = str(datetime.datetime.now()).replace(' ', '_').replace(':', '.')[:19]+'.txt'

with open(filename, 'w') as file:
	for item in report:
		file.write(item+'\n')
