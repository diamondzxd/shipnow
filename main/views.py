from django.shortcuts import render, redirect
from .forms import AddressForm,ProductForm
from .models import Address,Product,Order
from django.http import HttpResponse,JsonResponse
from django.core import serializers
import json
import datetime
# Create your views here.

#Index Page
def Index(request):
	return render(request,'main/base.html',None)

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
		return redirect('/displayorder/')

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

def CreateShipment(request,oid):
	order=Order.objects.filter(id=oid).first()
	

	#FedEx API Part

	#!/usr/bin/env python
	"""
	This example shows how to create a shipment and generate a waybill as output. The variables populated below
	represents the minimum required values. You will need to fill all of these, or
	risk seeing a SchemaValidationError exception thrown.

	Near the bottom of the module, you'll see some different ways to handle the
	label data that is returned with the reply.
	"""
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
	shipment.RequestedShipment.Shipper.Address.StreetLines = [order.pickup.address]
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
	shipment.RequestedShipment.Recipient.Address.StreetLines = [order.delivery.address]
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
	shipment.RequestedShipment.LabelSpecification.LabelStockType = 'PAPER_7X4.75'

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
	customer_reference.Value = "test-1"
	package1.CustomerReferences.append(customer_reference)

	# Add department number
	# department_number = shipment.create_wsdl_object_of_type('CustomerReference')
	# department_number.CustomerReferenceType="DEPARTMENT_NUMBER"
	# department_number.Value = "your department number"
	# package1.CustomerReferences.append(department_number)

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
	#package1.SPecialServicesRequested.SpecialServiceTypes = 'COD'

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
	# from fedex.tools.conversion import sobject_to_dict
	# response_dict = sobject_to_dict(shipment.response)
	# response_dict['CompletedShipmentDetail']['CompletedPackageDetails'][0]['Label']['Parts'][0]['Image'] = ''
	# print(response_dict)  # Image is empty string for display purposes.

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
	return HttpResponse('Shipment Created Succesfully! Tracking Number : ' + str(shipment.response.CompletedShipmentDetail.CompletedPackageDetails[0].TrackingIds[0].TrackingNumber))

def DeleteOrder(request,id):
	try:
		a=Order.objects.filter(id=id)
		a.delete()
		return redirect('/displayorder')
	except:
		return HttpResponse("Order does not Exists!")