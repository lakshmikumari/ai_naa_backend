import os
from urllib.parse import quote_plus

""" DB credentials """
MONGO_DB = "NAA"
MONGO_COMMOM_DB = "NAA_UAD"
s3_access_key = "S3_ACCESS_KEY"
s3_secret_key = "S3_SECRET_KEY"
MONGO_HOST_CONNECTION = os.getenv('AI_MONGO_CONNECTION')
prod_auth = os.getenv('prod_Auth')
#MONGO_HOST_CONNECTION = f"mongodb+srv://auditadmin:Gz4jUpjLVPcy4ei@audit-dev-cluster0.4e847.mongodb.net/"
#prod_auth = f"https://cloudsso.cisco.com/as/token.oauth2?grant_type=password&client_secret=xElm80sHcvw2AWQs==&client_id=auditinsight_prod_client&username=pinuserprod.gen&password=Insights@12345"



