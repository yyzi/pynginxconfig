# Attention! #
PyNginxConfig does not generate correct config from nginx position, it just gives interface to generate **syntactically correct** configs.

# Installation #
Download and extract package, then:
```
python setup.py install
```
Or use **pip**
```
pip install pynginxconfig
```

# Basic initialization #
```
from pynginxconfig import NginxConfig
nc = NginxConfig()
nc.load('''
user  www www;
worker_processes  2;

events {
    connections   2000;

    # use [ kqueue | rtsig | epoll | /dev/poll | select | poll ];
    use kqueue;
}

http {
     server {
        location /404.html {
            root  /spool/www;

            charset         on;
            source_charset  koi8-r;
        }
    }
}
''')
print(nc.gen_config())
```
I recommend to use config from [NginX documentation](http://nginx.org/ru/docs/example.html)

# Adding data. #
## Appending single parameter ##
```
nc.append(('user', 'www www'))
```
## Appending data to position ##
```
nc.append(('user', 'www www'), position=1)
```
## Adding block of data ##
```
nc.append({'name':'events', 'param':'', 'value':[('connections', '2000'), ('use', 'kqueue')]})
```
## Adding multiline params ##
```
nc.append(('multiline', ['big', 'multiline', 'value']))
```

# Structures in [data](data.md) #
Single parameter. Example of parameter:
```
('name', 'value')
```
Example of generating:
```
name value;
```

## Multiline parameter ##
```
('name', ['some', 'values', 'here'])
```
Example of generating:
```
name some
     values
     here;
```

## Block of parameters ##
```
{'name': 'location', 'param': '/', 'value': [('param1', '2000'), ('use', 'kqueue')]}
```
Example of generating:
```
location / {
    param1 2000;
    use kqueue;
}
```

# Getting parameters #
```
nc[0]
```
или
```
nc.get('user')
```

## Getting block ##
```
nc.get(('events',))
```
```
nc.get_value(nc.get([('http',), ('server',), ('location', '/404.html')]))
```

## Getting data in block ##
```
nc.get_value(nc.get([('http',), ('server',), ('location', '/404.html'), 'charset']))
```

## Getting values ##
```
nc.get_value(nc.get('user'))
```

## Modifying parameters ##
```
nc.set([('events',), 'connections'], '100')
```

# Removing #
## Removing parameters ##
```
nc.remove('user')
nc.remove(['user'])
```
```
# Pay attention on commas
nc.remove([('http',), ('server',), ('location', '/404.html'), 'root'])
```

## Removing blocks ##
```
nc.remove([('http',), ('server',), ('location', '/404.html')])

nc.remove([('http', '')])
nc.remove(('http', ''))
```nc.remove([('http',), ('server',), ('location', '/404.html')])

nc.remove([('http', '')])
nc.remove(('http', ''))
}}}```