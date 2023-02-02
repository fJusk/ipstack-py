# ipstack-py

### General
This module implements a client for accessing the [ipstack API](https://ipstack.com/documentation). It uses the requests library and models from pydantic for validating API responses.

Here is an example of using the client:

#### 1. Initialization
```py
  from ipstackpy import IpStackClient
  
  # Access key (insert your key)
  key = 'fa260c650d36bq38f719235ff938b8f15'
  
  # Initialization client
  client = IpStackClient(access_key=key)
  
  # or
  client = IpStackClient(key)
```
#### 2. Standard lookup
```py
  # ip address
  ip = '138.213.0.0'
  
  # request to API
  search_result = client.lookup(ip)
  
  # print results
  print(search_result.city)       # Tokyo
  print(search_result.latitude)   # 35.69628143310547
  print(search_result.longitude)  # 139.73855590820312
```
#### 3. Bulk IP lookup
```py
  # ip addresses
  ips = [ '138.213.0.0', '194.105.0.0', '156.023.0.0' ]
  
  # request to API
  search_results = client.lookup(ips)
  
  # print results
  for result in search_results:
      print(search_result.city)
```
**Output:**
```
  Tokyo
  Bucharest
  Santa Clara
```

### Installation
```
pip install git+https://github.com/fJusk/ipstack-py.git#egg=ipstackpy
```

