import urllib.parse

from suds.client import Client
import requests
import logging
from celery import shared_task

from django.conf import settings

from orders.models import Order, Quotation
from users.models import CustomUser
from location.models import ServiceProvider

logger = logging.getLogger(__name__)


@shared_task
def aramex_quote(order_id):
    order_qs = Order.objects.filter(id=order_id)


    if order_qs:
        order = order_qs[0]

        rate_client = Client(
            settings.ARAMEX_RATE_CALCULATOR_URL, cache=None)

        shipping_client = Client(
            settings.ARAMEX_SHIPPING_URL, cache=None)

        # origin address
        aramex_origin_address = shipping_client.factory.create("Address")

        aramex_origin_address.Line1 = "ABC Street"
        aramex_origin_address.Line2 = "Unit # 1"
        aramex_origin_address.Line3 = ""
        aramex_origin_address.City = "Amman"
        aramex_origin_address.StateOrProvinceCode = ""
        aramex_origin_address.PostCode = ""
        aramex_origin_address.CountryCode = "JO"
        aramex_origin_address.Longitude = 0
        aramex_origin_address.Latitude = 0
        aramex_origin_address.BuildingNumber = None
        aramex_origin_address.BuildingName = None
        aramex_origin_address.Floor = None
        aramex_origin_address.Apartment = None
        aramex_origin_address.POBox = None
        aramex_origin_address.Description = None

        # destination address
        aramex_destination_address = shipping_client.factory.create("Address")

        aramex_destination_address.Line1 = "XYZ Street"
        aramex_destination_address.Line2 = "Unit # 1"
        aramex_destination_address.Line3 = ""
        aramex_destination_address.City = "Dubai"
        aramex_destination_address.StateOrProvinceCode = ""
        aramex_destination_address.PostCode = ""
        aramex_destination_address.CountryCode = "AE"
        aramex_destination_address.Longitude = 0
        aramex_destination_address.Latitude = 0
        aramex_destination_address.BuildingNumber = None
        aramex_destination_address.BuildingName = None
        aramex_destination_address.Floor = None
        aramex_destination_address.Apartment = None
        aramex_destination_address.POBox = None
        aramex_destination_address.Description = None

        # ShipmentDetails
        aramex_shipment_details = shipping_client.factory.create("ShipmentDetails")
        ## ShipmentDetails: Dimensions (null)
        # aramex_dimensions = shipping_client.factory.create("Dimensions")
        # aramex_dimensions.Length = 1
        # aramex_dimensions.Width = 1
        # aramex_dimensions.Height = 1
        # aramex_dimensions.Unit = "CM"

        # aramex_shipment_details.Dimensions = aramex_dimensions
        aramex_shipment_details.Dimensions = None

        ## ShipmentDetails: ActualWeight
        aramex_weight = shipping_client.factory.create("Weight")

        aramex_weight.Unit = "KG"
        aramex_weight.Value = 1

        aramex_shipment_details.ActualWeight = aramex_weight

        ## ShipmentDetails: ChargeableWeight (null)
        # aramex_weight = shipping_client.factory.create("Weight")

        # aramex_weight.Unit = "KG"
        # aramex_weight.Value = 1

        # aramex_shipment_details.ChargeableWeight = aramex_weight
        aramex_shipment_details.ChargeableWeight = None

        ## ShipmentDetails: ProductGroup
        aramex_shipment_details.ProductGroup = "EXP"

        ## ShipmentDetails: ProductType
        aramex_shipment_details.ProductType = "PPX"

        ## ShipmentDetails: PaymentType
        aramex_shipment_details.PaymentType = "P"

        ## ShipmentDetails: PaymentOptions
        aramex_shipment_details.PaymentOptions = ""

        ## ShipmentDetails: Services
        aramex_shipment_details.Services = ""

        ## ShipmentDetails: NumberOfPieces
        aramex_shipment_details.NumberOfPieces = 1

        ## ShipmentDetails: DescriptionOfGoods
        aramex_shipment_details.DescriptionOfGoods = None

        ## ShipmentDetails: GoodsOriginCountry
        aramex_shipment_details.GoodsOriginCountry = None

        ## ShipmentDetails: CashOnDeliveryAmount (null)
        # aramex_money = shipping_client.factory.create("Money")
        # aramex_money.Value = 0.0
        # aramex_money.CurrencyCode =
        aramex_shipment_details.CashOnDeliveryAmount = None

        ## ShipmentDetails: InsuranceAmount
        # aramex_money = shipping_client.factory.create("Money")
        # aramex_money.Value = 0.0
        # aramex_money.CurrencyCode =
        aramex_shipment_details.InsuranceAmount = None

        ## ShipmentDetails: CustomsValueAmount
        # aramex_money = shipping_client.factory.create("Money")
        # aramex_money.Value = 0.0
        # aramex_money.CurrencyCode =
        aramex_shipment_details.CustomsValueAmount = None

        ## ShipmentDetails: CashAdditionalAmount
        # aramex_money = shipping_client.factory.create("Money")
        # aramex_money.Value = 0.0
        # aramex_money.CurrencyCode =
        aramex_shipment_details.CashAdditionalAmount = None

        ## ShipmentDetails: CollectAmount
        # aramex_money = shipping_client.factory.create("Money")
        # aramex_money.Value = 0.0
        # aramex_money.CurrencyCode =
        aramex_shipment_details.CollectAmount = None

        ## ShipmentDetails: Items (null)
        # aramex_items = shipping_client.factory.create("ShipmentItem")
        # aramex_items.Quantity =
        # aramex_items.Comments =
        # aramex_items.Reference =
        # aramex_items.Weight =
        aramex_shipment_details.Items = None


        # Transaction
        aramex_transaction = shipping_client.factory.create("Transaction")
        aramex_transaction.Reference1 = ""
        aramex_transaction.Reference2 = ""
        aramex_transaction.Reference3 = ""
        aramex_transaction.Reference4 = ""
        aramex_transaction.Reference5 = ""

        # ClientInfo
        aramex_client_info = shipping_client.factory.create("ClientInfo")

        aramex_client_info.AccountCountryCode = settings.ARAMEX_ACCOUNT_COUNTRY_CODE
        aramex_client_info.AccountEntity = settings.ARAMEX_ACCOUNT_ENTITY
        aramex_client_info.AccountNumber = settings.ARAMEX_ACCOUNT_NUMBER
        aramex_client_info.AccountPin = settings.ARAMEX_ACCOUNT_PIN
        aramex_client_info.UserName = settings.ARAMEX_USERNAME
        aramex_client_info.Password = settings.ARAMEX_PASSWORD
        aramex_client_info.Version = "1.0"
        aramex_client_info.Source = 24

        # RATE
        rate = rate_client.service.CalculateRate(
            aramex_client_info,
            aramex_transaction,
            aramex_origin_address,
            aramex_destination_address,
            aramex_shipment_details,
            "USD"
        )


        user = CustomUser.objects.get(username="aramex")

        aramex_quote = Quotation(
            carrier=user,
            order=order,
            total_cost=rate.TotalAmount.Value,
        )

        aramex_quote.save()


@shared_task
def dhl_quote(order_id):
    order = Order.objects.filter(id=order_id).first()

    service_provider = ServiceProvider.objects.get(name="DHL")

    origin_city = order.origin_city
    destination_city = order.destination_city

    if (not origin_city) or (not destination_city):
        logger.warning("origin city and destination city are required")
        return

    destination_country_code = order.destination_city.country
    origin_country_code = order.origin_city.country

    if not origin_country_code.service_provider.filter(pk=service_provider.pk):
        logger.warning(f"service provider {service_provider.name} doesn't have {origin_country_code.country_name}"
                       f" as origin country")
        return
    else:
        if not origin_city.service_provider.filter(pk=service_provider.pk):
            logger.warning(
                f"service provider {service_provider.name} - {service_provider.pk} doesn't have "
                f"{origin_city.city_name} - {origin_city.pk} as origin city for "
                f"{origin_country_code.country_name} - {origin_country_code.pk} country")
            return

    if not destination_country_code.service_provider.filter(pk=service_provider.pk):
        logger.warning(f"service provider {service_provider.name} doesn't have "
                       f"{destination_country_code.country_name} as origin country")
        return
    else:
        if not destination_city.service_provider.filter(pk=service_provider.pk):
            logger.warning(
                f"service provider {service_provider.name} - {service_provider.pk} doesn't have "
                f"{destination_city.city_name} - {destination_city.pk} as destination city for "
                f"{destination_country_code.country_name} - {destination_country_code.pk} country")
            return

    if order:
        dhl_url = urllib.parse.urljoin(settings.DHL_API_URL, settings.DHL_API_URN_RATES)

        headers = {'Authorization': settings.DHL_AUTH}

        total_cost = 0

        for package in order.packages.all(): #  because DHL works only with packages (weight, length, width and height are required)
            if package.quantity > 0:
                for q in range(package.quantity):
                    params = {
                        "accountNumber": "123456789",
                        "originCountryCode": origin_country_code.country_code,
                        "originCityName": origin_city.city_name,
                        "destinationCountryCode": destination_country_code.country_code,
                        "destinationCityName": destination_city.city_name,
                        "weight": package.weight,
                        "length": package.length,
                        "width": package.width,
                        "height": package.height,
                        "plannedShippingDate": order.cargo_ready_date,
                        "isCustomsDeclarable": "false",
                        "unitOfMeasurement": "metric"
                    }

                    response = requests.get(dhl_url, params=params, headers=headers)

                    try:
                        response.raise_for_status()
                    except Exception as e:
                        logger.warning(f"{e}  {response.json()}")
                        return

                    response_json = response.json()

                    for p in response_json["products"]:
                        for tp in p["totalPrice"]:
                            total_cost += tp["price"]

        dhl_quote_object = Quotation(
            carrier=service_provider.user,
            order=order,
            total_cost=total_cost
        )

        dhl_quote_object.save()
