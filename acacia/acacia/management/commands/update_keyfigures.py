'''
Created on Feb 13, 2014

@author: theo
'''
from django.core.management.base import BaseCommand
#from optparse import make_option
from acacia.data.models import KeyFigure
from acacia.data.loggers import DatasourceAdapter
import logging

class Command(BaseCommand):
    args = ''
    help = 'Update keyfigures'

    def handle(self, *args, **options):
        with DatasourceAdapter(logging.getLogger('update')) as logger:
            logger.datasource = ''
            logger.info('***UPDATE OF KEYFIGURES STARTED***')
            for k in KeyFigure.objects.all():
                oldvalue = k.value
                newvalue = k.update()
                if oldvalue != newvalue:
                    logger.debug('Keyfigure {loc): {name} updated to {value}'.format(name=k.name,loc=k.locatie,value=newvalue))
                else:
                    logger.debug('Keyfigure {loc): {name} not changed'.format(name=k.name,loc=k.locatie))
            logger.info('***UPDATE OF KEYFIGURES COMPLETED***')
