'''
Created on Sep 1, 2014

@author: theo
'''
from django import forms
from django.forms.widgets import RadioSelect
from .models import Scenario, Matrix

class ScenarioForm(forms.ModelForm):
    class Meta:
        model = Scenario
        fields = ['neerslag', 'bodem', 'kwaliteit', 'irrigatie', 'reken', 'oppervlakte', 'volume']
        widgets = {'reken': RadioSelect(),}
        
#     def __init__(self,*args,**kwargs):
#         super(ScenarioForm,self).__init__(*args,**kwargs)
#         self.fields['neerslag'].widget.attrs.update({'autofocus': 'autofocus'})

    # django < 1.7
    def add_error(self, field, msg):
        self._errors[field] = self.error_class([msg])
        del self.cleaned_data[field]
        
    def clean(self):
        d = self.cleaned_data;
        code = d['neerslag']+d['bodem']+d['kwaliteit']+d['irrigatie']
        try:
            matrix = Matrix.objects.get(code=code+'g')
        except:
            raise forms.ValidationError('Geen berekeningsresultaten beschikbaar voor deze combinatie van invoergegevens',code='invalid')
        
        if d['reken'] == 'o':
            grootte = d['oppervlakte'] * 10000 # Ha -> m2
            if grootte > matrix.rijmax:
                self.add_error('oppervlakte','Maximum oppervlakte is %g Ha' % (matrix.rijmax / 10000))
            elif grootte < matrix.rijmin:
                self.add_error('oppervlakte','Minimum oppervlakte is %g Ha' % (matrix.rijmin / 10000))
        else:
            grootte = d['volume']
            if grootte > matrix.kolmax:
                self.add_error('volume','Maximum volume is %g m2' % matrix.kolmax)
            elif grootte < matrix.kolmin:
                self.add_error('volume','Minimum volume is %g m2' % matrix.kolmin)
            
        return d
    
    
class AddMatrixForm(forms.ModelForm):
    class Meta:
        model = Matrix
        fields = ['file',]
        
    def save(self, commit=True):
        instance = super(AddMatrixForm, self).save(commit=False)
        instance.get_dimensions()
        return instance.save() if commit else instance
