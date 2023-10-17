# bunnystream-api-python


### Usage to Sign the CDN Streams

To sign the Stream videos before loading it on your player. Example, on your mobile app player where you cannot embed the Bunny stream code.


```py
from bunny-sign import *
url = "https://{CDN}/{VideoID}/playlist.m3u8"
securityKey = "{APIKEY}"
path_allowed = "/"
url_to_load = sign_bcdn_url(url, securityKey, path_allowed, True)
```

Replace `CDN`, `VideoID`, `APIKEY` with your relevant values.