import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime
import xml.etree.ElementTree as ET
import xmltodict



### Target Endpoint for CBS
web_service_ar_url = 'http://172.28.236.57:8080/services/ArServices'
web_service_bc_url = 'http://172.28.236.57:8080/services/BcServices'
web_service_bb_url = 'http://172.28.236.57:8080/services/BbServices'

time_save=datetime.now().strftime('%Y%m%d%H%M%S')




# print(time_save)

headers = {'Content-Type': 'text/plain; charset=utf-8'}

def savedel_log(response_data, log_file=f"D:/BssWork/Python/streamlit/streamlit_demo/LOG_RESULT/LOG_DELETE{time_save}.txt"):
    with open(log_file, "a") as f:
        f.write(json.dumps(response_data) + "\n")


def saveadd_log(response_data, log_file=f"D:/BssWork/Python/streamlit/streamlit_demo/LOG_RESULT/LOG_ADD{time_save}.txt"):
    with open(log_file, "a") as f:
        f.write(json.dumps(response_data) + "\n")

def send_to_api(data, api_url):
   #  response = requests.post(api_url, json=data)
    response=requests.request("POST", api_url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed with status code {response.status_code}", "details": response.text}


def add():
    st.title("Add Suboffering")
    st.write("Function for adding ChangeSuboffering data")
    process_add()

def delete():
    st.title("Delete Suboffering")
    st.write("Function for deleting ChangeSuboffering data")
    process_del()

def process_add():
    # api_url = st.text_input("Enter API URL", "http://example.com/api")

   # Add date range pickers
    start_date = st.date_input("Select Start Date", datetime.today().date())
    end_date = st.date_input("Select End Date", datetime.today().date())

    if start_date > end_date:
        st.error("⚠️ Start date cannot be after end date!")
        return

    # Convert dates to string format for processing
    start_date_str = start_date.strftime("%Y%m%d%H%M%S")
    end_date_str = end_date.strftime("%Y%m%d%H%M%S")
    
   

    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("### Data loaded:", df.head(5000))
        
        if st.button("Send Data to API"):
            results = []
            for index, row in df.iterrows():
               #  data = row.to_dict()
                
                offer_id=row["offer_id"]
                msisdn=row["msisdn"]                
                
                time_=datetime.now().strftime('%Y%m%d%H%M%S')
                expirtime_="20370101000000"
                
                Date_Log = datetime.now().strftime('%Y%m%d%H%M%S')
                transaction = f"""CRM_CHANGEPACKAGE_CBS_POSTPAID_{Date_Log}"""
                dataxml=f'''
<soapenv:Envelope xmlns:soapenv=""http://schemas.xmlsoap.org/soap/envelope/"" xmlns:bcs=""http://www.huawei.com/bme/cbsinterface/bcservices"" xmlns:cbs=""http://www.huawei.com/bme/cbsinterface/cbscommon"" xmlns:bcc=""http://www.huawei.com/bme/cbsinterface/bccommon"">
   <soapenv:Header/>
   <soapenv:Body>
      <bcs:ChangeSubOfferingRequestMsg>
         <RequestHeader>
            <cbs:Version>1</cbs:Version>
            <cbs:BusinessCode>ADDSF</cbs:BusinessCode>
            <cbs:MessageSeq>{transaction}</cbs:MessageSeq>
            <cbs:AccessSecurity>
               <cbs:LoginSystemCode>APICBS</cbs:LoginSystemCode>
               <cbs:Password>i85pm92PnsK9VpnFxzPiJYcvE10me2xPuHIycCRbxWbHrEFcT9OECUMF9nni0sGb</cbs:Password>
            </cbs:AccessSecurity>
            <cbs:AccessMode>3</cbs:AccessMode>
            <cbs:AdditionalProperty>
               <cbs:Code>SHOP_CODE</cbs:Code>
               <cbs:Value>BILLING</cbs:Value>
            </cbs:AdditionalProperty>
            <cbs:AdditionalProperty>
               <cbs:Code>STAFF_CODE</cbs:Code>
               <cbs:Value>BILLING</cbs:Value>
            </cbs:AdditionalProperty>
         </RequestHeader>
         <ChangeSubOfferingRequest>
            <bcs:SubAccessCode>
               <bcc:PrimaryIdentity>{msisdn}</bcc:PrimaryIdentity>
            </bcs:SubAccessCode>
            <bcs:SupplementaryOffering>
               <bcs:AddOffering>
                  <bcc:OfferingKey>
                     <bcc:OfferingCode>{offer_id}</bcc:OfferingCode>
                  </bcc:OfferingKey>
                  <bcc:BundledFlag>S</bcc:BundledFlag>
                  <bcc:OfferingClass>I</bcc:OfferingClass>
                  <bcc:Status>2</bcc:Status>
                  <bcs:EffectiveTime>
                     <bcc:Mode>S</bcc:Mode>
                     <bcc:Time>{start_date_str}</bcc:Time>
                  </bcs:EffectiveTime>
                  <bcs:ExpirationTime>{end_date_str}</bcs:ExpirationTime>
               </bcs:AddOffering>
            </bcs:SupplementaryOffering>
         </ChangeSubOfferingRequest>
      </bcs:ChangeSubOfferingRequestMsg>
   </soapenv:Body>
</soapenv:Envelope>
                '''

               #  response = send_to_api(dataxml, web_service_bc_url)
               #  results.append(response)
               #  saveadd_log(response)
                
               #  respData_act = results.content.decode('utf-8')
               #  new_resp_act = str(respData_act[38:])  
               #  soap_response = ET.fromstring(new_resp_act)
               #  ResultCode_element = soap_response.find('.//{http://www.huawei.com/bme/cbsinterface/cbscommon}ResultCode')
               #  ResultCode = ResultCode_element.text if ResultCode_element is not None else None
               #  ResultDesc_element = soap_response.find('.//{http://www.huawei.com/bme/cbsinterface/cbscommon}ResultDesc')
               #  ResultDesc = ResultDesc_element.text if ResultDesc_element is not None else None
               #  log_entry = f"{msisdn}|{offer_id}|{ResultCode}|{ResultDesc}|{Date_Log}|\n"
               #  with open(f"LOG_ADD{Date_Log}.txt", "a") as file:
               #     file.write(log_entry)
               #     print(f"{log_entry}")
               
               
                response=requests.request("POST", web_service_bc_url, headers=headers, data=dataxml)
                respData_cdp = response.content.decode('utf-8')
                new_resp_cdp = str(respData_cdp[38:])
               
               
                soap_response = ET.fromstring(new_resp_cdp)
                ResultCode_element = soap_response.find('.//{http://www.huawei.com/bme/cbsinterface/cbscommon}ResultCode')
                ResultCode = ResultCode_element.text if ResultCode_element is not None else None
                ResultDesc_element = soap_response.find('.//{http://www.huawei.com/bme/cbsinterface/cbscommon}ResultDesc')
                ResultDesc = ResultDesc_element.text if ResultDesc_element is not None else None
                
               #  results.append(soap_response)
                   # Write processed data to the output file
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
                log_entry = f"{msisdn}|{ResultCode}|{ResultDesc}|{timestamp}|\n"
                
                with open("LOG_ADD_PK.txt", "a") as file:
                   file.write(log_entry)
                print(f"{log_entry}")
               
               
                
            
            st.write("### API Responses:")
            st.json(results)
            st.success("Process completed. Log saved.")


def process_del():
    # api_url = st.text_input("Enter API URL", "http://example.com/api")


   # Add date range pickers
    start_date = st.date_input("Effect Time:", datetime.today().date())
   #  end_date = st.date_input("Select End Date", datetime.today().date())

    if start_date =="":
        st.error("⚠️ Start date cannot be after end date!")
        return

    # Convert dates to string format for processing
    start_date_str = start_date.strftime("%Y%m%d%H%M%S")
   #  end_date_str = end_date.strftime("%Y%m%d%H%M%S")
    
 
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("### Data loaded:", df.head(5000))
        
        if st.button("Send Data to API"):
            results = []
            for index, row in df.iterrows():
               #  data = row.to_dict()
               #  data = {"offer_id": row["offer_id"], "msisdn": row["msisdn"]}
                offer_id=row["offer_id"]
                msisdn=row["msisdn"]
                
                
                
                create_date = datetime.now().strftime('%Y%m%d%H%M%S')
                Date_Log = datetime.now().strftime('%Y%m%d%H%M%S')
                transaction = f"""CRM_CHANGEPACKAGE_CBS_POSTPAID_{Date_Log}"""
                
                dataxml=f'''
   <soapenv:Envelope xmlns:soapenv=""http://schemas.xmlsoap.org/soap/envelope/"" xmlns:bcs=""http://www.huawei.com/bme/cbsinterface/bcservices"" xmlns:cbs=""http://www.huawei.com/bme/cbsinterface/cbscommon"" xmlns:bcc=""http://www.huawei.com/bme/cbsinterface/bccommon"">
   <soapenv:Header/>
   <soapenv:Body>
      <bcs:ChangeSubOfferingRequestMsg>
         <RequestHeader>
            <cbs:Version>1</cbs:Version>
            <cbs:BusinessCode>CRM_Migration</cbs:BusinessCode>
            <cbs:MessageSeq>{transaction}</cbs:MessageSeq>
            <cbs:AccessSecurity>
               <cbs:LoginSystemCode>APICBS</cbs:LoginSystemCode>
               <cbs:Password>i85pm92PnsK9VpnFxzPiJYcvE10me2xPuHIycCRbxWbHrEFcT9OECUMF9nni0sGb</cbs:Password>
               <cbs:RemoteIP>10.30.5.26</cbs:RemoteIP>
            </cbs:AccessSecurity>
            <cbs:AccessMode>3</cbs:AccessMode>
            <cbs:AdditionalProperty>
               <cbs:Code>SHOP_CODE</cbs:Code>
               <cbs:Value>BILLING</cbs:Value>
            </cbs:AdditionalProperty>
            <cbs:AdditionalProperty>
                <cbs:Code>STAFF_CODE</cbs:Code>
                <cbs:Value>BILLING</cbs:Value>
             </cbs:AdditionalProperty>
         </RequestHeader>
         <ChangeSubOfferingRequest>
            <bcs:SubAccessCode>
               <bcc:PrimaryIdentity>{msisdn}</bcc:PrimaryIdentity>
            </bcs:SubAccessCode>
            <bcs:SupplementaryOffering>
               <bcs:ModifyOffering>
                  <bcs:OfferingKey>
                     <bcc:OfferingCode>{offer_id}</bcc:OfferingCode>
                  </bcs:OfferingKey>
                  <bcs:NewExpirationTime>
                     <bcc:Mode>S</bcc:Mode>
                     <bcc:Time>{start_date_str}</bcc:Time>
                  </bcs:NewExpirationTime>
               </bcs:ModifyOffering>
            </bcs:SupplementaryOffering>
         </ChangeSubOfferingRequest>
      </bcs:ChangeSubOfferingRequestMsg>
   </soapenv:Body>
</soapenv:Envelope>
                '''
                
               #  response = send_to_api(dataxml, web_service_bc_url)
               #  results.append(response)
                response=requests.request("POST", web_service_bc_url, headers=headers, data=dataxml)
                respData_cdp = response.content.decode('utf-8')
                new_resp_cdp = str(respData_cdp[38:])
               
               
                soap_response = ET.fromstring(new_resp_cdp)
                ResultCode_element = soap_response.find('.//{http://www.huawei.com/bme/cbsinterface/cbscommon}ResultCode')
                ResultCode = ResultCode_element.text if ResultCode_element is not None else None
                ResultDesc_element = soap_response.find('.//{http://www.huawei.com/bme/cbsinterface/cbscommon}ResultDesc')
                ResultDesc = ResultDesc_element.text if ResultDesc_element is not None else None
                
                
               #  results.append(soap_response)
                   # Write processed data to the output file
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
                log_entry = f"{msisdn}|{ResultCode}|{ResultDesc}|{timestamp}|\n"
                
                with open("LOG_CANCEL_PK.txt", "a") as file:
                   file.write(log_entry)
                print(f"{log_entry}")
                
            # savedel_log(response)
            
            st.write("### API Responses:")
            st.json(results)
            st.success("Process completed.")

