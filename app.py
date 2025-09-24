import streamlit as st
from pages import changea_ccount, home, query_balance, query_info, about, unbar, change_suboffering
from login import Login
# Load and apply custom CSS
def load_custom_css():
    css = f"""
    <style>
    @font-face {{
        font-family: 'Phetsarath OT';
        src: url('PhetsarathOT.ttf') format('truetype');
    }}
    html, 
    body
    h1, 
    h2, 
    h3, 
    h4, 
    h5, 
    h6 {{
        font-family: 'Phetsarath OT', sans-serif;
    }}
    
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Apply the CSS
load_custom_css()

# Initialize Login
login = Login(timeout=3600) 

# Authentication
if not login.is_authenticated():
    login.login()
else:
    login.check_timeout()
    role = login.get_user_role()

    # Sidebar for navigation
    st.sidebar.title("Menu Function")
    page = st.sidebar.radio("Go to", ["Home", "QueryBalance","QueryCustomerInfo","ChangeAccounttInfo","ChangeSuboffering","Unbar", "About","Logout"])

    st.write(f"""
             <h2>Profile Name: 
             {st.session_state['logged_in']['username']} !
             </h2>
             """, unsafe_allow_html=True)
    
    # Render pages based on selection
    if page == "Home":
        home.app()
    elif page == "QueryBalance":
        query_balance.app()
    elif page == "QueryCustomerInfo":
        if role == "admin":
            # st.write("You have admin access.")
            query_info.app()
        else:
            st.write(f"""
                    <h5 class="paragraph">username not have access, please contact administrator</h5>
                    """, unsafe_allow_html=True)
    elif page == "ChangeAccounttInfo":
        changea_ccount.app()

    elif page == "ChangeSuboffering":
        suboffering_action = st.sidebar.selectbox("Select Option Promotion Package:", ["addpromotionpackageGSM", "cancelpackageGSM"])
        
        if suboffering_action == "addpromotionpackageGSM":
            change_suboffering.addpromotionpackageGSM()
        elif suboffering_action == "cancelpackageGSM":
            change_suboffering.cancelpackageGSM()


    elif page == "Unbar":
        unbar.app()
    elif page == "About":
        about.app()
    elif page == "Logout":
        # Logout button
        login.logout()
    
    