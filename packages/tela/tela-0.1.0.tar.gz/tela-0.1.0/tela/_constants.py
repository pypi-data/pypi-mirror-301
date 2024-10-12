import httpx

RAW_RESPONSE_HEADER = "X-Custom-Raw-Response"
OVERRIDE_CAST_TO_HEADER = "____custom_override_cast_to"

# default timeout is 0
DEFAULT_TIMEOUT = httpx.Timeout(None)
DEFAULT_MAX_RETRIES = 3
DEFAULT_CONNECTION_LIMITS = httpx.Limits(max_connections=1000, max_keepalive_connections=100)

INITIAL_RETRY_DELAY = 0.5
MAX_RETRY_DELAY = 8.0
