import os
import polars as pl

dtypes = {
    'customer_id': str,
    'gender_cd': str,
    'postal_cd': str,
    'application_store_cd': str,
    'status_cd': str,
    'category_major_cd': str,
    'category_medium_cd': str,
    'category_small_cd': str,
    'product_cd': str,
    'store_cd': str,
    'prefecture_cd': str,
    'tel_no': str,
    'postal_cd': str,
    'street': str,
    'application_date': str,
    'birth_day': pl.Date
}

df_customer = pl.read_csv("../data/customer.csv", dtypes=dtypes)
df_category = pl.read_csv("../data/category.csv", dtypes=dtypes)
df_product  = pl.read_csv("../data/product.csv",  dtypes=dtypes)
df_receipt  = pl.read_csv("../data/receipt.csv",  dtypes=dtypes)
df_store    = pl.read_csv("../data/store.csv",    dtypes=dtypes)
df_geocode  = pl.read_csv("../data/geocode.csv",  dtypes=dtypes)


