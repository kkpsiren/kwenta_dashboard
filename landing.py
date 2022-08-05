import streamlit as st
import pandas as pd
from scripts import load_historical,run_queries
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
    
    d = load_historical()
    d0, d1 = run_queries()
    with st.expander('Money Flows'):
        st.dataframe(d1.style.background_gradient(cmap=cm))
    
    with st.expander('Top Users'):
        st.dataframe(d0.style.background_gradient(cmap=cm))
    
    
    trader = st.selectbox('Trader',d0['ADDRESS'].unique().tolist(),index=1)
    df_ = d.query('TRADER==@trader').copy()
    market = st.selectbox('Market',df_['MARKET'].unique().tolist())
    df = df_.query('MARKET==@market').copy()


    
    
    st.markdown(f"""Trader: *{trader}*  
[Etherscan](https://optimistic.etherscan.io/address/{trader})""")
    l,m,r = st.columns(3)
    with l:
        st.subheader('Market Events')
        st.write('\t'.join([f'{ser[0]}: **{ser[1]}**' for ser in df_['MARKET'].value_counts().iteritems()]))
    with m:
        st.subheader('Positions')
        st.write('\t'.join([f'{ser[0]}: **{ser[1]}**' for ser in df_['SIDE'].value_counts().iteritems()]))
    with r:
        st.subheader(f'Positions @{market}')
        st.write('\t'.join([f'{ser[0]}: **{ser[1]}**' for ser in df['SIDE'].value_counts().iteritems()]))
    l,m,r = st.columns(3)
    with m:
        st.subheader(f'Last Position')
        st.markdown(f"{df['SIDE'].iloc[-1]}")
    with r:
        st.subheader(f'Deposits - Withdrawals')
        st.markdown(f"{d0.query('ADDRESS==@trader')['OUT_AMOUNT'].iloc[0]:.2f} sUSD")
        
    st.subheader(f'{market}-PERP')
    with st.expander('Show Trades'):
        st.dataframe(df.sort_values(by='BLOCK_TIMESTAMP',ascending=False))
    st.plotly_chart(plot_history(df, 
                    x='BLOCK_TIMESTAMP',
                    y='MARGIN'),use_container_width=True)


    #html = 'https://velocity-app.flipsidecrypto.com/velocity/visuals/a1f233b7-0b46-48bf-adb3-4ac7cab994fc/c4dc49ca-f8c5-48ad-b6dc-3e6657ffa908'
    #st.components.v1.iframe(html, width=900, height=800, scrolling=False)
                     
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