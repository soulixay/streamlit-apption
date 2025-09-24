import streamlit as st
# import streamlit_authenticator as stauth
import time
import requests
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


################ QueryInnfo ################
def QueryCustomerInfo(msisdn):
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

    # soap_response = ET.fromstring(new_resp)

    # result_code_elem = soap_response.find('.//{http://www.huawei.com/bme/cbsinterface/cbscommon}ResultCode')
    # result_code = result_code_elem.text if result_code_elem is not None else '999999'

    # result_desc_elem = soap_response.find('.//{http://www.huawei.com/bme/cbsinterface/cbscommon}ResultDesc')
    # result_desc = result_desc_elem.text if result_desc_elem is not None else 'Unknow Error'

    xml2dict_data = xmltodict.parse(new_resp, encoding='utf-8')
   #  json_data = json.dumps(xml2dict_data, ensure_ascii=False)

    # print(json_data)
    return xml2dict_data
 
 
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
 
 
 ################ End Function ################

def app():
   #  st.title("Query Customer Info")
    st.write(f"""
            <h5 class="paragraph">Query Customer Info</h5>
            """, unsafe_allow_html=True)
    msisdn = st.text_input("Enter MSISDN (Phone Number):", placeholder="please input your phone number")
    
    if st.button("Search"):
        if msisdn:
            st.write(f"Searching for MSISDN: {msisdn}")
            result = QueryCustomerInfo(msisdn)
            
            # Check if the result has the "ResultCode" key
            if result:
                
                    
                # Flatten the result dictionary to display in a table
                flattened_data = flatten_dict(result)

                # Convert the flattened data to a Pandas DataFrame for table display
                flattened_df = pd.DataFrame(list(flattened_data.items()), columns=["Field", "Value"])

                # Display the result in a table
                st.dataframe(flattened_df)
            else:
                st.error("Failed to retrieve or parse the result.")
            st.write(result)
        else:
            st.warning("Please enter a valid MSISDN.")