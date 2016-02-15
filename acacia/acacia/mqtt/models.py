from django.db import models
import paho.mqtt.client as mqtt
import logging
logger = logging.getLogger(__name__)

def on_connect(client, userdata, flags, rc):
    logger.info('{client} connected to {host}. Result = {rc}'.format(client=client._client_id,host=client._host, rc=rc))
    
def on_disconnect(client, userdata, rc):
    logger.info('{client} disconnected from {host}. Result = {rc}'.format(client=client._client_id,host=client._host, rc=rc))
    
def on_subscribe(client, userdata, mid, qos):
    logger.info('Subscribed to #{mid} with QoS={qos} by {client}'.format(mid=mid,qos=qos,client=client._client_id))

def on_unsubscribe(client, userdata, mid):
    logger.info('Unsubscribed from #{mid} by {client}'.format(mid=mid,client=client._client_id))

def on_message(client, userdata, msg):
    logger.info('Message received, topic={topic}'.format(topic=msg.topic))
    try:
        topic = Topic.objects.get(topic=msg.topic)
        msg, created = topic.message_set.get_or_create(payload=msg.payload)
        if created:
            logger.info('Message saved')
        else:
            logger.info('Message already exist')
    except Topic.DoesNotExist:
        logger.error('Topic not registered: %s' % msg.topic)

clients = {}

class Host(models.Model):
    host = models.CharField(max_length=256)
    port = models.IntegerField(default=1883)
    keepalive = models.IntegerField(default = 60)
    _client = None

    def connect(self):
        if not self.host in clients:
            # make a new client
            client = mqtt.Client()
            client.on_connect = on_connect
            client.on_disconnect = on_disconnect
            client.on_message = on_message
            client.on_subscribe = on_subscribe
            client.on_unsubscribe = on_unsubscribe
            client.connect(str(self.host), int(self.port), int(self.keepalive))
            clients[self.host] = client
        self._client = clients[self.host]
    
    def client(self):
        if self._client is None:
            self.connect()
        return self._client
    
    def __unicode__(self):
        return self.host    
    
class Topic(models.Model):
    host = models.ForeignKey(Host)
    topic = models.CharField(max_length=512)
    active = models.BooleanField(default = True)
    
    def client(self):
        return self.host.client()
    
    def subscribe(self):
        self.client().subscribe(str(self.topic))

    def unsubscribe(self):
        self.client().unsubscribe(str(self.topic))

    def __unicode__(self):
        return self.topic    

#     class Meta:
#         unique_together = ('host', 'topic')

from django.db.models.signals import pre_delete, pre_save
from django.dispatch.dispatcher import receiver

@receiver(pre_delete, sender=Topic)
def topic_delete(sender, instance, **kwargs):
    instance.unsubscribe()

@receiver(pre_save, sender=Topic)
def topic_save(sender, instance, **kwargs):
    instance.subscribe()

class Message(models.Model):
    date = models.DateTimeField(auto_now_add = True)
    topic = models.ForeignKey(Topic)
    payload = models.CharField(max_length=512)

    def __unicode__(self):
        return '%s %s' % (self.topic, self.date)

#     class Meta:
#         unique_together = ('date', 'topic')
    
def subscribe_all():
    for topic in Topic.objects.filter(active=True):
        topic.subscribe()
        
def start():
    subscribe_all()
    for host in Host.objects.all():
        host.client().loop_start()

# TODO: move somewhere else: we don't always want to start network loop          
start()
