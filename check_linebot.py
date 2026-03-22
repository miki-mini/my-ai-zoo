import os
import sys

from linebot.v3.messaging import (
    ApiClient,
    MessagingApi,
    TextMessage,
    BroadcastRequest,
    Configuration
)

print(dir(MessagingApi))

import inspect
print(inspect.signature(MessagingApi.broadcast))
