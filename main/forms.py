from django import forms
from .models import Address,Product,Order

class AddressForm(forms.ModelForm):
	class Meta:
		model=Address
		fields='__all__'

	countryoptions=(
		('India','India'),
		)
	stateoptions=(
		('--Select--','--Select--'),
		('Andhra Pradesh','Andhra Pradesh'),
		('Andaman & Nicobar Islands','Andaman & Nicobar Islands'),
		('Arunachal Pradesh','Arunachal Pradesh'),
		('Assam','Assam'),
		('Bihar','Bihar'),
		('Chandigarh', 'Chandigarh'),
		('Chhattisgarh','Chhattisgarh'),
		('Dadar and Nagar Haveli','Dadar and Nagar Haveli'),
		('Daman and Diu', 'Daman and Diu'),
		('Delhi', 'Delhi'),
		('Goa', 'Goa'),
		('Gujarat','Gujarat'),
		('Haryana','Haryana'),
		('Himachal Pradesh','Himachal Pradesh'),
		('Jammu and Kashmir','Jammu and Kashmir'),
		('Karnataka','Karnataka'),
		('Kerala','Kerala'),
		('Lakshadweep', 'Lakshadweep'),
		('Madhya Pradesh','Madhya Pradesh'),
		('Maharashtra','Maharashtra'),
		('Manipur','Manipur'),
		('Meghalaya','Meghalaya'),
		('Mizoram','Mizoram'),
		('Nagaland','Nagaland'),
		('Odisha','Odisha'),
		('Puducherry','Puducherry'),
		('Punjab','Punjab'),
		('Rajasthan','Rajasthan'),
		('Sikkim','Sikkim'),
		('Telangana','Telangana'),
		('Tripura','Tripura'),
		('Uttar Pradesh','Uttar Pradesh'),
		('Uttarakhand','Uttarakhand'),
		('West Bengal','West Bengal')
		)

	name=forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control','autocomplete':'off'}))
	address=forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Address', 'class': 'form-control', 'rows':3,'autocomplete':'off'}))
	country=forms.ChoiceField(choices=countryoptions,widget=forms.Select(attrs={'class': 'form-control','autocomplete':'off'}))
	state=forms.ChoiceField(choices=stateoptions,widget=forms.Select(attrs={'class': 'form-control','autocomplete':'off'}))
	city=forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'City', 'class': 'form-control','autocomplete':'off'}))
	pincode=forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Pin Code', 'class': 'form-control','maxlength':'6','pattern':'\d{4}','autocomplete':'off'}))
	phone=forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Phone Number', 'class': 'form-control','autocomplete':'off'}))
	email=forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'E-mail ID', 'class': 'form-control','autocomplete':'off'}))
	is_saved=forms.BooleanField()


class ProductForm(forms.ModelForm):
	class Meta:
		model=Product
		fields='__all__'

	name=forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Product Name', 'class': 'form-control'}))
	price=forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Price', 'class': 'form-control'}))
	sku=forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'SKU', 'class': 'form-control'}))
	hsn=forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'HSN', 'class': 'form-control'}))
	weight=forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Weight (KG)', 'class': 'form-control'}))
	length=forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Length (cm)', 'class': 'form-control'}))
	breadth=forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Breadth', 'class': 'form-control'}))
	height=forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Height', 'class': 'form-control'}))