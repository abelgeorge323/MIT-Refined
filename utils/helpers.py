import streamlit as st

def metric_card(container, label, value, link=None):
    if link:
        if st.button(label, key=label):
            st.switch_page(link)
    else:
        container.metric(label, value)
