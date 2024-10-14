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
"""
polars.exceptions.SchemaError: invalid series dtype: expected `FixedSizeList`, got `list[str]`
"""

a = base.df_receipt.group_by('store_cd').agg(
    pl.col('product_cd').mode()
)

print(a)

b = a.select([
    'store_cd', 
    'product_cd'
]).sort('store_cd')


