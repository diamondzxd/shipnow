# Shipnow
 
## Shipnow Logistics Aggregator Platform

![shipnow index](https://i.imgur.com/BvmUE8C.png)

<hr>

### This is a logistics aggregator platform.

It takes input from the user through the Add Order form.  
  
After getting the order, the user can ship that order, find a list of courier companies along with their services and prices, choose the best option, and Click on Ship Now.  
  
After getting a shipping request, the application sends the Order data to the courier through APIs, and fetches the Waybill and generates the Shipping Label accordingly, saves it on the Storage and makes it available for the user to download and print that.  
  
It also allows to Generate the Invoice corresponding to that Order.

## How do I self host this myself?

This project can be easily built and ran as a container.

Steps to do that (Make sure docker and docker compose plugin is installed in the system):

```bash
git clone https://github.com/diamondzxd/shipnow
cd shipnow
docker compose build
docker compose up
```

The app will start on https://127.0.0.1:8000 :)

## Live Link

http://test.shipnow.co.in:8000

<hr>

## Some more screenshots

![shipnow add order](https://i.imgur.com/RzFJsA1.png)
![shipnow display shipments](https://i.imgur.com/msAsSe3.png)
![shipment detail](https://i.imgur.com/4bgnxb3.png)
![delhivery label](https://i.imgur.com/diAtz7p.png)
