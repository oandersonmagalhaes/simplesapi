from os import getenv

#########################################################################
#   DATABASE                                                            #
#########################################################################
SIMPLES_DABASE_URL = getenv("SIMPLES_DABASE_URL", None)

#########################################################################
#   REDIS                                                               #
#########################################################################
SIMPLESAPI_CACHE_URL = getenv("SIMPLESAPI_CACHE_URL", None)
SIMPLESAPI_CACHE_SSL = str(getenv("SIMPLESAPI_CACHE_SSL", "true")).lower() in ["1","true"]

#########################################################################
#   AWS                                                                 #
#########################################################################
SIMPLES_AWS_LOCAL = getenv("SIMPLES_AWS_LOCAL", "false").lower() in ["1","true"]
SIMPLES_AWS_ACCESS_KEY_ID = getenv("SIMPLES_AWS_ACCESS_KEY_ID", None)
SIMPLES_AWS_SECRET_ACCESS_KEY = getenv("SIMPLES_AWS_SECRET_ACCESS_KEY", None)
SIMPLES_AWS_REGION_NAME = getenv("SIMPLES_AWS_REGION_NAME", "us-east-1")

#########################################################################
#   ENCRYPT                                                             #
#########################################################################
INTERNAL_SERVICE_TOKEN = getenv("INTERNAL_SERVICE_TOKEN", None)