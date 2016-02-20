from django.shortcuts import HttpResponse
from .models import Event
from django.utils import timezone
import json, datetime

#MESSAGEBIRD_APIKEY = 'test_hN7EwTAz8Xz9xmhradD1twXAg'
MESSAGEBIRD_APIKEY = 'live_JPcO8tl6eSRxOFClD0tSwO3A0'
    
class Messenger():

    def __init__(self, event):
        self.event = event
        self.history = []
        
    def __enter__(self):
        return self

    def __exit__(self, _type, _value, _traceback):
        if self.history:
            self.send_messages()
 
    def send_sms(self, originator, body, recipients):
        import messagebird
        client = messagebird.Client(MESSAGEBIRD_APIKEY)
        params = {}
        msg = client.message_create(originator, recipients, body, params)
        return msg
        
    def send_html_mail(self,subject, message, from_email, recipient_list,
                  fail_silently=False, auth_user=None, auth_password=None,
                  connection=None):
        from django.core.mail import get_connection, EmailMessage
        connection = connection or get_connection(username=auth_user,
                                        password=auth_password,
                                        fail_silently=fail_silently)
        m = EmailMessage(subject, message, from_email, recipient_list, connection=connection)
        m.content_subtype = "html"
        return m.send()

    def send_messages(self):
        if self.event.action == 1:
            html ='\r\n'.join([h.format_html() for h in self.history])
            success = self.send_html_mail('Acaciadata Alarm', html, 'alarm@acaciadata.com', [self.event.target.email])
        elif self.event.action == 2:
            message = 'Event {evt} was triggered {count} times'.format(evt=str(self.event.trigger), count=len(self.history))
            success = self.send_sms('Acaciadata', message, self.event.target.cellphone)
        if success:
            for h in self.history:
                h.sent=True
                h.save()

    def add(self, message):
        self.history.append(self.event.history_set.create(message=message, sent=False))

def testevent(request, pk):
    evt = Event.objects.get(pk=pk)
    history = evt.history_set.filter(sent=True).order_by('-date')
    start = history[0].date if history else datetime.datetime(2016,1,1,tzinfo=timezone.get_default_timezone())
    data = evt.trigger.generate(start=start)
    num = data.count()
    if num > 0:
        with Messenger(evt) as m:
            for date,value in data.iteritems():
                m.add(evt.format_message(date,value,html=True))
            msg = 'Event {evt} was triggered {count} times for {ser} since {date}'.format(evt=str(evt.trigger), count=num, ser=str(evt.trigger.series),date=start)
    else:
        msg = 'No events occurred since {date}'.format(date=start)
    return HttpResponse(json.dumps(msg), content_type='application/json')
