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
    st.sidebar.title("Kwenta Dashboard")
    st.sidebar.markdown("""
With [Kwenta](https://kwenta.io/), you can trade commodities, forex, crypto, and more with up to 25x leverage and deep liquidity.  
Essentially the liquidity comes from the Synthetix futures markets that enable users to a leveraged exposure to an asset, long or short.
The user must post some margin in order to open a futures account, and profits/losses are
 continually tallied against this margin. If a user's margin runs out, then their position is closed
 by a liquidation keeper, which is rewarded with a flat fee extracted from the margin.

 The Synthetix debt pool is effectively the counterparty to each trade, so if a particular position
 is in profit, then the debt pool pays by issuing sUSD into their margin account,
 while if the position makes a loss then the debt pool burns sUSD from the margin, reducing the
 debt load in the system.
                     """)

    
    d = load_historical()
    d0, d1 = run_queries()
    layout_selected = st.radio('Select',['Overall','User'],horizontal=True)
    if layout_selected=='Overall':

        selected_flow_market = st.selectbox('Select Market', ['All']+d1['MARKET'].unique().tolist())
        st.header(f'{selected_flow_market}')
        if selected_flow_market=='All':
            
            st.subheader('Deposits vs Withdraws')
            st.write("This figure shows how much all markets are seeing combined deposits and withdraws")
            
            st.plotly_chart(plot_bar(d1, x0='DEPOSITS',x1='WITHDRAWS'),use_container_width=True) 
            
            st.subheader('Difference')
            st.write("This figure shows what is the absolute difference between the deposits and withdraws accross all markets")

            fig = plot_bar2(d1.groupby('DATE')[['CUMULATIVE_SUM','AMOUNT_IN']].sum().reset_index().sort_values(by='DATE'), x0='CUMULATIVE_SUM', x1='AMOUNT_IN')     
            st.plotly_chart(fig,use_container_width=True)  

            st.subheader('Cumulative Difference')
            st.write("This figure shows accumulative difference between the deposits and withdraws accross all markets")

            fig = plot_area(d1.groupby('DATE')[['CUMULATIVE_SUM','AMOUNT_IN']].sum().reset_index().sort_values(by='DATE'), x0='CUMULATIVE_SUM', x1='AMOUNT_IN')     
            st.plotly_chart(fig,use_container_width=True)  
        else:
            st.subheader('Deposits vs Withdraws')
            st.write(f"This figure shows much the {selected_flow_market} market is seeing deposits and withdraws")

            st.plotly_chart(plot_bar(d1.query('MARKET==@selected_flow_market'), x0='DEPOSITS',x1='WITHDRAWS'),use_container_width=True)  
            fig = plot_bar2(d1.query('MARKET==@selected_flow_market'), x0='CUMULATIVE_SUM', x1='AMOUNT_IN')     
            
            st.subheader('Difference')
            st.write(f"This figure shows what is the absolute difference between the deposits and withdrawals in the {selected_flow_market} market")

            st.plotly_chart(fig,use_container_width=True)   
            
            st.subheader('Cumulative Difference')
            st.write(f"This figure shows accumulative difference between the deposits and withdraws in the {selected_flow_market} market")

            fig = plot_area(d1.query('MARKET==@selected_flow_market'), x0='CUMULATIVE_SUM', x1='AMOUNT_IN')     
            st.plotly_chart(fig,use_container_width=True)               
            
        with st.expander('Show Data'):
            st.dataframe(d1.style.background_gradient(cmap=cm))
            
    else:
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
                   
    st.sidebar.markdown("""
Text modified from Kwenta and Synthetix [Smart Contracts](https://github.com/Synthetixio/synthetix/blob/v2.75.2/contracts/FuturesMarket.sol)
                        """)               
    st.sidebar.write("""#### Powered by FlipsideCrypto Godmode and ShroomDK 🫡""")
    st.sidebar.markdown(f""" 
### 💻 Github
[kkpsiren/kwenta_dashboard](https://github.com/kkpsiren/kwenta_dashboard)  
    """)
    with st.expander("Show queries"):
        st.markdown(f"""#### Query 1 for user deposit/withdrawal
```
{QUERY}
```""")
        st.markdown(f"""#### Query 2 for daily deposit/withdrawal" 
```
{QUERY2}
```""")
        st.markdown(f"""#### Query 3 for user trading activity" 
```
{QUERY3}
```""")