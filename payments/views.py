import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import MpesaTransaction


@csrf_exempt
def mpesa_callback(request):
    data = json.loads(request.body)
    stk_callback = data["Body"]["stkCallback"]

    checkout_request_id = stk_callback["CheckoutRequestID"]
    result_code = stk_callback["ResultCode"]

    try:
        transaction = MpesaTransaction.objects.get(checkout_request_id=checkout_request_id)
    except MpesaTransaction.DoesNotExist:
        return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})

    if result_code == 0:
        metadata = stk_callback["CallbackMetadata"]["Item"]
        receipt_number = next(item["Value"] for item in metadata if item["Name"] == "MpesaReceiptNumber")
        transaction.status = "success"
        transaction.mpesa_receipt_number = receipt_number
        transaction.save()
        transaction.order.status = "paid"
        transaction.order.save()
    else:
        transaction.status = "failed"
        transaction.save()

    return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})  