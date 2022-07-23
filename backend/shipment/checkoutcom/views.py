import base64
import urllib.parse
import logging
import time
import io

import checkout_sdk as sdk

import requests

from rest_framework.permissions import IsAuthenticated
from rest_framework import status as rest_framework_status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.conf import settings
from django.core.files import File

from orders.models import Quotation
from checkoutdetails.signals import quotation_status_changed
from payment.models import PaymentTransaction
from users.models import CustomUser
from shipping.models import Shipping, ImageShippings

logger = logging.getLogger(__name__)


class CheckoutcomPay(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, quotation_id=None):

        quotation = Quotation.objects.get(id=quotation_id)

        dhl_carrier = CustomUser.objects.get(username="DHL")
        aramex_carrier = CustomUser.objects.get(username="aramex")

        api = sdk.get_api(
            secret_key=settings.CHECKOUTCOM_SECRET_KEY,
            public_key=settings.CHECKOUTCOM_PUBLIC_KEY,
        )

        try:
            payment = api.payments.request(
                source={
                    "token": request.data["token"],
                },
                amount=int(quotation.total_cost * 100),  # cents
                currency=sdk.Currency.USD,
                reference="pay_ref",
            )
        except sdk.errors.CheckoutSdkError as e:
            logger.error(
                "{0.http_status} {0.error_type} {0.elapsed} {0.request_id}".format(e)
            )
        else:
            if payment.http_response.body.get("status") and payment.http_response.body.get("response_code"):
                logger.warning(f"data from checkout.com - {payment.http_response.body}")
                payment_transaction_object = PaymentTransaction.objects\
                    .create(status=payment.http_response.body["status"],
                            response_code=payment.http_response.body["response_code"])

                status = None
                if payment.http_response.body["status"] == "Paid":
                    status = Quotation.STATUS.PAYED
                    if quotation.carrier.pk == dhl_carrier.pk:
                        order = quotation.order

                        plannedShippingDateAndTime = order.eta.strftime("%Y-%m-%dT12:00:00")

                        request_json = {
                            "plannedShippingDateAndTime": plannedShippingDateAndTime,
                            "pickup": {
                                "isRequested": False,
                            },
                            "productCode": "D",
                            "accounts": [
                                {
                                    "typeCode": "shipper",
                                    "number": "123456789"
                                }
                            ],
                            "customerDetails": {
                                "shipperDetails": {
                                    "postalAddress": {
                                        "postalCode": order.origin_city.post_code1,
                                        "cityName": order.origin_city.city_name,
                                        "countryCode": order.origin_city.country,
                                        "addressLine1": f"{order.shipment_origin.house}  {order.shipment_origin.street}"
                                    },
                                    "contactInformation": {
                                        "phone": "+1123456789",
                                        "companyName": "Company Name",
                                        "fullName": "John Brew"
                                    }
                                },
                                "receiverDetails": {
                                    "postalAddress": {
                                        "postalCode": order.destination_city.post_code1,
                                        "cityName": order.destination_city.city_name,
                                        "countryCode": order.destination_city.country,
                                        "addressLine1": f"{order.shipment_destination.house}  "
                                                        f"{order.shipment_destination.street}"
                                    },
                                    "contactInformation": {
                                        "phone": "+1123456789",
                                        "companyName": "Company Name",
                                        "fullName": "John Brew"
                                    }
                                }
                            },
                            "content": {
                                "unitOfMeasurement": "metric",
                                "packages": [

                                ],
                                "isCustomsDeclarable": False,
                                "description": order.description,
                                "incoterm": "DAP"
                            },
                        }

                        for package in order.packages.all():
                            request_json["content"]["packages"].append(
                                {
                                    "weight": package.weight,
                                    "dimensions": {
                                        "length": package.length,
                                        "width": package.width,
                                        "height": package.height
                                    }
                                }
                            )

                        dhl_url = urllib.parse.urljoin(settings.DHL_API_URL, settings.DHL_API_URN_SHIPMENTS)

                        headers = {'Authorization': settings.DHL_AUTH}

                        response = requests.post(dhl_url, data=request_json, headers=headers)

                        try:
                            response.raise_for_status()
                        except Exception as e:
                            logger.warning(f"{e} -  {response.json()}")
                        else:
                            tracking_number = response.json()["shipmentTrackingNumber"]
                            shipping = Shipping.objects.create(tracking_number=tracking_number, order=quotation.order)

                            for doc in response.json()["documents"]:
                                extension = doc["imageFormat"].lower()
                                name = f"{int(time.time() * 1000)}_order_{order.pk}_{doc['typeCode']}"
                                full_name = name + "." + extension

                                try:
                                    file = File(io.BytesIO(base64.b64decode(doc["content"].encode())), name=full_name)
                                except Exception as e:
                                    logger.error(f"Creation of file - {e}")
                                else:
                                    ImageShippings.objects.create(shipping=shipping, file=file)

                if status:
                    Quotation.objects.filter(pk=quotation.pk).update(status=status)
                    quotation.refresh_from_db()
                    quotation_status_changed.send(sender=Quotation, quotation=quotation,
                                                  payment_transaction=payment_transaction_object)
                else:
                    logger.error(f"status from checkout.com - {payment.http_response.body['status']}")
                    logger.error(f"data from checkout.com - {payment.http_response.body}")

        return Response(payment.http_response.body, status=rest_framework_status.HTTP_200_OK)
