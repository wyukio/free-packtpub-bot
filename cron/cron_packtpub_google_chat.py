from crontab import CronTab
from sys import argv

if len(argv) >= 2: 
    url = argv[1] 
else: 
    raise AttributeError('Google chat bot URL is required.')

cron = CronTab(user='xerpa')  
job = cron.new(command='../script/packtpub.py %s' % argv[1])  
job.hour.every(11)

cron.write()    