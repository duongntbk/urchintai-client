# urchintai-client Package

This is a simple client for UR Chintai API (UR都市機構) written in Python.

Please see my blog post at the link below for more information regarding the API.

[https://duongnt.com/urchintai-api](https://duongnt.com/urchintai-api)

## Install

You can install `urchintai-client` using pip, just run the following command in the command line.
> pip install urchintai-client

## Usage

**Note**: all calls to remote API are executed asynchronously.

### Create client object
```
from urchintai_client.request_sender import RequestSender

# Create your aiohttp session object, we will call it sess
sender = RequestSender(sess) # this object is used to send request to and receive response from API
client = UrClient(sender)
```

You can choose to create and use your own aiohttp session, or you can use this helper class to create and manager session.
```
from urchintai_client.session_manager import SessionManager

sess = SessionManager.GetSession()
```

In this case you can call the following method to close the session and release resource.
```
await SessionManager.CloseSession()
```

### Check if a property has vacant room(s)

Call `is_property_vacant` method and pass the URL of the property you want to check.
```
url = 'https://www.ur-net.go.jp/chintai/kanto/kanagawa/40_2460.html'
is_vacant = await client.is_property_vacant(url)
```

If you know the property code, you can use it to check for vacancy.
```
property_code = {
    'store_code': '40',
    'house_code': '246',
    'type': '0'
}
is_vacant = await client.is_property_vacant(property_code)
```

### Find the name of a property

Call `get_property_name` method and pass the URL of the property.
```
url = 'https://www.ur-net.go.jp/chintai/kanto/kanagawa/40_2460.html'
name = await client.get_property_name(url)
```

### Check if a room is vacant

Call `is_room_vacant` method and pass the URL of the room you want to check.
```
url = 'https://www.ur-net.go.jp/chintai/kanto/kanagawa/40_2460_room.html?JKSS=000020654'
is_vacant = await client.is_room_vacant(url)
```

If you know the room code, you can use it to check for vacancy.
```
room_code = {
    'store_code': '40',
    'house_code': '246',
    'type': '0',
    'room_id': '000020654'
}
is_vacant = await client.is_room_vacant(room_code)
```

### Run test from terminal

Below is how we run `get_property_name` from python terminal. It should work as is as long as all dependencies are installed.
```
import asyncio

from urchintai_client.session_manager import SessionManager
from urchintai_client.request_sender import RequestSender
from urchintai_client.ur_client import UrClient

sender = RequestSender(SessionManager.GetSession())
client = UrClient(sender)

url = 'https://www.ur-net.go.jp/chintai/kanto/kanagawa/40_2460.html'
loop = asyncio.get_event_loop()
name = loop.run_until_complete(client.get_property_name(url))
print(f'Property name: {name}')

loop.run_until_complete(SessionManager.CloseSession()) # Don't forgot to close the session
```

This should print the following message to console.
```
Property name: 西久保町公園ハイツ
```
