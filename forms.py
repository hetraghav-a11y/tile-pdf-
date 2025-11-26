# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, FileField, TextAreaField
from wtforms.validators import DataRequired

class TileForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    sku = StringField("SKU")
    size = StringField("Size")
    price = StringField("Price")
    description = TextAreaField("Description")
    tags = StringField("Tags")
    photo = FileField("Photo")

class CompanyForm(FlaskForm):
    company_name = StringField("Company Name")
    phone = StringField("Phone")
    email = StringField("Email")
    logo = FileField("Logo")
