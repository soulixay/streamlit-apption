import streamlit as st
import time
import requests
from datetime import datetime
import xml.etree.ElementTree as ET
import xmltodict
import pandas as pd
import json
import os




# current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# Date_Log = datetime.now().strftime('%Y%m%d')

### Target Endpoint for CBS
web_service_ar_url = 'http://172.28.236.57:8080/services/ArServices'
web_service_bc_url = 'http://172.28.236.57:8080/services/BcServices'
web_service_bb_url = 'http://172.28.236.57:8080/services/BbServices'

# headers = {'Content-Type': 'text/plain; charset=utf-8'}
headers = {
    'Content-Type': 'application/json; charset=utf-8'
}

# ================== Function for Writing Logs ==================
def write_log(action, msisdn, response_text):
    """Write log to a .txt file with timestamp"""
    log_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_date = datetime.now().strftime('%Y%m%d')
    log_filename = f"logs_{log_date}.txt"

    log_entry = f"[{log_time}] ACTION: {action} | MSISDN: {msisdn} | RESPONSE: {response_text}\n"

    # Ensure log directory exists
    os.makedirs("logs", exist_ok=True)
    filepath = os.path.join("logs", log_filename)

    with open(filepath, "a", encoding="utf-8") as f:
        f.write(log_entry)

def QueryCustomerInfo(msisdn):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   #  Date_Log = datetime.now().strftime('%Y%m%d')

    Date_Log = datetime.now().strftime('%Y%m%d%H%M%S')
   #  print(Date_Log)
    payload = f'''
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:bcs="http://www.huawei.com/bme/cbsinterface/bcservices" xmlns:cbs="http://www.huawei.com/bme/cbsinterface/cbscommon" xmlns:bcc="http://www.huawei.com/bme/cbsinterface/bccommon">
       <soapenv:Header/>
       <soapenv:Body>
          <bcs:QueryCustomerInfoRequestMsg>
             <RequestHeader>
                <cbs:Version>1</cbs:Version>
                <cbs:BusinessCode>MCAre</cbs:BusinessCode>
                <cbs:MessageSeq>GetCustomerInformation</cbs:MessageSeq>
                <cbs:AccessSecurity>
                   <cbs:LoginSystemCode>APICBS</cbs:LoginSystemCode>
                   <cbs:Password>i85pm92PnsK9VpnFxzPiJYcvE10me2xPuHIycCRbxWbHrEFcT9OECUMF9nni0sGb</cbs:Password>
                </cbs:AccessSecurity>
             </RequestHeader>
             <QueryCustomerInfoRequest>
                <bcs:QueryObj>
                   <bcs:SubAccessCode>
                      <bcc:PrimaryIdentity>{msisdn}</bcc:PrimaryIdentity>
                   </bcs:SubAccessCode>
                </bcs:QueryObj>
                <bcs:QueryMode>0</bcs:QueryMode>
                <bcs:CustomerMask>1111</bcs:CustomerMask>
                <bcs:AccountMask>11</bcs:AccountMask>
                <bcs:SubscriberMask>111111111111</bcs:SubscriberMask>
             </QueryCustomerInfoRequest>
          </bcs:QueryCustomerInfoRequestMsg>
       </soapenv:Body>
    </soapenv:Envelope>
    '''
    response = requests.request("POST", web_service_bc_url, headers=headers, data=payload)
    respData = response.content.decode('utf-8')
    new_resp = str(respData[38:])

    xml2dict_data = xmltodict.parse(new_resp, encoding='utf-8')
    
    
    # Navigate to the relevant part of the JSON structure
    account_info = xml2dict_data['soapenv:Envelope']['soapenv:Body']['bcs:QueryCustomerInfoResultMsg']['QueryCustomerInfoResult']['bcs:Account']['bcs:AcctInfo']['bcs:AcctBasicInfo']
    
    # Extracting the target value
    target_value = None
    for acct_property in account_info['bcc:AcctProperty']:
        code = acct_property['bcc:Code']
        if code == "CN_ACCT_GROUP_TYPE":
            target_value = acct_property['bcc:Value']
            break
    
    # Prepare the final JSON output
    result_json = {
        "CN_ACCT_GROUP_TYPE": target_value
    }
    
    # Convert to JSON string
    json_output = json.dumps(result_json, indent=4, ensure_ascii=False)
    
   # ✅ Write log
    write_log("QueryCustomerInfo", msisdn, json_output)
   #  print(json_output)
    return json_output


################# Change Account Innfo ################
def change_account_info(msisdn,deb_profile):
   current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   Date_Log = datetime.now().strftime('%Y%m%d%H%M%S')
   if deb_profile == 'individual':
      acct_group_type = '2'
      acct_flag = '0'
      credit_limit = '2000000'
   elif deb_profile == 'inhouse':
      acct_group_type = '1'
      acct_flag = '0'
      credit_limit = '1000000000'
   elif deb_profile == 'vip':
      acct_group_type = '5'
      acct_flag = '0'
      credit_limit = '1000000000'
   elif deb_profile == 'individual_prepaid':
      acct_group_type = '3'
      acct_flag = '1'
      credit_limit = '0'
   elif deb_profile == 'corporate':
      acct_group_type = '4'
      acct_flag = '0'
      credit_limit = '1000000000'

   ### Change Debt Profile
   payload_cdp = f'''
   <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:bcs="http://www.huawei.com/bme/cbsinterface/bcservices" xmlns:cbs="http://www.huawei.com/bme/cbsinterface/cbscommon" xmlns:bcc="http://www.huawei.com/bme/cbsinterface/bccommon">
      <soapenv:Header/>
      <soapenv:Body>
         <bcs:ChangeAcctInfoRequestMsg>
            <RequestHeader>
               <cbs:Version>1</cbs:Version>
               <cbs:BusinessCode>CHANGEDEBTPROFILE</cbs:BusinessCode>
               <cbs:MessageSeq>CDP_{deb_profile}_{Date_Log}</cbs:MessageSeq>
               <cbs:AccessSecurity>
                  <cbs:LoginSystemCode>APICBS</cbs:LoginSystemCode>
                  <cbs:Password>i85pm92PnsK9VpnFxzPiJYcvE10me2xPuHIycCRbxWbHrEFcT9OECUMF9nni0sGb</cbs:Password>
               </cbs:AccessSecurity>
            </RequestHeader>
            <ChangeAcctInfoRequest>
               <bcs:AcctAccessCode>
                  <bcc:PrimaryIdentity>{msisdn}</bcc:PrimaryIdentity>
               </bcs:AcctAccessCode>
               <bcs:AcctBasicInfo>
                  <bcc:AcctProperty>
                     <bcc:Code>CN_ACCT_CC_FLAG</bcc:Code>
                     <bcc:Value>{acct_flag}</bcc:Value>
                  </bcc:AcctProperty>
                  <bcc:AcctProperty>
                     <bcc:Code>CN_ACCT_GROUP_TYPE</bcc:Code>
                     <bcc:Value>{acct_group_type}</bcc:Value>
                  </bcc:AcctProperty>
               </bcs:AcctBasicInfo>
            </ChangeAcctInfoRequest>
         </bcs:ChangeAcctInfoRequestMsg>
      </soapenv:Body>
   </soapenv:Envelope>
   '''
   response_cdp = requests.request("POST", web_service_bc_url, headers=headers, data=payload_cdp)
   respData_cdp = response_cdp.content.decode('utf-8')
   new_resp_cdp = str(respData_cdp[38:])

   xml2dict_data_cdp = xmltodict.parse(new_resp_cdp, encoding='utf-8')

   ### Change Account Credit Limit
   payload_cac = f'''
   <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:bcs="http://www.huawei.com/bme/cbsinterface/bcservices" xmlns:cbs="http://www.huawei.com/bme/cbsinterface/cbscommon" xmlns:bcc="http://www.huawei.com/bme/cbsinterface/bccommon">
      <soapenv:Header/>
      <soapenv:Body>
         <bcs:ChangeAcctCreditLimitRequestMsg>
            <RequestHeader>
               <cbs:Version>1</cbs:Version>
               <cbs:BusinessCode>CHANGEACCTKEY</cbs:BusinessCode>
               <cbs:MessageSeq>CAC_{deb_profile}_{Date_Log}</cbs:MessageSeq>
               <cbs:AccessSecurity>
                  <cbs:LoginSystemCode>APICBS</cbs:LoginSystemCode>
                  <cbs:Password>i85pm92PnsK9VpnFxzPiJYcvE10me2xPuHIycCRbxWbHrEFcT9OECUMF9nni0sGb</cbs:Password>
               </cbs:AccessSecurity>
            </RequestHeader>
            <ChangeAcctCreditLimitRequest>
               <bcs:AcctAccessCode>
                  <bcc:PrimaryIdentity>{msisdn}</bcc:PrimaryIdentity>
               </bcs:AcctAccessCode>
               <bcs:AccountCredit>
                  <bcs:CommonCreditLimit>
                     <bcs:NewLimitAmount>{credit_limit}</bcs:NewLimitAmount>
                     <bcs:EffectiveTime>
                        <bcc:Mode>I</bcc:Mode>
                     </bcs:EffectiveTime>
                  </bcs:CommonCreditLimit>
               </bcs:AccountCredit>
            </ChangeAcctCreditLimitRequest>
         </bcs:ChangeAcctCreditLimitRequestMsg>
      </soapenv:Body>
   </soapenv:Envelope>
   '''

   response_cac = requests.request("POST", web_service_bc_url, headers=headers, data=payload_cac)
   respData_cdp = response_cac.content.decode('utf-8')
   new_resp_cdp = str(respData_cdp[38:])

   xml2dict_data_cac = xmltodict.parse(new_resp_cdp, encoding='utf-8')
   ### acivate subscriber
   payload_act = f'''
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:bcs="http://www.huawei.com/bme/cbsinterface/bcservices" xmlns:cbs="http://www.huawei.com/bme/cbsinterface/cbscommon" xmlns:bcc="http://www.huawei.com/bme/cbsinterface/bccommon">
   <soapenv:Header/>
   <soapenv:Body>
      <bcs:ChangeSubStatusRequestMsg>
         <RequestHeader>
            <cbs:Version>1</cbs:Version>
            <!--Channel that request:-->
            <cbs:BusinessCode>CRM_BARRING_REQUEST</cbs:BusinessCode>
            <cbs:MessageSeq>UNBAR_{deb_profile}_{Date_Log}</cbs:MessageSeq>
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
               <bcc:PrimaryIdentity>{msisdn}</bcc:PrimaryIdentity>
            </bcs:SubAccessCode>
            <bcs:OpType>40</bcs:OpType>
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
   response_act = requests.request("POST", web_service_bc_url, headers=headers, data=payload_act)
   respData_act = response_act.content.decode('utf-8')
   new_resp_act = str(respData_act[38:])

   xml2dict_data_act = xmltodict.parse(new_resp_act, encoding='utf-8')
   # print([xml2dict_data_cdp,xml2dict_data_cac,xml2dict_data_act])
   result = [xml2dict_data_cdp, xml2dict_data_cac, xml2dict_data_act]

   # ✅ Write log
   write_log("ChangeAccountInfo", msisdn, json.dumps(result, ensure_ascii=False))
   return result


# Function to flatten the dictionary into a list of key-value pairs
def flatten_dict(data, parent_key='', sep='_'):
    items = []
    for k, v in data.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            for i, elem in enumerate(v):
                items.extend(flatten_dict(elem, f"{new_key}_{i}", sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

#########################################End Function #########################################

def app():
   #  st.write("ChangAccountInfo")
    st.write(f'<h3>query deb profile</h3>', unsafe_allow_html=True)
    msisdn = st.text_input("Enter MSISDN (Phone Number):", placeholder="please input your phone number")
    
    if st.button("search"):
                
           result = QueryCustomerInfo(msisdn)
           if result:
              data=json.loads(result)
              # Split the data into keys and values
            #   keys = list(data.keys())
            #   values = list(data.values())  
            #   st.write(values)
              code_="None"
              if data.get("CN_ACCT_GROUP_TYPE") == "1":
                 code_="inhouse"
              elif data.get("CN_ACCT_GROUP_TYPE") == "2":
                 code_="individual"
              elif data.get("CN_ACCT_GROUP_TYPE") == "3":
                 code_="individual_prepaid"
              elif data.get("CN_ACCT_GROUP_TYPE") == "4":
                 code_="corporate"
              elif data.get("CN_ACCT_GROUP_TYPE") == "5":
                 code_="vip"
               
              st.subheader("**AcctProperty:**")
              st.text_input(f"**CN_ACCT_GROUP_TYPE:**", value=data)
            #   st.text_input(f"**Value:**",value= code_)
              # Display a colored text input
              st.markdown(f"""
              <style>
              .input-color {{
                  background-color: #f0f8ff; /* Light blue background */
                  color: #000; /* Black text */
                  border: 1px solid #007bff; /* Blue border */
                  padding: 10px;
                  border-radius: 5px;
              }}
              </style>
              <div class="input-color">
                  <label for="value_input"><strong>Deb Profile:</strong></label>
                  <input type="text" id="value_input" value="{code_}" style="width: 100%; border: none; outline: none; background: transparent;" />
              </div>
              """, unsafe_allow_html=True)
              
              # Display the current account group 
              # Sample initial account group type
               
              
              
              
              
              
              
           else:
              st.error("Failed to retrieve or parse the result.")
         
    # Streamlit UI
    # Initialize session state for expander
    if 'expander_open' not in st.session_state:
       st.session_state.expander_open = False
    st.write(f'<h3>change deb profile</h3>', unsafe_allow_html=True)        
    # Expander for changing account group type
    with st.expander("Change Account Group Type", expanded=True):
        # Radio options for selecting account profile
        options = ["Choose a new account type","individual", "inhouse", "vip", "individual_prepaid", "corporate"]
        selected_option = st.selectbox("Choose a new account group type:", options)

        # Input fields in the expander
        new_msisdn = st.text_input("Enter new MSISDN:", value=msisdn)

        # Button to confirm the change
        if st.button("Confirm Change"):
            
            result = change_account_info(new_msisdn, selected_option)
            st.write(result)
            # Check if the result has the "ResultCode" key
            if result:  
               parsed=result[0]
               st.json(parsed)
               st.session_state.expander_open = False
            else:
               st.error("Failed to retrieve or parse the result.")
               
      #   st.session_state.expander_open = False
    
    # Optional: Display current account group type
   #  if 'current_group_type' in st.session_state:
   #      st.write(f"Current Account Group Type: {st.session_state.current_group_type}")
              

           
         
           
          

