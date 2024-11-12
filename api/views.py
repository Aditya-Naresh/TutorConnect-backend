from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
import environ
import razorpay

from .models import Order
from .serializers import OrderSerializer

env = environ.Env()
environ.Env.read_env()


class StartPaymentView(APIView):
    def post(self, request, *args, **kwargs):
        amount = request.data.get("amount")
        name = request.data.get("name")
        client = razorpay.Client(
            auth=(
                env("PUBLIC_KEY"),
                env("RAZORPAY_SECRET_KEY"),
            ),
        )

        payment = client.order.create(
            {
                "amount": str(int(amount) * 100),
                "currency": "INR",
                "payment_capture": "1",
            }
        )

        order = Order.objects.create(
            order_product=name,
            order_amount=amount,
            order_payment_id=payment["id"],
        )

        serializer = OrderSerializer(order)

        data = {"payment": payment, "order": serializer.data}

        return Response(data, status=status.HTTP_200_OK)


class HandlePaymentSuccessView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            res = json.loads(request.data.get("response"))
            ord_id = res.get("razorpay_order_id")
            raz_pay_id = res.get("razorpay_payment_id")
            raz_signature = res.get("razorpay_signature")

            if not ord_id or not raz_pay_id or not raz_signature:
                return Response(
                    {"error": "Invalid payment response"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                order = Order.objects.get(order_payment_id=ord_id)
            except Order.DoesNotExist:
                return Response(
                    {"error": "Order not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            data = {
                "razorpay_order_id": ord_id,
                "razorpay_payment_id": raz_pay_id,
                "razorpay_signature": raz_signature,
            }

            client = razorpay.Client(
                auth=(env("PUBLIC_KEY"), env("RAZORPAY_SECRET_KEY"))
            )

            try:
                client.utility.verify_payment_signature(data)
                order.isPaid = True
                order.save()

                return Response(
                    {"message": "Payment successfully received!"},
                    status=status.HTTP_200_OK,
                )
            except razorpay.errors.SignatureVerificationError:
                return Response(
                    {"error": "Signature verification failed"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except Exception as e:
                return Response(
                    {"error": f"Signature verification failed: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Exception as e:
            print("Execption occured: ", {str(e)})
            return Response(
                {"error": "Something went wrong while processing the payment"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
