from django.shortcuts import render, redirect
from .forms import AddressForm,ProductForm
from .models import Address,Product,Order,Shipment
from django.http import HttpResponse,JsonResponse
from django.core import serializers
import json
import datetime
from textwrap import wrap
from main.utils import render_to_pdf
# Create your views here.

#Index Page
def Index(request):
	return render(request,'main/shipnow-index.html',None)

# Addresses
def AddAddress(request):
	if(request.method=='GET'):
		form=AddressForm()
		data={}
		data['form']=form
		return render(request,'main/AddAddress.html',data)
	else:
		address=AddressForm(request.POST)
		address.save()
		return redirect('/displayaddress/')

def DisplayAddress(request):
	addresses=Address.objects.all()
	return render(request,'main/DisplayAddress.html',{'addresses':addresses})

def UpdateAddress(request,id):
	method=request.method
	if(method=='GET'):
		address=Address.objects.filter(id=id).values().first()
		data={}
		data['form']=AddressForm(address)
		return render(request,'main/UpdateAddress.html',data)
	else:
		try:
			address=Address.objects.get(id=id)
			addressform=AddressForm(request.POST,instance=address)
			addressform.save()
			return redirect('/displayaddress/')
		except:
			return HttpResponse('No Record Found for the Specified Query')

def DeleteAddress(request,id):
	try:
		a=Address.objects.filter(id=id)
		a.delete()
		return redirect('/displayaddress')
	except:
		return HttpResponse("Address does not Exists!")

#For Ajax Requests, API Endpoint
def FetchAddress(request):
	addresses = serializers.serialize("json", Address.objects.all())
	data = {"addresses": addresses}
	return JsonResponse(data,safe=False)

# Products

def AddProduct(request):
	if(request.method=='GET'):
		form=ProductForm()
		data={}
		data['form']=form
		return render(request,'main/AddProduct.html',data)
	else:
		address=ProductForm(request.POST)
		address.save()
		return redirect('/displayproduct/')

def DisplayProduct(request):
	products=Product.objects.all()
	return render(request,'main/DisplayProduct.html',{'products':products})

def UpdateProduct(request,id):
	method=request.method
	if(method=='GET'):
		product=Product.objects.filter(id=id).values().first()
		data={}
		data['form']=ProductForm(product)
		return render(request,'main/UpdateProduct.html',data)
	else:
		try:
			product=Product.objects.get(id=id)
			productform=ProductForm(request.POST,instance=product)
			productform.save()
			return redirect('/displayproduct/')
		except:
			return HttpResponse('No Record Found for the Specified Query')

def DeleteProduct(request,id):
	try:
		a=Product.objects.filter(id=id)
		a.delete()
		return redirect('/displayproduct')
	except:
		return HttpResponse("Product does not Exists!")

def FetchProduct(request):
	products = serializers.serialize("json", Product.objects.all())
	data = {"products": products}
	return JsonResponse(data,safe=False)

# Orders

def AddOrder(request):

	if(request.method=='POST'):
		pickup_address_selector=request.POST.get('pickup_address_selector')
		delivery_address_selector=request.POST.get('delivery_address_selector')
		product_selector=request.POST.get('product_selector')

		try:
			pickup_address=Address.objects.get(id=pickup_address_selector)

		except:
			is_saved=request.POST.get('pickup_save')
			is_saved = 1 if 'True' else 0
			pickup_address=Address()
			pickup_address.name=request.POST.get('pickup_name')
			pickup_address.address=request.POST.get('pickup_address')
			pickup_address.country=request.POST.get('pickup_country')
			pickup_address.state=request.POST.get('pickup_state')
			pickup_address.city=request.POST.get('pickup_city')
			pickup_address.pincode=request.POST.get('pickup_pincode')
			pickup_address.phone=request.POST.get('pickup_phone')
			pickup_address.email=request.POST.get('pickup_email')
			pickup_address.is_saved=is_saved
			pickup_address.save()



		try:
			delivery_address=Address.objects.get(id=delivery_address_selector)

		except:
			is_saved=request.POST.get('delivery_save')
			is_saved = 1 if 'True' else 0
			delivery_address=Address()
			delivery_address.name=request.POST.get('delivery_name')
			delivery_address.address=request.POST.get('delivery_address')
			delivery_address.country=request.POST.get('delivery_country')
			delivery_address.state=request.POST.get('delivery_state')
			delivery_address.city=request.POST.get('delivery_city')
			delivery_address.pincode=request.POST.get('delivery_pincode')
			delivery_address.phone=request.POST.get('delivery_phone')
			delivery_address.email=request.POST.get('delivery_email')
			delivery_address.is_saved=is_saved
			delivery_address.save()

		try:
			product=Product.objects.get(id=product_selector)

		except:
			is_saved=request.POST.get('product_save')
			is_saved = 1 if 'True' else 0
			product=Product()
			product.name=request.POST.get('product_name')
			product.price=request.POST.get('product_price')
			product.sku=request.POST.get('product_sku')
			product.hsn=request.POST.get('product_hsn')
			product.weight=request.POST.get('product_weight')
			product.length=request.POST.get('product_length')
			product.breadth=request.POST.get('product_breadth')
			product.height=request.POST.get('product_height')
			product.is_saved=is_saved
			product.save()

		# Passing the Above details to Order

		order=Order()
		order.pickup=pickup_address
		order.delivery=delivery_address
		order.product=product
		order.payment_mode=request.POST.get('payment_mode')
		order.amount=request.POST.get('order_amount')
		now=datetime.datetime.now()
		order.datetime = now.strftime("%Y-%m-%d %H:%M")
		order.save()
		return redirect('/createshipment/'+str(order.id))

#--------------------------------------------------------------------------			
# Form's GET Part Below

	addressform1=AddressForm(auto_id="pickup_%s")
	addressform2=AddressForm(auto_id="delivery_%s")
	productform=ProductForm(auto_id="product_%s")
	addresses=Address.objects.filter(is_saved=True)
	products=Product.objects.filter(is_saved=True)
	data={
	'addressform1':addressform1,
	'addressform2':addressform2,
	'productform':productform,
	'addresses':addresses,
	'products':products
	}
	return render(request,'main/AddOrder.html',data)

def DisplayOrder(request):
	orders=Order.objects.all()
	return render(request,'main/DisplayOrder.html',{'orders':orders})

def DeleteOrder(request,id):
	try:
		a=Order.objects.filter(id=id)
		a.delete()
		return redirect('/displayorder')
	except:
		return HttpResponse("Order does not Exists!")

#For Ajax Requests, API Endpoint
def FetchOrder(request):
	orders = serializers.serialize("python", Order.objects.all())
	data = {"orders": orders}
	return JsonResponse(data,safe=False)

def CreateShipment(request,oid):
	order=Order.objects.filter(id=oid).first()
	# couriers=['FedEx','Delhivery','Shyplite']
	couriers={}

	# Courier Selection Part will be here.
	if(order.payment_mode=='cod'):
		if(order.amount<=20000):
			import csv
			line=order.delivery.pincode
			with open('fedex_cod.csv', 'r') as fp:
			    csvreader = csv.reader(fp)
			    for row in csvreader:
			            if line == int(row[0]):
			                couriers.update(FX_Air=(50+(130*order.product.weight)))
			                couriers.update(FX_Road=(50+(46*order.product.weight)) if (50+(46*order.product.weight)) >= 50+92 else 50+92)

		# Delhivery Courier
		import requests
		surface_token='***REMOVED***'
		heavy_token='***REMOVED***'
		try:
			response = requests.get('https://staging-express.delhivery.com/c/api/pin-codes/json/?token='+surface_token+'&filter_codes='+str(order.delivery.pincode))
			response = response.json()
			service=response['delivery_codes'][0]['postal_code']['cod']
			headers={'authorization':'Token ***REMOVED***','accept':'application/json','Content-Type':'application/json'}
			response = requests.get('https://track.delhivery.com/api/kinko/v1/invoice/charges/.json?ss=Delivered&md=S&zn=C2&pt=COD',headers=headers)
			response = response.json()
			a=response[0]['total_amount']
			couriers.update(DelhiverySF=a)
			couriers.update(Delhivery5KG='200 (upto 5 KG) after that 30 Rs./KG')
		except:
			pass
		if not couriers:
			no_service=True




	if(order.payment_mode=='prepaid'):
		import csv
		line=order.delivery.pincode
		with open('fedex_prepaid.csv', 'r') as fp:
		    csvreader = csv.reader(fp)
		    for row in csvreader:
		            if line == int(row[0]):
		                couriers.update(FX_Air=(130*order.product.weight))
		                couriers.update(FX_Road=(46*order.product.weight) if 46*order.product.weight >= 92 else 92)
		#Delhivery Courier
		import requests
		surface_token='***REMOVED***'
		heavy_token='***REMOVED***'
		try:
			response = requests.get('https://staging-express.delhivery.com/c/api/pin-codes/json/?token='+surface_token+'&filter_codes='+str(order.delivery.pincode))
			response = response.json()
			service=response['delivery_codes'][0]['postal_code']['pre_paid']
			headers={'authorization':'Token ***REMOVED***','accept':'application/json','Content-Type':'application/json'}
			response = requests.get('https://track.delhivery.com/api/kinko/v1/invoice/charges/.json?ss=Delivered&md=S&zn=C2&pt=COD',headers=headers)
			response = response.json()
			a=response[0]['total_amount']
			couriers.update(DelhiverySF=a)
			couriers.update(Delhivery5KG='200 (upto 5 KG) after that 30 Rs./KG')
		except:
			pass





	# couriers['FedEx']=131*order.product.weight
	# couriers['Delhivery']=120*order.product.weight
	# couriers['Shyplite']=130*order.product.weight
	
	if(request.method=='GET'):
		data={}
		data['couriers']=couriers
		data['order']=order
		try:
			data['no_service']=no_service
		except:
			pass
		return render(request,'main/CreateShipment.html',data)
	
def CreateShipmentFinal(request,oid,courier):
	order=Order.objects.filter(id=oid).first()

	if courier=='FX_Air':
		# #FedEx API Part

		# #!/usr/bin/env python
		# """
		# This example shows how to create a shipment and generate a waybill as output. The variables populated below
		# represents the minimum required values. You will need to fill all of these, or
		# risk seeing a SchemaValidationError exception thrown.

		# Near the bottom of the module, you'll see some different ways to handle the
		# label data that is returned with the reply.
		# """
		import logging
		import binascii
		import datetime
		import sys

		from .fedex.examples.example_config import CONFIG_OBJ
		from fedex.services.ship_service import FedexProcessShipmentRequest

		# What kind of file do you want this example to generate?
		# Valid choices for this example are PDF, PNG
		GENERATE_IMAGE_TYPE = 'PDF'

		# Un-comment to see the response from Fedex printed in stdout.
		logging.basicConfig(stream=sys.stdout, level=logging.INFO)

		# This is the object that will be handling our shipment request.
		# We're using the FedexConfig object from example_config.py in this dir.
		customer_transaction_id = "*** ShipService Request v17 using Python ***"  # Optional transaction_id
		shipment = FedexProcessShipmentRequest(CONFIG_OBJ, customer_transaction_id=customer_transaction_id)

		# This is very generalized, top-level information.
		# REGULAR_PICKUP, REQUEST_COURIER, DROP_BOX, BUSINESS_SERVICE_CENTER or STATION
		shipment.RequestedShipment.DropoffType = 'REGULAR_PICKUP'

		# See page 355 in WS_ShipService.pdf for a full list. Here are the common ones:
		# STANDARD_OVERNIGHT, PRIORITY_OVERNIGHT, FEDEX_GROUND, FEDEX_EXPRESS_SAVER,
		# FEDEX_2_DAY, INTERNATIONAL_PRIORITY, SAME_DAY, INTERNATIONAL_ECONOMY
		shipment.RequestedShipment.ServiceType = 'STANDARD_OVERNIGHT'

		# What kind of package this will be shipped in.
		# FEDEX_BOX, FEDEX_PAK, FEDEX_TUBE, YOUR_PACKAGING, FEDEX_ENVELOPE
		shipment.RequestedShipment.PackagingType = 'YOUR_PACKAGING'

		# Shipper contact info.
		shipment.RequestedShipment.Shipper.Contact.PersonName = order.pickup.name
		shipment.RequestedShipment.Shipper.Contact.CompanyName = ''
		shipment.RequestedShipment.Shipper.Contact.PhoneNumber = order.pickup.phone

		# Shipper address.
		shipment.RequestedShipment.Shipper.Address.StreetLines = wrap(order.pickup.address,35)
		shipment.RequestedShipment.Shipper.Address.City = order.pickup.city
		shipment.RequestedShipment.Shipper.Address.StateOrProvinceCode = 'DL'
		shipment.RequestedShipment.Shipper.Address.PostalCode = order.pickup.pincode
		shipment.RequestedShipment.Shipper.Address.CountryCode = 'IN'
		shipment.RequestedShipment.Shipper.Address.Residential = False

		# Recipient contact info.
		shipment.RequestedShipment.Recipient.Contact.PersonName = order.delivery.name
		shipment.RequestedShipment.Recipient.Contact.CompanyName = ''
		shipment.RequestedShipment.Recipient.Contact.PhoneNumber = order.delivery.phone

		# Recipient address
		shipment.RequestedShipment.Recipient.Address.StreetLines = wrap(order.delivery.address,35)
		shipment.RequestedShipment.Recipient.Address.City = order.delivery.city
		shipment.RequestedShipment.Recipient.Address.StateOrProvinceCode = 'DL'
		shipment.RequestedShipment.Recipient.Address.PostalCode = order.delivery.pincode
		shipment.RequestedShipment.Recipient.Address.CountryCode = 'IN'
		# This is needed to ensure an accurate rate quote with the response. Use AddressValidation to get ResidentialStatus
		shipment.RequestedShipment.Recipient.Address.Residential = True
		shipment.RequestedShipment.EdtRequestType = 'NONE'

		# Create Weight, in pounds.
		package1_weight = shipment.create_wsdl_object_of_type('Weight')
		package1_weight.Value = float(order.product.weight)
		package1_weight.Units = "KG"

		quantity=1
		commodity = shipment.create_wsdl_object_of_type('Commodity')
		commodity.Name = order.product.name
		commodity.NumberOfPieces = quantity
		commodity.Description = order.product.name
		commodity.CountryOfManufacture = "IN"
		commodity.Weight = package1_weight
		commodity.Quantity = quantity
		commodity.QuantityUnits = 'PCS' # EACH - for items measured in units
		commodity.UnitPrice.Currency = "INR"
		commodity.UnitPrice.Amount = int(order.amount)
		commodity.CustomsValue.Currency = "INR"
		commodity.CustomsValue.Amount = quantity * commodity.UnitPrice.Amount

		# Custom Clearance Details

		shipment.RequestedShipment.CustomsClearanceDetail.DutiesPayment.Payor.ResponsibleParty.AccountNumber = CONFIG_OBJ.account_number
		shipment.RequestedShipment.CustomsClearanceDetail.DutiesPayment.PaymentType = 'SENDER'

		# TODO
		# Implement Commercial Invoice and Purpose of Shipment (as a property of Commerial Invoice)
		# Acceptable values:
		# "GIFT", "NOT_SOLD", "PERSONAL_EFFECTS", "REPAIR_AND_RETURN", "SAMPLE","SOLD"
		shipment.RequestedShipment.CustomsClearanceDetail.CommercialInvoice.Purpose = "SOLD"
		shipment.RequestedShipment.CustomsClearanceDetail.CustomsValue.Amount = int(order.amount)
		shipment.RequestedShipment.CustomsClearanceDetail.CustomsValue.Currency = 'INR'

		shipment.add_commodity(commodity)

		# Senders account information
		shipment.RequestedShipment.ShippingChargesPayment.Payor.ResponsibleParty.AccountNumber = CONFIG_OBJ.account_number

		# Who pays for the shipment?
		# RECIPIENT, SENDER or THIRD_PARTY
		shipment.RequestedShipment.ShippingChargesPayment.PaymentType = 'SENDER'

		# Specifies the label type to be returned.
		# LABEL_DATA_ONLY or COMMON2D
		shipment.RequestedShipment.LabelSpecification.LabelFormatType = 'COMMON2D'

		# Specifies which format the label file will be sent to you in.
		# DPL, EPL2, PDF, PNG, ZPLII
		shipment.RequestedShipment.LabelSpecification.ImageType = GENERATE_IMAGE_TYPE

		# To use doctab stocks, you must change ImageType above to one of the
		# label printer formats (ZPLII, EPL2, DPL).
		# See documentation for paper types, there quite a few.
		shipment.RequestedShipment.LabelSpecification.LabelStockType = 'PAPER_8.5X11_TOP_HALF_LABEL'

		# This indicates if the top or bottom of the label comes out of the 
		# printer first.
		# BOTTOM_EDGE_OF_TEXT_FIRST or TOP_EDGE_OF_TEXT_FIRST
		# Timestamp in YYYY-MM-DDThh:mm:ss format, e.g. 2002-05-30T09:00:00
		shipment.RequestedShipment.ShipTimestamp = datetime.datetime.now().replace(microsecond=0).isoformat()

		# BOTTOM_EDGE_OF_TEXT_FIRST, TOP_EDGE_OF_TEXT_FIRST
		shipment.RequestedShipment.LabelSpecification.LabelPrintingOrientation = 'TOP_EDGE_OF_TEXT_FIRST'

		# Delete the flags we don't want.
		# Can be SHIPPING_LABEL_FIRST, SHIPPING_LABEL_LAST or delete
		if hasattr(shipment.RequestedShipment.LabelSpecification, 'LabelOrder'):
		    del shipment.RequestedShipment.LabelSpecification.LabelOrder  # Delete, not using.


		# Insured Value
		# package1_insure = shipment.create_wsdl_object_of_type('Money')
		# package1_insure.Currency = 'USD'
		# package1_insure.Amount = 1.0

		# Create PackageLineItem
		package1 = shipment.create_wsdl_object_of_type('RequestedPackageLineItem')
		# BAG, BARREL, BASKET, BOX, BUCKET, BUNDLE, CARTON, CASE, CONTAINER, ENVELOPE etc..
		package1.PhysicalPackaging = 'BOX'
		package1.Weight = package1_weight

		# Add Insured and Total Insured values.
		# package1.InsuredValue = package1_insure
		# shipment.RequestedShipment.TotalInsuredValue = package1_insure

		# Add customer reference
		customer_reference = shipment.create_wsdl_object_of_type('CustomerReference')
		customer_reference.CustomerReferenceType="CUSTOMER_REFERENCE"
		customer_reference.Value = str(order.delivery.name+" "+order.delivery.city)
		package1.CustomerReferences.append(customer_reference)

		# Add department number
		department_number = shipment.create_wsdl_object_of_type('CustomerReference')
		department_number.CustomerReferenceType="DEPARTMENT_NUMBER"
		department_number.Value = "support@oldlappy.com"
		package1.CustomerReferences.append(department_number)

		# Add invoice number
		# invoice_number = shipment.create_wsdl_object_of_type('CustomerReference')
		# invoice_number.CustomerReferenceType="INVOICE_NUMBER"
		# invoice_number.Value = "your invoice number"
		# package1.CustomerReferences.append(invoice_number)

		# Add a signature option for the package using SpecialServicesRequested or comment out.
		# SpecialServiceTypes can be APPOINTMENT_DELIVERY, COD, DANGEROUS_GOODS, DRY_ICE, SIGNATURE_OPTION etc..
		package1.SpecialServicesRequested.SpecialServiceTypes = 'SIGNATURE_OPTION'
		# SignatureOptionType can be ADULT, DIRECT, INDIRECT, NO_SIGNATURE_REQUIRED, SERVICE_DEFAULT
		package1.SpecialServicesRequested.SignatureOptionDetail.OptionType = 'SERVICE_DEFAULT'
		# shipment.RequestedShipment.SpecialServicesRequested.CodDetail.AddTransportationChargesDetail.RateTypeBasis = 'ACCOUNT'
		# shipment.RequestedShipment.SpecialServicesRequested.CodDetail.AddTransportationChargesDetail.ChargeBasisLevel = 'CURRENT_PACKAGE'
		# shipment.RequestedShipment.SpecialServicesRequested.CodDetail.CodRecipient.Contact = 'Murli Aggarwal'
		# shipment.RequestedShipment.SpecialServicesRequested.CodDetail.CodRecipient.City = 'New Delhi'
		# shipment.RequestedShipment.SpecialServicesRequested.CodDetail.CodRecipient.Country = 'India'
		# shipment.RequestedShipment.SpecialServicesRequested.CodDetail.CodRecipient.State = 'Delhi'
		# shipment.RequestedShipment.SpecialServicesRequested.CodDetail.CodRecipient.PostalCode = '110085'
		# shipment.RequestedShipment.SpecialServicesRequested.CodDetail.CodRecipient.Phone = '9891413700'
		# shipment.RequestedShipment.SpecialServicesRequested.CodDetail.CodRecipient.RemitToName = 'Honest Computers'


		if(order.payment_mode)=='cod':
			shipment.RequestedShipment.SpecialServicesRequested.SpecialServiceTypes = 'COD'
			package1.SpecialServicesRequested.CodDetail.CodCollectionAmount.Currency = 'INR'
			package1.SpecialServicesRequested.CodDetail.CodCollectionAmount.Amount = int(order.amount)
			shipment.RequestedShipment.SpecialServicesRequested.CodDetail.CodCollectionAmount.Currency = 'INR'
			shipment.RequestedShipment.SpecialServicesRequested.CodDetail.CodCollectionAmount.Amount = int(order.amount)
			shipment.RequestedShipment.SpecialServicesRequested.CodDetail.CollectionType = 'CASH'
			package1.SpecialServicesRequested.CodDetail.CollectionType = 'CASH'




		# Un-comment this to see the other variables you may set on a package.
		# print(package1)

		# This adds the RequestedPackageLineItem WSDL object to the shipment. It
		# increments the package count and total weight of the shipment for you.
		shipment.add_package(package1)

		# If you'd like to see some documentation on the ship service WSDL, un-comment
		# this line. (Spammy).
		# print(shipment.client)

		# Un-comment this to see your complete, ready-to-send request as it stands
		# before it is actually sent. This is useful for seeing what values you can
		# change.
		# print(shipment.RequestedShipment)
		# print(shipment.ClientDetail)
		# print(shipment.TransactionDetail)

		# If you want to make sure that all of your entered details are valid, you
		# can call this and parse it just like you would via send_request(). If
		# shipment.response.HighestSeverity == "SUCCESS", your shipment is valid.
		# print(shipment.send_validation_request())

		# Fires off the request, sets the 'response' attribute on the object.
		shipment.send_request()

		# This will show the reply to your shipment being sent. You can access the
		# attributes through the response attribute on the request object. This is
		# good to un-comment to see the variables returned by the Fedex reply.
		# print(shipment.response)

		# This will convert the response to a python dict object. To
		# make it easier to work with. Also see basic_sobject_to_dict, it's faster but lacks options.
		from fedex.tools.conversion import basic_sobject_to_dict
		response_dict = basic_sobject_to_dict(shipment.response)
		response_dict['CompletedShipmentDetail']['CompletedPackageDetails'][0]['Label']['Parts'][0]['Image'] = ''
		print(response_dict)  # Image is empty string for display purposes.

		# This will dump the response data dict to json.
		# from fedex.tools.conversion import sobject_to_json
		# print(sobject_to_json(shipment.response))

		# Here is the overall end result of the query.
		print("HighestSeverity: {}".format(shipment.response.HighestSeverity))

		# Getting the tracking number from the new shipment.
		print("Tracking #: {}"
		      "".format(shipment.response.CompletedShipmentDetail.CompletedPackageDetails[0].TrackingIds[0].TrackingNumber))

		# Net shipping costs. Only show if available. Sometimes sandbox will not include this in the response.
		CompletedPackageDetails = shipment.response.CompletedShipmentDetail.CompletedPackageDetails[0]
		if hasattr(CompletedPackageDetails, 'PackageRating'):
		    print("Net Shipping Cost (US$): {}"
		          "".format(CompletedPackageDetails.PackageRating.PackageRateDetails[0].NetCharge.Amount))
		else:
		    print('WARNING: Unable to get shipping rate.')

		# Get the label image in ASCII format from the reply. Note the list indices
		# we're using. You'll need to adjust or iterate through these if your shipment
		# has multiple packages.

		ascii_label_data = shipment.response.CompletedShipmentDetail.CompletedPackageDetails[0].Label.Parts[0].Image

		# Convert the ASCII data to binary.
		label_binary_data = binascii.a2b_base64(ascii_label_data)

		"""
		This is an example of how to dump a label to a local file.
		"""
		awb=str(shipment.response.CompletedShipmentDetail.CompletedPackageDetails[0].TrackingIds[0].TrackingNumber)
		# This will be the file we write the label out to.
		out_path = 'cdn/labels/' + awb + '.pdf'
		print("Writing to file {}".format(out_path))
		out_file = open(out_path, 'wb')
		out_file.write(label_binary_data)
		out_file.close()
		# Creating Shipment Object now!

		shipment = Shipment()
		shipment.order = order
		shipment.awb = awb
		shipment.courier = courier
		shipment.save()
		# return HttpResponse(label_binary_data, content_type='application/pdf')
		return redirect('/displayshipments/'+ str(shipment.id))



		"""
		This is an example of how to print the label to a serial printer. This will not
		work for all label printers, consult your printer's documentation for more
		details on what formats it can accept.
		"""
		# Pipe the binary directly to the label printer. Works under Linux
		# without requiring PySerial. This WILL NOT work on other platforms.
		# label_printer = open("/dev/ttyS0", "w")
		# label_printer.write(label_binary_data)
		# label_printer.close()

		"""
		This is a potential cross-platform solution using pySerial. This has not been
		tested in a long time and may or may not work. For Windows, Mac, and other
		platforms, you may want to go this route.
		"""
		# import serial
		# label_printer = serial.Serial(0)
		# print("SELECTED SERIAL PORT: "+ label_printer.portstr)
		# label_printer.write(label_binary_data)
		# label_printer.close()
		# return HttpResponse('Shipment Created Succesfully! Tracking Number : ' + str(shipment.response.CompletedShipmentDetail.CompletedPackageDetails[0].TrackingIds[0].TrackingNumber))

	elif courier=='FX_Road':
		# #FedEx API Part

		# #!/usr/bin/env python
		# """
		# This example shows how to create a shipment and generate a waybill as output. The variables populated below
		# represents the minimum required values. You will need to fill all of these, or
		# risk seeing a SchemaValidationError exception thrown.

		# Near the bottom of the module, you'll see some different ways to handle the
		# label data that is returned with the reply.
		# """
		import logging
		import binascii
		import datetime
		import sys

		from .fedex.examples.example_config import CONFIG_OBJ
		from fedex.services.ship_service import FedexProcessShipmentRequest

		# What kind of file do you want this example to generate?
		# Valid choices for this example are PDF, PNG
		GENERATE_IMAGE_TYPE = 'PDF'

		# Un-comment to see the response from Fedex printed in stdout.
		logging.basicConfig(stream=sys.stdout, level=logging.INFO)

		# This is the object that will be handling our shipment request.
		# We're using the FedexConfig object from example_config.py in this dir.
		customer_transaction_id = "*** ShipService Request v17 using Python ***"  # Optional transaction_id
		shipment = FedexProcessShipmentRequest(CONFIG_OBJ, customer_transaction_id=customer_transaction_id)

		# This is very generalized, top-level information.
		# REGULAR_PICKUP, REQUEST_COURIER, DROP_BOX, BUSINESS_SERVICE_CENTER or STATION
		shipment.RequestedShipment.DropoffType = 'REGULAR_PICKUP'

		# See page 355 in WS_ShipService.pdf for a full list. Here are the common ones:
		# STANDARD_OVERNIGHT, PRIORITY_OVERNIGHT, FEDEX_GROUND, FEDEX_EXPRESS_SAVER,
		# FEDEX_2_DAY, INTERNATIONAL_PRIORITY, SAME_DAY, INTERNATIONAL_ECONOMY
		shipment.RequestedShipment.ServiceType = 'FEDEX_EXPRESS_SAVER'

		# What kind of package this will be shipped in.
		# FEDEX_BOX, FEDEX_PAK, FEDEX_TUBE, YOUR_PACKAGING, FEDEX_ENVELOPE
		shipment.RequestedShipment.PackagingType = 'YOUR_PACKAGING'

		# Shipper contact info.
		shipment.RequestedShipment.Shipper.Contact.PersonName = order.pickup.name
		shipment.RequestedShipment.Shipper.Contact.CompanyName = ''
		shipment.RequestedShipment.Shipper.Contact.PhoneNumber = order.pickup.phone

		# Shipper address.
		shipment.RequestedShipment.Shipper.Address.StreetLines = wrap(order.pickup.address,35)
		shipment.RequestedShipment.Shipper.Address.City = order.pickup.city
		shipment.RequestedShipment.Shipper.Address.StateOrProvinceCode = 'DL'
		shipment.RequestedShipment.Shipper.Address.PostalCode = order.pickup.pincode
		shipment.RequestedShipment.Shipper.Address.CountryCode = 'IN'
		shipment.RequestedShipment.Shipper.Address.Residential = False

		# Recipient contact info.
		shipment.RequestedShipment.Recipient.Contact.PersonName = order.delivery.name
		shipment.RequestedShipment.Recipient.Contact.CompanyName = ''
		shipment.RequestedShipment.Recipient.Contact.PhoneNumber = order.delivery.phone

		# Recipient address
		shipment.RequestedShipment.Recipient.Address.StreetLines = wrap(order.delivery.address,35)
		shipment.RequestedShipment.Recipient.Address.City = order.delivery.city
		shipment.RequestedShipment.Recipient.Address.StateOrProvinceCode = 'DL'
		shipment.RequestedShipment.Recipient.Address.PostalCode = order.delivery.pincode
		shipment.RequestedShipment.Recipient.Address.CountryCode = 'IN'
		# This is needed to ensure an accurate rate quote with the response. Use AddressValidation to get ResidentialStatus
		shipment.RequestedShipment.Recipient.Address.Residential = True
		shipment.RequestedShipment.EdtRequestType = 'NONE'

		# Create Weight, in pounds.
		package1_weight = shipment.create_wsdl_object_of_type('Weight')
		package1_weight.Value = float(order.product.weight)
		package1_weight.Units = "KG"

		quantity=1
		commodity = shipment.create_wsdl_object_of_type('Commodity')
		commodity.Name = order.product.name
		commodity.NumberOfPieces = quantity
		commodity.Description = order.product.name
		commodity.CountryOfManufacture = "IN"
		commodity.Weight = package1_weight
		commodity.Quantity = quantity
		commodity.QuantityUnits = 'PCS' # EACH - for items measured in units
		commodity.UnitPrice.Currency = "INR"
		commodity.UnitPrice.Amount = int(order.amount)
		commodity.CustomsValue.Currency = "INR"
		commodity.CustomsValue.Amount = quantity * commodity.UnitPrice.Amount

		# Custom Clearance Details

		shipment.RequestedShipment.CustomsClearanceDetail.DutiesPayment.Payor.ResponsibleParty.AccountNumber = CONFIG_OBJ.account_number
		shipment.RequestedShipment.CustomsClearanceDetail.DutiesPayment.PaymentType = 'SENDER'

		# TODO
		# Implement Commercial Invoice and Purpose of Shipment (as a property of Commerial Invoice)
		# Acceptable values:
		# "GIFT", "NOT_SOLD", "PERSONAL_EFFECTS", "REPAIR_AND_RETURN", "SAMPLE","SOLD"
		shipment.RequestedShipment.CustomsClearanceDetail.CommercialInvoice.Purpose = "SOLD"
		shipment.RequestedShipment.CustomsClearanceDetail.CustomsValue.Amount = int(order.amount)
		shipment.RequestedShipment.CustomsClearanceDetail.CustomsValue.Currency = 'INR'

		shipment.add_commodity(commodity)

		# Senders account information
		shipment.RequestedShipment.ShippingChargesPayment.Payor.ResponsibleParty.AccountNumber = CONFIG_OBJ.account_number

		# Who pays for the shipment?
		# RECIPIENT, SENDER or THIRD_PARTY
		shipment.RequestedShipment.ShippingChargesPayment.PaymentType = 'SENDER'

		# Specifies the label type to be returned.
		# LABEL_DATA_ONLY or COMMON2D
		shipment.RequestedShipment.LabelSpecification.LabelFormatType = 'COMMON2D'

		# Specifies which format the label file will be sent to you in.
		# DPL, EPL2, PDF, PNG, ZPLII
		shipment.RequestedShipment.LabelSpecification.ImageType = GENERATE_IMAGE_TYPE

		# To use doctab stocks, you must change ImageType above to one of the
		# label printer formats (ZPLII, EPL2, DPL).
		# See documentation for paper types, there quite a few.
		shipment.RequestedShipment.LabelSpecification.LabelStockType = 'PAPER_8.5X11_TOP_HALF_LABEL'

		# This indicates if the top or bottom of the label comes out of the 
		# printer first.
		# BOTTOM_EDGE_OF_TEXT_FIRST or TOP_EDGE_OF_TEXT_FIRST
		# Timestamp in YYYY-MM-DDThh:mm:ss format, e.g. 2002-05-30T09:00:00
		shipment.RequestedShipment.ShipTimestamp = datetime.datetime.now().replace(microsecond=0).isoformat()

		# BOTTOM_EDGE_OF_TEXT_FIRST, TOP_EDGE_OF_TEXT_FIRST
		shipment.RequestedShipment.LabelSpecification.LabelPrintingOrientation = 'TOP_EDGE_OF_TEXT_FIRST'

		# Delete the flags we don't want.
		# Can be SHIPPING_LABEL_FIRST, SHIPPING_LABEL_LAST or delete
		if hasattr(shipment.RequestedShipment.LabelSpecification, 'LabelOrder'):
		    del shipment.RequestedShipment.LabelSpecification.LabelOrder  # Delete, not using.


		# Insured Value
		# package1_insure = shipment.create_wsdl_object_of_type('Money')
		# package1_insure.Currency = 'USD'
		# package1_insure.Amount = 1.0

		# Create PackageLineItem
		package1 = shipment.create_wsdl_object_of_type('RequestedPackageLineItem')
		# BAG, BARREL, BASKET, BOX, BUCKET, BUNDLE, CARTON, CASE, CONTAINER, ENVELOPE etc..
		package1.PhysicalPackaging = 'BOX'
		package1.Weight = package1_weight

		# Add Insured and Total Insured values.
		# package1.InsuredValue = package1_insure
		# shipment.RequestedShipment.TotalInsuredValue = package1_insure

		# Add customer reference
		customer_reference = shipment.create_wsdl_object_of_type('CustomerReference')
		customer_reference.CustomerReferenceType="CUSTOMER_REFERENCE"
		customer_reference.Value = str(order.delivery.name+" "+order.delivery.city)
		package1.CustomerReferences.append(customer_reference)

		# Add department number
		department_number = shipment.create_wsdl_object_of_type('CustomerReference')
		department_number.CustomerReferenceType="DEPARTMENT_NUMBER"
		department_number.Value = "support@oldlappy.com"
		package1.CustomerReferences.append(department_number)

		# Add invoice number
		# invoice_number = shipment.create_wsdl_object_of_type('CustomerReference')
		# invoice_number.CustomerReferenceType="INVOICE_NUMBER"
		# invoice_number.Value = "your invoice number"
		# package1.CustomerReferences.append(invoice_number)

		# Add a signature option for the package using SpecialServicesRequested or comment out.
		# SpecialServiceTypes can be APPOINTMENT_DELIVERY, COD, DANGEROUS_GOODS, DRY_ICE, SIGNATURE_OPTION etc..
		package1.SpecialServicesRequested.SpecialServiceTypes = 'SIGNATURE_OPTION'
		# SignatureOptionType can be ADULT, DIRECT, INDIRECT, NO_SIGNATURE_REQUIRED, SERVICE_DEFAULT
		package1.SpecialServicesRequested.SignatureOptionDetail.OptionType = 'SERVICE_DEFAULT'
		# shipment.RequestedShipment.SpecialServicesRequested.CodDetail.AddTransportationChargesDetail.RateTypeBasis = 'ACCOUNT'
		# shipment.RequestedShipment.SpecialServicesRequested.CodDetail.AddTransportationChargesDetail.ChargeBasisLevel = 'CURRENT_PACKAGE'
		# shipment.RequestedShipment.SpecialServicesRequested.CodDetail.CodRecipient.Contact = 'Murli Aggarwal'
		# shipment.RequestedShipment.SpecialServicesRequested.CodDetail.CodRecipient.City = 'New Delhi'
		# shipment.RequestedShipment.SpecialServicesRequested.CodDetail.CodRecipient.Country = 'India'
		# shipment.RequestedShipment.SpecialServicesRequested.CodDetail.CodRecipient.State = 'Delhi'
		# shipment.RequestedShipment.SpecialServicesRequested.CodDetail.CodRecipient.PostalCode = '110085'
		# shipment.RequestedShipment.SpecialServicesRequested.CodDetail.CodRecipient.Phone = '9891413700'
		# shipment.RequestedShipment.SpecialServicesRequested.CodDetail.CodRecipient.RemitToName = 'Honest Computers'


		if(order.payment_mode)=='cod':
			shipment.RequestedShipment.SpecialServicesRequested.SpecialServiceTypes = 'COD'
			package1.SpecialServicesRequested.CodDetail.CodCollectionAmount.Currency = 'INR'
			package1.SpecialServicesRequested.CodDetail.CodCollectionAmount.Amount = int(order.amount)
			shipment.RequestedShipment.SpecialServicesRequested.CodDetail.CodCollectionAmount.Currency = 'INR'
			shipment.RequestedShipment.SpecialServicesRequested.CodDetail.CodCollectionAmount.Amount = int(order.amount)
			shipment.RequestedShipment.SpecialServicesRequested.CodDetail.CollectionType = 'CASH'
			package1.SpecialServicesRequested.CodDetail.CollectionType = 'CASH'




		# Un-comment this to see the other variables you may set on a package.
		# print(package1)

		# This adds the RequestedPackageLineItem WSDL object to the shipment. It
		# increments the package count and total weight of the shipment for you.
		shipment.add_package(package1)

		# If you'd like to see some documentation on the ship service WSDL, un-comment
		# this line. (Spammy).
		# print(shipment.client)

		# Un-comment this to see your complete, ready-to-send request as it stands
		# before it is actually sent. This is useful for seeing what values you can
		# change.
		# print(shipment.RequestedShipment)
		# print(shipment.ClientDetail)
		# print(shipment.TransactionDetail)

		# If you want to make sure that all of your entered details are valid, you
		# can call this and parse it just like you would via send_request(). If
		# shipment.response.HighestSeverity == "SUCCESS", your shipment is valid.
		# print(shipment.send_validation_request())

		# Fires off the request, sets the 'response' attribute on the object.
		shipment.send_request()

		# This will show the reply to your shipment being sent. You can access the
		# attributes through the response attribute on the request object. This is
		# good to un-comment to see the variables returned by the Fedex reply.
		# print(shipment.response)

		# This will convert the response to a python dict object. To
		# make it easier to work with. Also see basic_sobject_to_dict, it's faster but lacks options.
		from fedex.tools.conversion import basic_sobject_to_dict
		response_dict = basic_sobject_to_dict(shipment.response)
		response_dict['CompletedShipmentDetail']['CompletedPackageDetails'][0]['Label']['Parts'][0]['Image'] = ''
		print(response_dict)  # Image is empty string for display purposes.

		# This will dump the response data dict to json.
		# from fedex.tools.conversion import sobject_to_json
		# print(sobject_to_json(shipment.response))

		# Here is the overall end result of the query.
		print("HighestSeverity: {}".format(shipment.response.HighestSeverity))

		# Getting the tracking number from the new shipment.
		print("Tracking #: {}"
		      "".format(shipment.response.CompletedShipmentDetail.CompletedPackageDetails[0].TrackingIds[0].TrackingNumber))

		# Net shipping costs. Only show if available. Sometimes sandbox will not include this in the response.
		CompletedPackageDetails = shipment.response.CompletedShipmentDetail.CompletedPackageDetails[0]
		if hasattr(CompletedPackageDetails, 'PackageRating'):
		    print("Net Shipping Cost (US$): {}"
		          "".format(CompletedPackageDetails.PackageRating.PackageRateDetails[0].NetCharge.Amount))
		else:
		    print('WARNING: Unable to get shipping rate.')

		# Get the label image in ASCII format from the reply. Note the list indices
		# we're using. You'll need to adjust or iterate through these if your shipment
		# has multiple packages.

		ascii_label_data = shipment.response.CompletedShipmentDetail.CompletedPackageDetails[0].Label.Parts[0].Image

		# Convert the ASCII data to binary.
		label_binary_data = binascii.a2b_base64(ascii_label_data)

		"""
		This is an example of how to dump a label to a local file.
		"""
		# This will be the file we write the label out to.
		out_path = str(shipment.response.CompletedShipmentDetail.CompletedPackageDetails[0].TrackingIds[0].TrackingNumber)+'.pdf'
		print("Writing to file {}".format(out_path))
		out_file = open(out_path, 'wb')
		out_file.write(label_binary_data)
		out_file.close()
		return HttpResponse(label_binary_data, content_type='application/pdf')



		"""
		This is an example of how to print the label to a serial printer. This will not
		work for all label printers, consult your printer's documentation for more
		details on what formats it can accept.
		"""
		# Pipe the binary directly to the label printer. Works under Linux
		# without requiring PySerial. This WILL NOT work on other platforms.
		# label_printer = open("/dev/ttyS0", "w")
		# label_printer.write(label_binary_data)
		# label_printer.close()

		"""
		This is a potential cross-platform solution using pySerial. This has not been
		tested in a long time and may or may not work. For Windows, Mac, and other
		platforms, you may want to go this route.
		"""
		# import serial
		# label_printer = serial.Serial(0)
		# print("SELECTED SERIAL PORT: "+ label_printer.portstr)
		# label_printer.write(label_binary_data)
		# label_printer.close()
		# return HttpResponse('Shipment Created Succesfully! Tracking Number : ' + str(shipment.response.CompletedShipmentDetail.CompletedPackageDetails[0].TrackingIds[0].TrackingNumber))


	elif courier =='DelhiverySF':
		import requests
		import json
		surface_token='***REMOVED***'#production
		if(order.payment_mode=='cod'):
			payment = 'COD'
		else:
			payment = 'Prepaid'

		send_data={
  			"shipments": [
		    {
		      "city": order.delivery.city,
		      "commodity_value": order.amount,
		      "weight": int(order.product.weight*1000),
		      "add": order.delivery.address,
		      "phone": order.delivery.phone,
		      "payment_mode": payment,
		      "name": order.delivery.name,
		      "seller_name": "Honest Computers",
		      "return_city": "New Delhi",
		      "return_phone": "9891413700",
		      "cod_amount": order.amount,
		      "products_desc": order.product.name,
		      "pin": order.delivery.pincode,
		      "state": order.delivery.state,
		      "total_amount": order.amount,
		      "seller_add": "D-12/79, Sector-7, Rohini, Delhi",
		      "country": "India",
		      "client": "HONESTCOMPUTERS SURFACE",
		      "order": "test",
		    }
		  ],
			  "pickup_location": 
			    {
			      # "city": "Delhi",
			      "name": "HONESTCOMPUTERS SURFACE-DEL-Honest Computers",
			      # "pin": "110085",
			      # "country": "India",
			      # "phone": "9891413700",
			      # "add": "D-12/79, Sector-7, Rohini, Delhi"
		    	}
		}

		headers = {'content-type' : 'application/json','Authorization' : 'Token '+surface_token}
		response=requests.post('https://track.delhivery.com/api/cmu/create.json',data='format=json&data='+str(json.dumps(send_data)),headers=headers)
		print(json.dumps(send_data))
		response_data = response.json()
		waybill = response_data['packages'][0]['waybill']

		shipment = Shipment()
		shipment.order = order
		shipment.awb = waybill
		shipment.courier = courier
		shipment.save()

		headers = {'content-type' : 'application/json','Authorization' : 'Token '+surface_token}
		response=requests.get('https://staging-express.delhivery.com/api/p/packing_slip?wbns'+str(waybill),headers=headers)


		# return HttpResponse(label_binary_data, content_type='application/pdf')
		return redirect('/displayshipments/'+ str(shipment.id))

		return HttpResponse()



	elif courier == 'Delhivery5KG':
		import requests
		surface_token='***REMOVED***'
		heavy_token='***REMOVED***'
		if(order.payment_mode=='cod'):
			return HttpResponse('delhivery 5kg cod part')
		else:
			return HttpResponse("delhivery 5 kg prepaid part")

def DisplayShipments(request):
	shipments=Shipment.objects.all()
	data = {}
	data['shipments'] = shipments
	return render(request,'main/DisplayShipments.html',data)

def DisplayShipmentDetail(request,sid):
	shipment=Shipment.objects.filter(id=sid).first()
	data = {}
	data['shipment'] = shipment
	return render(request,'main/DisplayShipmentDetail.html',data)

def LabelTesting(request):
	import requests
	order = Order.objects.filter(id=2).first()
	courier = 'DelhiverySF'
	surface_token='***REMOVED***'#production
	from main.utils import render_to_pdf
	headers = {'content-type' : 'application/json','Authorization' : 'Token '+surface_token}
	response = requests.get('https://track.delhivery.com/api/p/packing_slip?wbns='+'1784510013451',headers=headers)
	label_data = response.json()
	sbarcode = label_data['packages'][0]['barcode']
	obarcode = label_data['packages'][0]['oid_barcode']
	destination_dc = label_data['packages'][0]['destination']
	routing_code = label_data['packages'][0]['sort_code']
	if (order.payment_mode=='cod'):
		payment_mode = 'Cash On Delivery'
	else:
		payment_mode = 'Pre-Paid'
	data = {}
	data['shipment_barcode'] = sbarcode
	data['order_barcode'] = obarcode
	data['destination_dc'] = destination_dc
	data['routing_code'] = routing_code
	data['order'] = order
	data['payment_mode'] = payment_mode
	data['rupees'] = '''data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGwAAACgCAMAAADeknkwAAAAY1BMVEX///8BAQEAAADt7e0bGxssLCzf398VFRXAwMCgoKD6+vrq6uojIyPT09P19fWSkpLGxsa3t7cNDQ1bW1usrKxCQkIxMTGBgYFpaWl0dHTMzMw6OjpJSUl7e3umpqZWVlaKiop6N8GrAAAEg0lEQVR4nN1bW5uqMAws0QW5iIKA4A3//688oGehK4lYttOHnRd9EOZLCOlMWpX6xpY8KIh2A1daktfR9Ywff5j9uIwGsh08sL2WRDTZfeBSCZrrS0+iUf7Nn5nTJF4HrqhEc53TH0lEppHoNHD58CQ2YyWe0Vz5yBWatw6jNBJtnCWR9CSWxMP0liKqsRJvFLwgz3NjYsqT19t8Q3udlS9gu91uit21rZIH9cwzozyLpTspA0T+Jmxm46N1NH+rT+GH9Vs+ooM9sp5vVz3o+NInKqyyqah4ExwlsV22vgOIdFTbJlP+mYhLY5/JrXW2qJZi0xYte7iLbCsA21Fg05ShRbR816dLOn+tMVa8GEOUSIc9n0g6IshUTUwauzxCyPgll5JPe3y8MkB0YMkoky+JtXZ2Cr4MUCW86kjkS5LbwJWe36zsn8uGd/JgXPGOaD2nvRZCLVsk07rLGim/+7gql75zTKJL35lesC6mM++pwySeHCZxrMTozDZVi2kMxqoP4Ul0ad6PP5K4EHwYE2jmPaT1QuTs7CR5/ZlumYxWMR3plQmNrunkh8oGuHXCtrsY0EzTqBeeVfQ9bhKYfSfzRMyUI5UYrn7MO03jHUR2ZwLDKGLVz0+mZGeE1u9w4h7ZHcPVFf5UZ5DRzONzOK3FZkrWaW8M15aYBbfCcHFDZVhgbMNvMVzFOArRxkmYF5p9xSBDEKU2nCCgBMJVsFyYJIbakjl8I7rNX2mMFTu4wjywGyvgCFH1p5a4SSrRxeJ8+In9gdelZH0V88NclMBWc5j6YRvw06Oey96wNj2FTfl27GE+YvSzzU9kRRHumvKNg3hSaZbyY4QmRkWjOizRpAzZvKfs2saikl9gPrvKWCi1Tcm6qNoFT2sgM3DuHcrN8qZhEllvXH9BZUDWMeXHXy5dn6TxgeSQ/dq2zkf2oDpkNvS1RDa+dkkd2lr4BbKOJKgudRPuVxZXLOGZUeH7sXXLJUVWIcxdIaURsd2xKoVjNZAdMc7bPWPbzF9sDE6/P9kQUncnnR+ATABqKTS7+/j/UUlsiCLxc5dFkgknoihAzDekzQR918YexCKxf0ZBqSiQVEcIYJPORWHmsZnIhikSYWcGUiStFBvCN6fSiVFIkWw9x52EfwMCxNRePMkCGZUymxFPtmb+WmPEFW8GMWMjtypB7iSw406cmWkBmkQ8yAw5FCQcd/Iwy420p4wpkpukyROHUtKjFrDcRK2USESR+ImgySFbxHInQaiEm8T2hegktSSTEX4jFToJQTY4Y9FvIPbLpMNmMCnJL6UlpkjY0P5EkfCanHCmlI0thxUJx4ZabqZpRE0uVuLk4g+b0jVCk9xfx1vf30qMKWVDQ/y7otMkbqUkn0ZQkbB7/R7KlMqdBCElD9zZAg+045+K7zZCSsp+w2mRrDGTC+aZ9aFBJhdOTWksdhLU5IIXJYs3lN9A9Bs5QiVcJTb7p17Us0hYd4MypXyRIDqJ7DdwkwuODWVKWXdTI5Yb6S/mGL8RuOwke2nHAWJKQ1ElcEXyDw0zQkCP45K4AAAAAElFTkSuQmCC'''
	data['oldlappy_logo'] = '''data:image/png;base64,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'''
	data['courier_logo'] = '''data:image/png;base64,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wAAAAAAATyAAAwAAAAA8gQAMAAAAAPAEAjAAAAAAwBMIwAAAAAAATyAAAwAAAAA8gQAMAAAAAPAEAjAAAAAAwBMIwAAAAAAATyAAAwAAAAA8gQAMAAAAAPAEAjAAAAAAwBMIwAAAAAAATyAAAwAAAAA8gQAMAAAAAPAEAjAAAAAAwBMIwAAAAAAATyAAAwAAAAA8gQAMAAAAAPAEAjAAAAAAwBMIwAAAAAAATyAAAwAAAAA8gQAMAAAAAPAEAjAAAAAAwBMIwAAAAAAATyAAAwAAAAA8gQAMAAAAAPAEAjAAAAAAwBMIwAAAAAAATyAAAwAAAAA8gQAMAAAAAPAEAjAAAAAAwBMIwAAAAAAATyAAAwAAAAA8gQAMAAAAAPAEAjAAAAAAwBMIwAAAAAAATyAAAwAAAAA8gQAMAAAAAPAEAjAAAAAAwBMIwAAAAAAATyAAAwAAAAA8gQAMAAAAAPAEAjAAAAAAwBMIwAAAAAAATyAAAwAAAAA8gQAMAAAAAPAEAjAAAAAAwBMIwAAAAAAATyAAAwAAAAA8gQAMAAAAAPAEAjAAAAAAwBMIwAAAAAAATyAAAwAAAAA8gQAMAAAAAPAEAjAAAAAAwBMIwAAAAAAATyAAAwAAAAA8gQAMAAAAAPAEAjAAAAAAwBMIwAAAAAAATyAAAwAAAAA8gQAMAAAAAPAEAjAAAAAAwBMIwAAAAAAATyAAAwAAAAA8gQAMAAAAAPAEAjAAAAAAwBMIwAAAAAAATyAAAwAAAAA8gQAMAAAAAPAEAjAAAAAAwBMIwAAAAAAATyAAAwAAAAA8gQAMAAAAAPAEAjAAAAAAwBMIwAAAAAAATyAAAwAAAAA8gQAMAAAAAPAEAjAAAAAAwBMIwAAAAAAATyAAAwAAAAA8gQAMAAAAAPAEAjAAAAAAwBMIwAAAAAAATyAAAwAAAAA8gQAMAAAAAPAEAjAAAAAAwBMIwAAAAAAATyAAAwAAAAA8gQAMAAAAAPAEAjAAAAAAwBMIwAAAAAAADxD5/0lkIeBE+EdWAAAAAElFTkSuQmCC'''

	# return HttpResponse(label_data)
	# return render(request,'pdf/label.html',data)
	pdf = render_to_pdf('pdf/label.html',data)
	return HttpResponse(pdf, content_type='application/pdf')