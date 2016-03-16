from flask.ext.wtf import Form, widgets


from wtforms import SelectField

from wtforms import StringField, BooleanField, FieldList, FormField, RadioField, SubmitField, SelectMultipleField
from wtforms import IntegerField
#from wtforms.widgets import ListWidget
from wtforms.validators import DataRequired



class SpectraForm(Form):
    start_freq = IntegerField('Start Frequency (GHz):', default=2000)
    stop_freq = IntegerField('Stop Frequency (GHz):', default=600000)
    temp = IntegerField('Temperature (K):', default=300)
    molecules = SelectMultipleField("Molecules:", coerce=int, choices=[(0, "Inactive"), (1, "Active")],
                                    default=1 ,
                                    )
    submit = SubmitField("Submit")

    def __init__(self, molecules):
        super().__init__()
        self.molecules.choices = molecules
