import streamlit as st
import pandas as pd
from scripts import run_queries
from plots import * 
from queries import *
import datetime
#cm = sns.light_palette("green", as_cmap=True)
#   with st.expander('show list'):
#        st.dataframe(data.sort_values(by='USD',ascending=False).style.background_gradient(cmap=cm))
import seaborn as sns
pd.set_option('display.width', 1400)
cm = sns.light_palette("green", as_cmap=True)


def get_change(ser,previous,what='NEW_ADDRESS'):
    if what =='USER':
        a = ser['USERS_DOING_TRANSACTIONS']+ser['USERS_RECEIVING_TOKENS']
        b = previous['USERS_DOING_TRANSACTIONS']+previous['USERS_RECEIVING_TOKENS']
        change = f"{((a / b)-1)*100:.2f} %"
        
    else:
        change = f"{((ser[what] / previous[what])-1)*100:.2f} %"
    return change


def landing_page():

    st.sidebar.image("https://optimistic.etherscan.io/images/logo-ether.svg?v=0.0.4",width=300)
    st.sidebar.title("kwenta_dashboard")
    
    html = 'https://velocity-app.flipsidecrypto.com/velocity/visuals/a1f233b7-0b46-48bf-adb3-4ac7cab994fc/c4dc49ca-f8c5-48ad-b6dc-3e6657ffa908'
    st.components.v1.iframe(html, width=900, height=800, scrolling=False)

    html = 'https://velocity-app.flipsidecrypto.com/velocity/visuals/0ab89787-3159-4cc4-a312-625efcbb99b9/c4dc49ca-f8c5-48ad-b6dc-3e6657ffa908'
    st.components.v1.iframe(html, width=900, height=800, scrolling=False)

    html = 'https://velocity-app.flipsidecrypto.com/velocity/visuals/d0db04aa-ecff-4858-a0e9-1ff042242b87/c4dc49ca-f8c5-48ad-b6dc-3e6657ffa908'
    st.components.v1.iframe(html, width=900, height=800, scrolling=False)

                     
    st.sidebar.write("""#### Powered by FlipsideCrypto Godmode and ShroomDK 🫡""")

    st.sidebar.markdown(f""" 
### 💻 Github
[kkpsiren/kwenta_dashboard](https://github.com/kkpsiren/kwenta_dashboard)  
    """)
    with st.expander("Show queries"):
        st.markdown(f"""#### Query 1 for metrics
```
{QUERY}
```""")
        st.markdown(f"""#### Query 2 for NFT specs" 
```
{QUERY2}
```""")