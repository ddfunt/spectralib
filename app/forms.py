from flask.ext.wtf import Form, widgets


from wtforms import SelectField

from wtforms import StringField, BooleanField, FieldList, FormField, RadioField, SubmitField, SelectMultipleField,FloatField, validators
from wtforms import IntegerField
#from wtforms.widgets import ListWidget
from wtforms.validators import DataRequired



class SpectraForm(Form):
    start_freq = IntegerField('Start Frequency (MHz):', default=2000)
    stop_freq = IntegerField('Stop Frequency (MHz):', default=600000)
    temp = IntegerField('Temperature (K):', default=300)
    resolution = IntegerField('Resolution Elements (1/GHz):',

                              default=1,
                              )
    #linewidth = FloatField('Linewidth <sub>for spectrum only</sub> (MHz):', default=0.5)
    #show_spectra = BooleanField('Show Full Spectra?: ', default=False)
    molecules = SelectMultipleField("Molecules:", coerce=int, choices=[(0, "Inactive"), (1, "Active")],
                                    default=1 ,
                                    )
    submit = SubmitField("Submit")

    def __init__(self, molecules):
        super().__init__()
        self.molecules.choices = molecules
