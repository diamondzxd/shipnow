#!/usr/bin/env python
"""
This example shows how to create a pickup request
"""
import datetime
import sys
import logging

from example_config_flat import CONFIG_OBJ
from fedex.services.pickup_service import FedexCreatePickupRequest

customer_transaction_id = "*** PickupService Request v11 using Python ***"  # Optional transaction_id
pickup_service = FedexCreatePickupRequest(CONFIG_OBJ, customer_transaction_id)

pickup_service.OriginDetail.PickupLocation.Contact.PersonName = 'Murli Aggarwal'
pickup_service.OriginDetail.PickupLocation.Contact.EMailAddress = 'admin@oldlappy.com'
pickup_service.OriginDetail.PickupLocation.Contact.CompanyName = 'Honest Computers'
pickup_service.OriginDetail.PickupLocation.Contact.PhoneNumber = '9891413700'
pickup_service.OriginDetail.PickupLocation.Address.StateOrProvinceCode = 'DL'
pickup_service.OriginDetail.PickupLocation.Address.PostalCode = '110085'
pickup_service.OriginDetail.PickupLocation.Address.CountryCode = 'IN'
pickup_service.OriginDetail.PickupLocation.Address.StreetLines = ['D-12/79, Sec-7, Rohini', 'Delhi']
pickup_service.OriginDetail.PickupLocation.Address.City = 'New Delhi'
# pickup_service.OriginDetail.PickupLocation.Address.UrbanizationCode = ''  # For Puerto Rico only
pickup_service.OriginDetail.PickupLocation.Address.Residential = False

# FRONT, NONE, REAR, SIDE
pickup_service.OriginDetail.PackageLocation = 'FRONT'

# APARTMENT, BUILDING, DEPARTMENT, FLOOR, ROOM, SUITE
pickup_service.OriginDetail.BuildingPart = 'BUILDING'

# Identifies the date and time the package will be ready for pickup by FedEx.
pickup_service.OriginDetail.ReadyTimestamp = datetime.datetime.now().replace(microsecond=0).isoformat()
#pickup_service.OriginDetail.ReadyTimestamp = '2019-08-10T12:00:00'

# Identifies the latest time at which the driver can gain access to pick up the package(s)
pickup_service.OriginDetail.CompanyCloseTime = '19:00:00'

pickup_service.CarrierCode = 'FDXE'

pickup_service.TotalWeight.Units = 'KG'
pickup_service.TotalWeight.Value = '20'
pickup_service.PackageCount = '3'
# pickup_service.OversizePackageCount = '1'

pickup_service.CommodityDescription = 'package'

# DOMESTIC or INTERNATIONAL
pickup_service.CountryRelationship = 'DOMESTIC'

# See PickupServiceCategoryType
# pickup_service.PickupServiceCategory = 'FEDEX_DISTANCE_DEFERRED'
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

print(pickup_service.TransactionDetail)
print(pickup_service.ClientDetail)
pickup_service.send_request()

print (pickup_service.response.HighestSeverity == 'SUCCESS')
print (pickup_service.response.Notifications[0].Message)
