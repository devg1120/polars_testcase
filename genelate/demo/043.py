import base
import polars as pl



"""
t = base.df_receipt.group_by('store_cd').agg(
    pl.col('product_cd').mode()
).select([
    'store_cd', 
    pl.col('product_cd').arr.first()
]).sort('store_cd')

print(t)
"""

gender_mapping = {
    '0': 'male',
    '1': 'female',
    '9': 'unknown'
}

ans = (base.df_customer
    .join(base.df_receipt, how='left', on='customer_id')
    .with_columns([
        ((pl.col('age') / 10).floor() * 10).alias('era'),
        pl.col('gender_cd').replace_strict(gender_mapping).alias('gender')
    ])
    .group_by(['gender', 'era']).agg(pl.col('amount').sum())
 #.pivot(values='amount', index='era', columns='gender')
    .pivot(values='amount', index='era', on='gender')
    .sort('era')
)

print(ans)
