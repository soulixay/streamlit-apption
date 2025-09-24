import streamlit as st
import time
import json
import time
import requests
from datetime import datetime
import xml.etree.ElementTree as ET
import xmltodict


current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
Date_Log = datetime.now().strftime('%Y%m%d')

### Target Endpoint for CBS
web_service_ar_url = 'http://172.28.236.57:8080/services/ArServices'
web_service_bc_url = 'http://172.28.236.57:8080/services/BcServices'
web_service_bb_url = 'http://172.28.236.57:8080/services/BbServices'

headers = {'Content-Type': 'text/plain; charset=utf-8'}

################ QueryBalance ################
def QueryBalance(msisdn):
    payload = f'''
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ars="http://www.huawei.com/bme/cbsinterface/arservices" xmlns:cbs="http://www.huawei.com/bme/cbsinterface/cbscommon" xmlns:arc="http://cbs.huawei.com/ar/wsservice/arcommon">
       <soapenv:Header/>
       <soapenv:Body>
          <ars:QueryBalanceRequestMsg>
             <RequestHeader>
                <cbs:Version>1</cbs:Version>
                <cbs:BusinessCode>MCARE</cbs:BusinessCode>
                <cbs:MessageSeq>MCARE</cbs:MessageSeq>
                <cbs:AccessSecurity>
                   <cbs:LoginSystemCode>APICBS</cbs:LoginSystemCode>
                   <cbs:Password>i85pm92PnsK9VpnFxzPiJYcvE10me2xPuHIycCRbxWbHrEFcT9OECUMF9nni0sGb</cbs:Password>
                </cbs:AccessSecurity>
             </RequestHeader>
             <QueryBalanceRequest>
                <ars:QueryObj>
                   <ars:SubAccessCode>
                      <arc:PrimaryIdentity>{msisdn}</arc:PrimaryIdentity>
                   </ars:SubAccessCode>
                </ars:QueryObj>
             </QueryBalanceRequest>
          </ars:QueryBalanceRequestMsg>
       </soapenv:Body>
    </soapenv:Envelope>
    '''
        # Call the web service
    response = requests.request("POST", web_service_ar_url, headers=headers, data=payload)
    respData = response.content.decode('utf-8')
    new_resp = str(respData[38:])

    soap_response = ET.fromstring(new_resp)

    result_code_elem = soap_response.find('.//{http://www.huawei.com/bme/cbsinterface/cbscommon}ResultCode')
    result_code = result_code_elem.text if result_code_elem is not None else '999999'

    result_desc_elem = soap_response.find('.//{http://www.huawei.com/bme/cbsinterface/cbscommon}ResultDesc')
    result_desc = result_desc_elem.text if result_desc_elem is not None else 'Unknow Error'

    acctkey_elem = soap_response.find('.//{http://www.huawei.com/bme/cbsinterface/arservices}AcctKey')
    acctkey = acctkey_elem.text if acctkey_elem is not None else 'Unknow Error'

    TotalAmount_elem = soap_response.find('.//{http://cbs.huawei.com/ar/wsservice/arcommon}TotalAmount')
    TotalAmount = TotalAmount_elem.text if TotalAmount_elem is not None else '0'

    TotalCreditAmount_elem = soap_response.find('.//{http://www.huawei.com/bme/cbsinterface/arservices}TotalAmount')
    TotalCreditAmount = TotalCreditAmount_elem.text if TotalCreditAmount_elem is not None else '0'

    TotalUsageAmount_elem = soap_response.find('.//{http://www.huawei.com/bme/cbsinterface/arservices}TotalAmount')
    TotalUsageAmount = TotalUsageAmount_elem.text if TotalUsageAmount_elem is not None else '0'

    TotalRemainAmount_elem = soap_response.find('.//{http://www.huawei.com/bme/cbsinterface/arservices}TotalAmount')
    TotalRemainAmount = TotalRemainAmount_elem.text if TotalRemainAmount_elem is not None else '0'

    # Initialize the total outstanding amount
    total_outstanding_amount = 0

    # List to store extracted details
    outstanding_details = []

    # Iterate through each OutStandingList
    for outstanding_list in soap_response.findall('.//{http://www.huawei.com/bme/cbsinterface/arservices}OutStandingList'):
        # Extract required fields
        bill_cycle_id = outstanding_list.find('.//{http://www.huawei.com/bme/cbsinterface/arservices}BillCycleID').text
        due_date = outstanding_list.find('.//{http://www.huawei.com/bme/cbsinterface/arservices}DueDate').text
        outstanding_amount = int(outstanding_list.find('.//{http://www.huawei.com/bme/cbsinterface/arservices}OutStandingAmount').text)

        # Add to the total outstanding amount
        total_outstanding_amount += outstanding_amount

        # Save the details
        outstanding_details.append({
            "BillCycleID": bill_cycle_id,
            "DueDate": due_date,
            "OutStandingAmount": outstanding_amount
        })
    
    response_data = {
        'ResultCode' : result_code,
        'ResultDesc' : result_desc,
        'AcctKey' : acctkey,
        'Msisdn' : msisdn,
        'TotalBalanceAmount' : TotalAmount,
        'TotalCreditAmount' : TotalCreditAmount,
        'TotalCreditUsageAmount' : TotalUsageAmount,
        'TotalCreditRemainAmount' : TotalRemainAmount,
        'TotalOustandingBalance' : total_outstanding_amount,
        'OustandingList' : outstanding_details
    }
    print(response_data)
    return response_data

################ End Function ################

def app():
    # st.title("QueryBalance")
    st.write(f"""
            <h5 class="paragraph">QueryBalance</h5>
            """, unsafe_allow_html=True)
    msisdn = st.text_input("Enter MSISDN (Phone Number):", placeholder="please input your phone number")
    if st.button("Search"):
        # print("Search button clicked!") 
        if msisdn:
            # Call the QueryBalance function
            result = QueryBalance(msisdn)
            # Display the results
            if result["ResultCode"] != "0":
                st.error(f"Error: {result['ResultDesc']}")
            else:
                st.success(f"Result: {result['ResultDesc']}")
                
                # Display detailed balance information
                st.subheader("**Account Details:**")
                st.text_input(f"**Account Key:**", value=result['AcctKey'])
                st.text_input(f"**MSISDN:**",value= result['Msisdn'])
                st.text_input(f"**Total Balance Amount:**", value=result['TotalBalanceAmount'])
                st.text_input(f"**Total Credit Amount:**", value=result['TotalCreditAmount'])
                st.text_input(f"**Total Credit Usage Amount:**", value=result['TotalCreditUsageAmount'])
                st.text_input(f"**Total Credit Remain Amount:**", value=result['TotalCreditRemainAmount'])
                if 'TotalOustandingBalance' in result:
                    st.text_input(f"**Total Outstanding Balance:**", value=result['TotalOustandingBalance'])
                else:
                    st.text_input("**Total Outstanding Balance:**", value="Data not available")
                
                
                outstanding_list = result.get("OustandingList", [])
                if outstanding_list:
                    st.write("**Outstanding Details:**")
                    for idx, item in enumerate(outstanding_list, start=1):
                        st.write(f"{idx}. {item}")
                else:
                    st.write("No outstanding details available.")
                
        else:
              st.warning("Please enter a valid MSISDN.")
