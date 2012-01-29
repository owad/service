from django_cron import CronJobBase, Schedule
from django.core.mail import EmailMessage
from datetime import datetime
from dbbackup import Command


class DatabaseBackup(CronJobBase):
    RUN_EVERY_MINS = 1 # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'my_app.my_cron_job' # a unique code

    def do(self):
        file_path = Command().handle()
        mail = EmailMessage('Backup bazy iserwis.lechkom.pl z dnia %s' % datetime.now().strftime('%d-%m-%Y'), '', 'admin@iserwis.lechkom.pl', ['paboowicz@gmail.com'])
        mail.attach_file(file_path)
        mail.send()
