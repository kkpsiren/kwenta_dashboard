
QUERY = """with transfers as (
  select block_timestamp, 
  event_inputs:from as transfer_from, 
  event_inputs:to as transfer_to, 
  to_number(event_inputs:value) / pow(10,18) as amount,
  tx_hash,
  case
  when origin_to_address = lower('0x001b7876F567f0b3A639332Ed1e363839c6d85e2') then 'AAVE'
when origin_to_address = lower('0xFe00395ec846240dc693e92AB2Dd720F94765Aa3') then 'APE'
when origin_to_address = lower('0x4ff54624D5FB61C34c634c3314Ed3BfE4dBB665a') then 'AVAX'
when origin_to_address = lower('0xEe8804d8Ad10b0C3aD1Bd57AC3737242aD24bB95') then 'BTC'
when origin_to_address = lower('0x10305C1854d6DB8A1060dF60bDF8A8B2981249Cf') then 'DYDX'
when origin_to_address = lower('0xf86048DFf23cF130107dfB4e6386f574231a5C65') then 'ETH'
when origin_to_address = lower('0xad44873632840144fFC97b2D1de716f6E2cF0366') then 'EUR'
when origin_to_address = lower('0x1228c7D8BBc5bC53DB181bD7B1fcE765aa83bF8A') then 'LINK'
when origin_to_address = lower('0xbCB2D435045E16B059b2130b28BE70b5cA47bFE5') then 'MATIC'
when origin_to_address = lower('0xcF853f7f8F78B2B801095b66F8ba9c5f04dB1640') then 'SOL'
when origin_to_address = lower('0x5Af0072617F7f2AEB0e314e2faD1DE0231Ba97cD') then 'UNI'
when origin_to_address = lower('0xb147C69BEe211F57290a6cde9d1BAbfD0DCF3Ea3') then 'XAG'
when origin_to_address = lower('0x4434f56ddBdE28fab08C4AE71970a06B300F8881') then 'XAU'
  end as market
from optimism.core.fact_event_logs
where --tx_hash = '0xd46bbf6ba8be63fc9e8ef1731245e18c1a3484dfffcf8c66bd513fb7b9f38c45'
event_name = 'Transfer'
  and contract_address = '0x8c6f28f2f1a3c87f0f938b96d27520d9751ec8d9' -- sUSD
    and origin_to_address in (lower('0x001b7876F567f0b3A639332Ed1e363839c6d85e2'),
  								lower('0xFe00395ec846240dc693e92AB2Dd720F94765Aa3'),
  								lower('0x4ff54624D5FB61C34c634c3314Ed3BfE4dBB665a'),
  								lower('0xEe8804d8Ad10b0C3aD1Bd57AC3737242aD24bB95'),
  								lower('0x10305C1854d6DB8A1060dF60bDF8A8B2981249Cf'),
  								lower('0xf86048DFf23cF130107dfB4e6386f574231a5C65'),
  								lower('0xad44873632840144fFC97b2D1de716f6E2cF0366'),
  								lower('0x1228c7D8BBc5bC53DB181bD7B1fcE765aa83bF8A'),
  								lower('0xbCB2D435045E16B059b2130b28BE70b5cA47bFE5'),
  								lower('0xcF853f7f8F78B2B801095b66F8ba9c5f04dB1640'),
  								lower('0x5Af0072617F7f2AEB0e314e2faD1DE0231Ba97cD'),
  								lower('0xb147C69BEe211F57290a6cde9d1BAbfD0DCF3Ea3'),
  								lower('0x4434f56ddBdE28fab08C4AE71970a06B300F8881'))
  --and origin_function_signature = '0x88a3c848'
),
deposits as (
  select market, block_timestamp, TRANSFER_FROM as address, amount as deposit_amount,
  sum(amount) over (partition by address order by block_timestamp) as cumulative_deposit_amount
  from transfers
  where TRANSFER_TO='0x0000000000000000000000000000000000000000'
),
withdrawals as (
  select market, block_timestamp, TRANSFER_TO as address, amount as withdrawal_amount,
  sum(amount) over (partition by address order by block_timestamp) as cumulative_withdrawal_amount
  from transfers
  where TRANSFER_FROM='0x0000000000000000000000000000000000000000'
),
user_deposit as (
  select d.address, count(deposit_amount) as deposit_counts, sum(deposit_amount) as deposit_summed
from deposits d
  group by 1
),
user_withdrawal as (
  select d.address, count(withdrawal_amount) as withdrawal_counts, sum(withdrawal_amount) as withdrawal_summed
from withdrawals d
  group by 1
)
select d.address, deposit_summed, (ifnull(withdrawal_summed,0)-deposit_summed) as out_amount
from user_deposit d
left join user_withdrawal w on d.address=w.address
order by 3 desc nulls last
""" 

QUERY2 = """with transfers as (
  select block_timestamp, 
  event_inputs:from as transfer_from, 
  event_inputs:to as transfer_to, 
  to_number(event_inputs:value) / pow(10,18) as amount,
  tx_hash,
  case
  when origin_to_address = lower('0x001b7876F567f0b3A639332Ed1e363839c6d85e2') then 'AAVE'
when origin_to_address = lower('0xFe00395ec846240dc693e92AB2Dd720F94765Aa3') then 'APE'
when origin_to_address = lower('0x4ff54624D5FB61C34c634c3314Ed3BfE4dBB665a') then 'AVAX'
when origin_to_address = lower('0xEe8804d8Ad10b0C3aD1Bd57AC3737242aD24bB95') then 'BTC'
when origin_to_address = lower('0x10305C1854d6DB8A1060dF60bDF8A8B2981249Cf') then 'DYDX'
when origin_to_address = lower('0xf86048DFf23cF130107dfB4e6386f574231a5C65') then 'ETH'
when origin_to_address = lower('0xad44873632840144fFC97b2D1de716f6E2cF0366') then 'EUR'
when origin_to_address = lower('0x1228c7D8BBc5bC53DB181bD7B1fcE765aa83bF8A') then 'LINK'
when origin_to_address = lower('0xbCB2D435045E16B059b2130b28BE70b5cA47bFE5') then 'MATIC'
when origin_to_address = lower('0xcF853f7f8F78B2B801095b66F8ba9c5f04dB1640') then 'SOL'
when origin_to_address = lower('0x5Af0072617F7f2AEB0e314e2faD1DE0231Ba97cD') then 'UNI'
when origin_to_address = lower('0xb147C69BEe211F57290a6cde9d1BAbfD0DCF3Ea3') then 'XAG'
when origin_to_address = lower('0x4434f56ddBdE28fab08C4AE71970a06B300F8881') then 'XAU'
  end as market
from optimism.core.fact_event_logs
where --tx_hash = '0xd46bbf6ba8be63fc9e8ef1731245e18c1a3484dfffcf8c66bd513fb7b9f38c45'
event_name = 'Transfer'
  and contract_address = '0x8c6f28f2f1a3c87f0f938b96d27520d9751ec8d9' -- sUSD
    and origin_to_address in (lower('0x001b7876F567f0b3A639332Ed1e363839c6d85e2'),
  								lower('0xFe00395ec846240dc693e92AB2Dd720F94765Aa3'),
  								lower('0x4ff54624D5FB61C34c634c3314Ed3BfE4dBB665a'),
  								lower('0xEe8804d8Ad10b0C3aD1Bd57AC3737242aD24bB95'),
  								lower('0x10305C1854d6DB8A1060dF60bDF8A8B2981249Cf'),
  								lower('0xf86048DFf23cF130107dfB4e6386f574231a5C65'),
  								lower('0xad44873632840144fFC97b2D1de716f6E2cF0366'),
  								lower('0x1228c7D8BBc5bC53DB181bD7B1fcE765aa83bF8A'),
  								lower('0xbCB2D435045E16B059b2130b28BE70b5cA47bFE5'),
  								lower('0xcF853f7f8F78B2B801095b66F8ba9c5f04dB1640'),
  								lower('0x5Af0072617F7f2AEB0e314e2faD1DE0231Ba97cD'),
  								lower('0xb147C69BEe211F57290a6cde9d1BAbfD0DCF3Ea3'),
  								lower('0x4434f56ddBdE28fab08C4AE71970a06B300F8881'))
  --and origin_function_signature = '0x88a3c848'
),
deposits as (
  select market, block_timestamp, TRANSFER_FROM as address, amount as deposit_amount,
  sum(amount) over (partition by address order by block_timestamp) as cumulative_deposit_amount
  from transfers
  where TRANSFER_TO='0x0000000000000000000000000000000000000000'
),
withdrawals as (
  select market, block_timestamp, TRANSFER_TO as address, amount as withdrawal_amount,
  sum(amount) over (partition by address order by block_timestamp) as cumulative_withdrawal_amount
  from transfers
  where TRANSFER_FROM='0x0000000000000000000000000000000000000000'
),
user_deposit as (
  select d.block_timestamp:: date as date,market, count(deposit_amount) as deposit_counts, sum(deposit_amount) as deposit_summed
from deposits d
  group by 1,2
),
user_withdrawal as (
  select d.block_timestamp:: date as date,market, count(withdrawal_amount) as withdrawal_counts, sum(withdrawal_amount) as withdrawal_summed
from withdrawals d
  group by 1,2
)
select ifnull(d.date,w.date) as date, ifnull(d.market,w.market) as market, 
  ifnull(deposit_summed,0) as deposits, 
  -1*ifnull(withdrawal_summed,0) as withdraws, 
  (deposits+withdraws) as amount_in, 
  sum(deposits+withdraws) over (partition by ifnull(d.market,w.market) order by ifnull(d.date,w.date)) as cumulative_sum
from user_deposit d
full outer join user_withdrawal w on d.date=w.date and d.market=w.market
  
order by 1 desc

"""
QUERY3 = """
with transfers as (
  select block_timestamp, 
  origin_from_address as trader,
  tokenflow_eth.hextoint(substr(data,3,64)) as margin,
  tokenflow_eth.hextoint(substr(data,67,64)) as size, 
  tokenflow_eth.hextoint(substr(data,131,64)) as tradeSize, 
  tokenflow_eth.hextoint(substr(data,195,64)) as lastPrice, 
  tokenflow_eth.hextoint(substr(data,259,64)) as fundingIndex,
  case
  when origin_to_address = lower('0x001b7876F567f0b3A639332Ed1e363839c6d85e2') then 'AAVE'
when origin_to_address = lower('0xFe00395ec846240dc693e92AB2Dd720F94765Aa3') then 'APE'
when origin_to_address = lower('0x4ff54624D5FB61C34c634c3314Ed3BfE4dBB665a') then 'AVAX'
when origin_to_address = lower('0xEe8804d8Ad10b0C3aD1Bd57AC3737242aD24bB95') then 'BTC'
when origin_to_address = lower('0x10305C1854d6DB8A1060dF60bDF8A8B2981249Cf') then 'DYDX'
when origin_to_address = lower('0xf86048DFf23cF130107dfB4e6386f574231a5C65') then 'ETH'
when origin_to_address = lower('0xad44873632840144fFC97b2D1de716f6E2cF0366') then 'EUR'
when origin_to_address = lower('0x1228c7D8BBc5bC53DB181bD7B1fcE765aa83bF8A') then 'LINK'
when origin_to_address = lower('0xbCB2D435045E16B059b2130b28BE70b5cA47bFE5') then 'MATIC'
when origin_to_address = lower('0xcF853f7f8F78B2B801095b66F8ba9c5f04dB1640') then 'SOL'
when origin_to_address = lower('0x5Af0072617F7f2AEB0e314e2faD1DE0231Ba97cD') then 'UNI'
when origin_to_address = lower('0xb147C69BEe211F57290a6cde9d1BAbfD0DCF3Ea3') then 'XAG'
when origin_to_address = lower('0x4434f56ddBdE28fab08C4AE71970a06B300F8881') then 'XAU'
  end as market,
  tx_hash
from optimism.core.fact_event_logs
where --tx_hash = '0xd46bbf6ba8be63fc9e8ef1731245e18c1a3484dfffcf8c66bd513fb7b9f38c45'
  --contract_address = '0x8c6f28f2f1a3c87f0f938b96d27520d9751ec8d9' -- sUSD
    origin_to_address in (lower('0x001b7876F567f0b3A639332Ed1e363839c6d85e2'),
  								lower('0xFe00395ec846240dc693e92AB2Dd720F94765Aa3'),
  								lower('0x4ff54624D5FB61C34c634c3314Ed3BfE4dBB665a'),
  								lower('0xEe8804d8Ad10b0C3aD1Bd57AC3737242aD24bB95'),
  								lower('0x10305C1854d6DB8A1060dF60bDF8A8B2981249Cf'),
  								lower('0xf86048DFf23cF130107dfB4e6386f574231a5C65'),
  								lower('0xad44873632840144fFC97b2D1de716f6E2cF0366'),
  								lower('0x1228c7D8BBc5bC53DB181bD7B1fcE765aa83bF8A'),
  								lower('0xbCB2D435045E16B059b2130b28BE70b5cA47bFE5'),
  								lower('0xcF853f7f8F78B2B801095b66F8ba9c5f04dB1640'),
  								lower('0x5Af0072617F7f2AEB0e314e2faD1DE0231Ba97cD'),
  								lower('0xb147C69BEe211F57290a6cde9d1BAbfD0DCF3Ea3'),
  								lower('0x4434f56ddBdE28fab08C4AE71970a06B300F8881'))
and topics[0] = '0x930fd93131df035ac630ef616ad4212af6370377bf327e905c2724cd01d95097'
and block_timestamp:: date > '2022-08-04'
  )
  
select *
from transfers
order by fundingindex
"""