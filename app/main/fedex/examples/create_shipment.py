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

from example_config_heavy import CONFIG_OBJ
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
shipment.RequestedShipment.Shipper.Contact.PersonName = 'Piyush Dhall'
shipment.RequestedShipment.Shipper.Contact.CompanyName = 'Honest Computers'
shipment.RequestedShipment.Shipper.Contact.PhoneNumber = '9654301509'

# Shipper address.
shipment.RequestedShipment.Shipper.Address.StreetLines = ['F-25/46, Sector-3, Rohini','Green View Apartments']
shipment.RequestedShipment.Shipper.Address.City = 'Delhi'
shipment.RequestedShipment.Shipper.Address.StateOrProvinceCode = 'DL'
shipment.RequestedShipment.Shipper.Address.PostalCode = '110085'
shipment.RequestedShipment.Shipper.Address.CountryCode = 'IN'
shipment.RequestedShipment.Shipper.Address.Residential = False

# Recipient contact info.
shipment.RequestedShipment.Recipient.Contact.PersonName = 'Murli Aggarwal'
shipment.RequestedShipment.Recipient.Contact.CompanyName = ''
shipment.RequestedShipment.Recipient.Contact.PhoneNumber = '9891413700'

# Recipient address
shipment.RequestedShipment.Recipient.Address.StreetLines = ['D-12/79, Sector-7, Rohini','Sai Baba Market']
shipment.RequestedShipment.Recipient.Address.City = 'Delhi'
shipment.RequestedShipment.Recipient.Address.StateOrProvinceCode = 'DL'
shipment.RequestedShipment.Recipient.Address.PostalCode = '110085'
shipment.RequestedShipment.Recipient.Address.CountryCode = 'IN'
# This is needed to ensure an accurate rate quote with the response. Use AddressValidation to get ResidentialStatus
shipment.RequestedShipment.Recipient.Address.Residential = False
shipment.RequestedShipment.EdtRequestType = 'NONE'

# Create Weight, in pounds.
package1_weight = shipment.create_wsdl_object_of_type('Weight')
package1_weight.Value = 0.5
package1_weight.Units = "KG"

quantity=1
commodity = shipment.create_wsdl_object_of_type('Commodity')
commodity.Name = "Books"
commodity.NumberOfPieces = quantity
commodity.Description = "Books for a present"
commodity.CountryOfManufacture = "IN"
commodity.Weight = package1_weight
commodity.Quantity = quantity
commodity.QuantityUnits = 'PCS' # EACH - for items measured in units
commodity.UnitPrice.Currency = "INR"
commodity.UnitPrice.Amount = 100
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
shipment.RequestedShipment.CustomsClearanceDetail.CustomsValue.Amount = 100
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
