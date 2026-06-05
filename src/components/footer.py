import streamlit as st





def footer_home():
    logo_url ="https://share.ftimg.com/aff/flamingtext/2018/05/11/flamingtext__25602573616417830.png"
    st.markdown(f"""
        <div style="margin-top:2rem;display:flex;gap:6px;justify-content:center;items-align:center">
        <p style="font-weight:bold;color:white;"> created with ❤️ by </p>
        <img src="{logo_url}" style="max-height:25px" />                              
        </div>





                """, unsafe_allow_html=True)
