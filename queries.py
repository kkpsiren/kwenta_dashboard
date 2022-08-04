
QUERY = """-- overall
with today as (select sum(price) as total_amount, 
  avg(price) as total_average_price,
  count(distinct(buyer_address)) as distinct_buyers, 
  count(distinct(seller_address)) as distinct_sellers, 
  count(distinct(nft_address)) as distinct_nfts,
  count(tx_hash) as total_sales,
  min(block_timestamp:: date) as min_date
  --, block_timestamp:: date as date, 
from optimism.core.ez_nft_sales
where platform_name = 'quixotic'
and currency_symbol = 'ETH'),
last_week as (
  select sum(price) as total_amount, 
  avg(price) as total_average_price,
  count(distinct(buyer_address)) as distinct_buyers, 
  count(distinct(seller_address)) as distinct_sellers, 
  count(distinct(nft_address)) as distinct_nfts,
  count(tx_hash) as total_sales,
  min(block_timestamp:: date) as min_date
  --, block_timestamp:: date as date, 
from optimism.core.ez_nft_sales
where platform_name = 'quixotic'
and currency_symbol = 'ETH'
and block_timestamp:: date < getdate()-interval '1 week'
)
select 'today' as date, *
from today
union ALL
select 'last_week' as date, *
from last_week
""" 

QUERY2 = """-- overall
select case 
  when project_name is not null then project_name
  when nft_address = '0x69a68eb548a37ee475d9f89646945588558796d1' then 'oliens'
  when nft_address = '0xbe81eabdbd437cba43e4c1c330c63022772c2520' then 'quixotic hack contract' 
  --https://twitter.com/apetimism/status/1542743841735749632
  else nft_address 
  end as name,nft_address, sum(price) as total_amount, 
  avg(price) as total_average_price,
  count(distinct(buyer_address)) as distinct_buyers, 
  count(distinct(seller_address)) as distinct_sellers, 
  count(tx_hash) as sales
  --, block_timestamp:: date as date, 
from optimism.core.ez_nft_sales
  left join optimism.core.dim_labels dl on address=nft_address
where platform_name = 'quixotic'
and currency_symbol = 'ETH'
group by 1,2"""
  