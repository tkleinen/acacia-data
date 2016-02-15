from django.contrib import admin
from .models import Host, Topic, Message

class TopicInline(admin.TabularInline):
    model = Topic

class MessageInline(admin.TabularInline):
    model = Message

class HostAdmin(admin.ModelAdmin):
    model = Host
    inlines = [TopicInline]
    list_display = ('host', 'port')

class TopicAdmin(admin.ModelAdmin):
    model = Topic
    inlines = [MessageInline]
    list_display = ('topic', 'host', 'active')

class MessageAdmin(admin.ModelAdmin):
    model = Message
    list_display = ('topic', 'date', 'payload')
        
# Register your models here.
admin.site.register(Host, HostAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Message, MessageAdmin)
