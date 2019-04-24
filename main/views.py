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
		return HttpResponse('Record Saved Succesfully!')

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
			return HttpResponse("Data Updated Succesfully!")
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
		return HttpResponse('Record Saved Succesfully!')

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
			return HttpResponse("Data Updated Succesfully!")
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
		return redirect('createshipment/'+order.id)

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
	if(order.payment_mode=='cod'):
		return HttpResponse("This order is Cash on Delivery!")
	else:
		return HttpResponse("This order is Pre-Paid!")