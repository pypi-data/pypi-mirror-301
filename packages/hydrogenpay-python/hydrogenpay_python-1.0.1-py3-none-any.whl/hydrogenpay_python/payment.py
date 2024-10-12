import requests
import json
import copy
from hydrogenpay_python.base import HydrogenpayBase
from hydrogenpay_python.exceptions import HydrogenpayError, TransactionChargeError, TransactionVerificationError, TransactionValidationError, ServerError
from hydrogenpay_python.misc import checkIfParametersAreComplete
import logging

response_object = {
    "error": False,
    "transactionComplete": False,
    "txRef": "",
    "status": "",
    "currency": "",
    "chargedamount": 00,
    "chargemessage": "",
    "meta": ""
}


class Payment(HydrogenpayBase):
    """ This is the base class for all the payments """

    def __init__(self, sandboxKey, liveKey, mode, setEnv):
        # Instantiating the base class
        super(
            Payment,
            self).__init__(
            sandboxKey,
            liveKey,
            mode,
            setEnv)

    @classmethod
    def retrieve(cls, mapping, *keys):
        return (mapping[key] for key in keys)

    @classmethod
    def deleteUnnecessaryKeys(cls, response_dict, *keys):
        for key in keys:
            del response_dict[key]
        return response_dict

    def _preliminaryResponseChecks(
            self,
            response,
            TypeOfErrorToRaise,
            txRef=None):
        preliminary_error_response = copy.deepcopy(response_object)
        preliminary_error_response = Payment.deleteUnnecessaryKeys(
            preliminary_error_response,
            "transactionComplete",
            "currency")

        # Check if we can obtain a json
        try:
            responseJson = response.json()
        except BaseException:
            raise ServerError({"error": True, "txRef": txRef, "errMsg": response})

        # Check if the response contains data parameter
        if responseJson.get("data", None):
            if txRef:
                txRef = responseJson["data"].get("transactionRef", None)
                # if txRef:
                #     print(f"Extracted transactionRef: {txRef}")  # For debugging purposes
        else:
            raise TypeOfErrorToRaise({"error": True,
                                      "txRef": responseJson["data"].get("transactionRef", None),
                                      "errMsg": responseJson.get("message",
                                                                 "Server is down")})

        # Check if it is returning a 200
        if not response.ok:
            errMsg = responseJson.get("message", "Unknown error")
            raise TypeOfErrorToRaise(
                {"error": True, "errMsg": responseJson.get("message", None)})

        return {"json": responseJson,"txRef": txRef} 

        
    def _handleInitiateResponse(self, response, txRef=None, request=None):
        """ This handles transaction charge responses """

        # Perform preliminary checks to validate the response
        res = self._preliminaryResponseChecks(response, TransactionChargeError, txRef=txRef)
        responseJson = res["json"]

        # Check if statusCode is "90000" (indicating success)
        status_code = responseJson.get("statusCode", None)

        if status_code == "90000":
         # Return success response when statusCode is 90000
            return {
                "error": False,
                "status": responseJson.get("status", "No status provided"),  # Handle if status is missing
                "message": responseJson.get("message", "No message provided"),
                "txRef": txRef or responseJson["data"].get("transactionRef", "No transactionRef provided"),
                "authUrl": responseJson["data"].get("url", None)  # Return the URL for further action
            }

        else:
            # Handle failure case when statusCode is not 90000
            return {
                "error": True,
                "message": responseJson.get("message", "No message provided"),
                "statusCode": status_code
            }


    def _handleStimulateBankTransferResponse(self, response, request=None):
        """ This handles transaction simulate responses """

        # Perform preliminary checks to validate the response
        res = self._preliminaryResponseChecks(response, TransactionChargeError)
        responseJson = res["json"]

        print(f"Handle Stimulate Response : {responseJson}")
        # Check if statusCode is "90000" (indicating success)
        status_code = responseJson.get("statusCode", None)

        if status_code == "90000":
         # Return success response when statusCode is 90000
            return {
                "error": False,
                "orderId": responseJson['data'].get("orderId", "No status provided"),  # Handle if status is missing
                "message": responseJson.get("message", "No message provided"),
                "merchantRef": responseJson["data"].get("merchantRef", "No transactionRef provided"),
                "customerEmail": responseJson["data"].get("customerEmail", None),
                "transactionId": responseJson["data"].get("transactionId", None),
                "amount": responseJson["data"].get("amount", None),
                "description": responseJson["data"].get("description", None),
                "currency": responseJson["data"].get("currency", None),
                "merchantInfo": responseJson["data"].get("merchantInfo", None),
                "discountPercentage": responseJson["data"].get("discountPercentage", None),
                "callBackUrl": responseJson["data"].get("callBackUrl", None),
                "isRecurring": responseJson["data"].get("isRecurring", None),
                "frequency": responseJson["data"].get("frequency", None),
                "serviceFees": responseJson["data"].get("serviceFees", None),
                "isBankDiscountEnabled": responseJson["data"].get("isBankDiscountEnabled", None),
                "bankDiscountValue": responseJson["data"].get("bankDiscountValue", None),
                "vatFee": responseJson["data"].get("vatFee", None),
                "vatPercentage": responseJson["data"].get("vatPercentage", None),
                "transactionMode": responseJson["data"].get("transactionMode", None),
            }

        else:
            # Handle failure case when statusCode is not 90000
            return {
                "error": True,
                "message": responseJson.get("message", "No message provided"),
                "statusCode": status_code
            }
  

    # Confirm Response
    def _handleConfirmResponse(self, response, txRef, request=None):
        """ This handles all responses from the confirmation call.\n
             Parameters include:\n
            response (dict) -- This is the response Http object returned from the payment confirm call
         """
        
        # print(f"Data Response pass to handleVerifyRes: {response}, {txRef}")
        # Perform preliminary checks to validate the response
        res = self._preliminaryResponseChecks(response, TransactionChargeError, txRef=txRef)
        responseJson = res["json"]

        confirm_response = responseJson['data']
        # print(f"Verify Response JSON Data: {confirm_response}")
        if responseJson.get('statusCode') == "90000":
            # Transaction was successful
            confirm_response["error"] = False
            confirm_response["transactionComplete"] = True
        else:
            # Transaction failed or was incomplete
            confirm_response["error"] = True
            confirm_response["transactionComplete"] = False

        # Return the final confirmation response
        # print(f"Verify Response JSON Data Full: {confirm_response}")
        return confirm_response


    # Initiate function (hasFailed is a flag that indicates there is a timeout),
    def initiate(
            self,
            paymentDetails,
            requiredParameters,
            endpoint):
        """ This is the base initiate call. It is usually overridden by implementing classes.\n
             Parameters include:\n
            paymentDetails (dict) -- These are the parameters passed to the function for processing\n
            requiredParameters (list) -- These are the parameters required for the specific call\n
        """
        # Checking for required components
        try:
            checkIfParametersAreComplete(requiredParameters, paymentDetails)
            print(f"Required parameters are present: {paymentDetails}")
        except BaseException:
            raise

        # Performing shallow copy of payment details to prevent tampering with original payment details
        paymentDetails = copy.copy(paymentDetails)

        # Request headers
        headers = {
            'Authorization': self._getLiveKey(),
            'content-type': 'application/json',
        }

        response = requests.post(
            endpoint, headers=headers, data=json.dumps(paymentDetails))

        # Log if the response is ok
        if response.ok:
            responseTime = response.elapsed.total_seconds()
            logging.info(f"Response OK: {responseTime}s")
        else:
            responseTime = response.elapsed.total_seconds()
            logging.error(f"Response Failed: {response.status_code}, Time: {responseTime}s")

        return self._handleInitiateResponse(
                response, paymentDetails)

    def simulatetransfer(
            self,
            paymentDetails,
            requiredParameters,
            endpoint):
        """ This is the base initiation call. It is usually overridden by implementing classes.\n
             Parameters include:\n
            paymentDetails (dict) -- These are the parameters passed to the function for processing\n
            requiredParameters (list) -- These are the parameters required for the specific call\n
        """
        # Checking for required components
        try:
            checkIfParametersAreComplete(requiredParameters, paymentDetails)
            print(f"Required parameters are present: {paymentDetails}")
        except BaseException:
            raise

        # Performing shallow copy of payment details to prevent tampering with original payment details
        paymentDetails = copy.copy(paymentDetails)

        # Request headers
        headers = {
            'Authorization': self._getLiveKey(),
            'Mode': str(19289182),
            'content-type': 'application/json',
        }

        response = requests.post(
            endpoint, headers=headers, data=json.dumps(paymentDetails))

        # print(f"Stimulate Transfer API Response: {response.status_code}")
        # print(f"Stimulate Transfer Response Body: {response.text}")
            
        if response.ok:
            responseTime = response.elapsed.total_seconds()
            logging.info(f"Response OK: {responseTime}s")
        else:
            responseTime = response.elapsed.total_seconds()
            logging.error(f"Response Failed: {response.status_code}, Time: {responseTime}s")

        return self._handleStimulateBankTransferResponse(
                response, paymentDetails)


    def confirmpayment(self, txRef, endpoint):
        """
            This is used to check the status of a transaction.
        Parameters:
            txRef (string): The transaction reference that was passed to the payment call. 
            If you didn't define a reference, you can access the auto-generated
            endpoint (string): The API endpoint to confirm the payment.
        """

    # Debug: Log the endpoint being used
        # print(f"Payment Endpoint Check: {endpoint}")
    
    # Prepare request headers
        headers = {
                'Authorization': self._getLiveKey(), 
                'content-type': 'application/json',
        }
        
    # Prepare the request payload containing the transaction reference
        payload = {
            "transactionRef": txRef  # Pass the transaction reference in the correct format
        }
    
        try:
            response = requests.post(endpoint, headers=headers, data=json.dumps(payload)) # Serialize the payload to JSON
        # Handle the confirmation response
            if response.ok:
                # If successful, handle the response
                return self._handleConfirmResponse(response, txRef)
            else:
            # If the response fails, log the error
                print(f"Error during confirmation: {response.status_code} - {response.text}")
                return None  # Or raise an exception based on your error handling needs

        except requests.exceptions.RequestException as e:
            # Handle any exceptions that occur during the request
            print(f"Request failed: {e}")
            return None

   