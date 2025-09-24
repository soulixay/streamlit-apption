import streamlit as st
# import streamlit_authenticator as stauth
import time
import requests
import json
from datetime import datetime
import xml.etree.ElementTree as ET
import xmltodict
import pandas as pd



current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
Date_Log = datetime.now().strftime('%Y%m%d')

### Target Endpoint for CBS
web_service_ar_url = 'http://172.28.236.57:8080/services/ArServices'
web_service_bc_url = 'http://172.28.236.57:8080/services/BcServices'
web_service_bb_url = 'http://172.28.236.57:8080/services/BbServices'

headers = {'Content-Type': 'text/plain; charset=utf-8'}


################ My function ################
 
def unbar(msisdn, resultstatus):
    # Define the URL of the API
    url = "http://172.28.16.121:3001/UpdateStatusEnable"

    if resultstatus is None:
        return "Invalid status code provided"

    body = {
        "username": msisdn,
        "status": resultstatus
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        # Send the POST request
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()  # Raise exception for HTTP errors

        # Inspect and return the server's response
        print("Server response status code:", response.status_code)
        print("Raw response text:", response.text)

        # Parse JSON response (if applicable)
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except requests.exceptions.RequestException as req_err:
        return f"Request error occurred: {req_err}"
    except ValueError as parse_err:
        # Handle JSON parsing error
        return f"JSON parse error: {parse_err}"
     
     
def ChangeSubStatusCBS(N_Status, N_msisdn, N_opty):
    # Define the SOAP endpoint URL
    url = "http://172.28.236.57:8080/services/BcServices"
    

    # Generate a unique message sequence
    message_seq = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    Code_=""
    resultstatus=""
    # Define the SOAP request XML
    soap_request = f'''
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                      xmlns:bcs="http://www.huawei.com/bme/cbsinterface/bcservices"
                      xmlns:cbs="http://www.huawei.com/bme/cbsinterface/cbscommon"
                      xmlns:bcc="http://www.huawei.com/bme/cbsinterface/bccommon">
       <soapenv:Header/>
       <soapenv:Body>
          <bcs:ChangeSubStatusRequestMsg>
             <RequestHeader>
                <cbs:Version>1</cbs:Version>
                <cbs:BusinessCode>CRM_BARRING_REQUEST</cbs:BusinessCode>
                <cbs:MessageSeq>CHANG_SUB_STS{message_seq}</cbs:MessageSeq>
                <cbs:AccessSecurity>
                   <cbs:LoginSystemCode>APICBS</cbs:LoginSystemCode>
                   <cbs:Password>i85pm92PnsK9VpnFxzPiJYcvE10me2xPuHIycCRbxWbHrEFcT9OECUMF9nni0sGb</cbs:Password>
                </cbs:AccessSecurity>
                <cbs:AdditionalProperty>
                   <cbs:Code>SHOP_CODE</cbs:Code>
                   <cbs:Value>BILLING</cbs:Value>
                </cbs:AdditionalProperty>
                <cbs:AdditionalProperty>
                   <cbs:Code>STAFF_CODE</cbs:Code>
                   <cbs:Value>BILLING</cbs:Value>
                </cbs:AdditionalProperty>
             </RequestHeader>
             <ChangeSubStatusRequest>
                <bcs:SubAccessCode>
                   <bcc:PrimaryIdentity>{N_msisdn}</bcc:PrimaryIdentity>
                </bcs:SubAccessCode>
                <bcs:OpType>{N_opty}</bcs:OpType>
                <bcs:NewStatus>{N_Status}</bcs:NewStatus>
                <bcs:AdditionalProperty>
                   <bcc:Code>USER_NAME</bcc:Code>
                   <bcc:Value>BILLING</bcc:Value>
                </bcs:AdditionalProperty>
                <bcs:AdditionalProperty>
                   <bcc:Code>SHOP_CODE</bcc:Code>
                   <bcc:Value>BILLING</bcc:Value>
                </bcs:AdditionalProperty>
                <bcs:AdditionalProperty>
                   <bcc:Code>REASON_ID</bcc:Code>
                   <bcc:Value>UNBARRING</bcc:Value>
                </bcs:AdditionalProperty>
             </ChangeSubStatusRequest>
          </bcs:ChangeSubStatusRequestMsg>
       </soapenv:Body>
    </soapenv:Envelope>
    '''

    # Define the headers
    headers = {
    'Content-Type': 'application/json; charset=utf-8'
    }

    # Send the POST request
    response = requests.post(url, headers=headers, data=soap_request)
    
   #  print(response)
    
    if "fh" in N_msisdn:
       if N_Status =="2":
          resultstatus = True
       elif N_Status =="3":
          resultstatus = False
       elif N_Status =="4":
          resultstatus = False
       unbar(N_msisdn,resultstatus)
      #  print("page:3 fh",N_msisdn,resultstatus)
    elif "tp" in N_msisdn:
       if N_Status =="2":
          resultstatus = True
       elif N_Status =="3":
          resultstatus = False
       elif N_Status =="4":
          resultstatus = False
       unbar(N_msisdn,resultstatus) 
      #  print("processing  'signeone' tp")
    elif "wt" in N_msisdn:
       if N_Status =="2":
          resultstatus = True
       elif N_Status =="3":
          resultstatus = False
       elif N_Status =="4":
          resultstatus = False
       unbar(N_msisdn,resultstatus)
      #  print("processing 'signeone' wt")
    elif "fr" in N_msisdn:
       if N_Status =="2":
          resultstatus = True
       elif N_Status =="3":
          resultstatus = False
       elif N_Status =="4":
          resultstatus = False
       unbar(N_msisdn,resultstatus)  
      #  print("processing 'signeone' fr")
    elif "fg" in N_msisdn:
       if N_Status =="2":
          resultstatus = True
       elif N_Status =="3":
          resultstatus = False
       elif N_Status =="4":
          resultstatus = False
       unbar(N_msisdn,resultstatus)
      #  print("processing 'signeone' fg")
    elif "fwtc" in N_msisdn:
       if N_Status =="2":
          resultstatus = True
       elif N_Status =="3":
          resultstatus = False
       elif N_Status =="4":
          resultstatus = False
       unbar(N_msisdn,resultstatus)
      #  print("processing 'signeone' fwtc")
    else:
         print("isdn is GSM, please select isdn again.")
   
    # Check the response
    if response.status_code == 200:
        return True, "Change subscription status successfully processed."
        
    else:
         return False, f"Error: {response.status_code}. {response.text}"

     
     

 
 
 ################ End Function ################

def app():
    st.write("""
        <h5 class="paragraph">Change Status CBS & Singeone</h5>
    """, unsafe_allow_html=True)
    
    code_=""
    optype_=""
    
    # Input for MSISDN (Phone Number)
    msisdn = st.text_input("Enter MSISDN (Phone Number):", placeholder="Please input your phone number")
    
    # Dropdown menu for additional options
    operation = st.selectbox(
        "Select Operation:",
        ["Please Select","Unbar","Barring 1 way", "Barring 2 way"]
    )

    if st.button("Submit"):
        if msisdn and operation != "Please Select":
            st.write(f"Searching for MSISDN: {msisdn} with operation: {operation}")
        elif not msisdn:
            st.warning("Please enter a valid MSISDN.")
        elif operation == "Please Select":
            st.warning("Please select an operation.")
        if operation =="Unbar":
           code_="2"
           optype_="40"
           success, message = ChangeSubStatusCBS(code_,msisdn,optype_)
           
           if success:
               st.success(message)
           else:
               st.error(message)
        elif operation=="Barring 1 way":
            code_="3"
            optype_="11"
            success, message = ChangeSubStatusCBS(code_,msisdn,optype_)
            if success:
                st.success(message)
            else:
                st.error(message)
        elif operation=="Barring 2 way":
            code_="4"
            optype_="12"
            success, message = ChangeSubStatusCBS(code_,msisdn,optype_)
            if success:
                st.success(message)
            else:
                st.error(message)
        else:
           code_="None"
           print("Invalid operation")
           
        
           
           
           
# Run the app
if __name__ == "__main__":
    app()
        