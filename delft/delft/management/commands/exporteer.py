import os

from django.core.management.base import BaseCommand
from acacia.data.models import Series
from django.utils.text import slugify

class Command(BaseCommand):
    args = ''
    help = 'Export all series'
        
    fldr = '/media/sf_F_DRIVE/projdirs/Zuid-Holland/validatie/export'

    def handle(self, *args, **options):
        for s in Series.objects.all():
            loc = s.meetlocatie()
            if loc is None:
                name = slugify(s.name)
            else:
                loc = s.parameter
                name = slugify(unicode(loc)) 
                fname = os.path.join(self.fldr,name) + '.csv'
                print fname
                with open(fname,'w') as f:
                    text = s.to_csv()
                    f.write(text)
                
