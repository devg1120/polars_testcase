import base as B


t = B.df_receipt.select(['sales_ymd', 'customer_id', 'product_cd', 'amount']).head(10)
print(t)
