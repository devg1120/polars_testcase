import base
import polars as pl



"""
t = base.df_receipt.group_by('store_cd').agg(
    pl.col('product_cd').mode()
).select([
    'store_cd', 
    pl.col('product_cd').arr.first()
]).sort('store_cd')
"""

"""
df_data = df_receipt.filter(pl.col('customer_id').str.starts_with('Z').not_())

df_cnt = df_data.groupby('customer_id').agg(pl.col('sales_ymd').n_unique()).sort('sales_ymd', descending=True).head(20)
df_sum = df_data.groupby('customer_id').agg(pl.col('amount').sum()).sort('amount', descending=True).head(20)

df_cnt.join(df_sum, how='outer', on='customer_id')
"""

df_data = eval("base.df_receipt.filter(pl.col('customer_id').str.starts_with('Z').not_())")

df_cnt = eval("df_data.group_by('customer_id').agg(pl.col('sales_ymd').n_unique()).sort('sales_ymd', descending=True).head(20)")

df_sum = eval("df_data.group_by('customer_id').agg(pl.col('amount').sum()).sort('amount', descending=True).head(20)")


t = eval("df_cnt.join(df_sum, how='outer', on='customer_id')")

print(t)

