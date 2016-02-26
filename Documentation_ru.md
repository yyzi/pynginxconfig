# Внимание! #
PyNginxConfig не генерирует правильные конфиги для nginx, он генерирует лишь **синтаксически правильные** конфигурационные файлы. Вся ответственность за их правильность ложится на плечи программиста.

# Установка #
Скачайте и распакуйте архив, далее выполните:
```
python setup.py install
```
Или через pip
```
pip install pynginxconfig
```

# Базовая инициализация #
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
Советую взять пример базовой конфигурации со страницы NginX [NginX documentation](http://nginx.org/ru/docs/example.html)

# Добавление параметров. #
## Добавление одиночного текстового параметра ##
```
nc.append(('user', 'www www'))
```
## Добавление параметра в определённую позицию ##
```
nc.append(('user', 'www www'), position=1)
```
## Добавление блока данных ##
```
nc.append({'name':'events', 'param':'', 'value':[('connections', '2000'), ('use', 'kqueue')]})
```
## Добавление многострочного параметра ##
```
nc.append(('multiline', ['big', 'multiline', 'value']))
```

# Структуры в [data](data.md) #
Одиночный текстовый параметр:
```
('name', 'value')
```
Пример генерации:
```
name value;
```

## Многострочный параметр ##
```
('name', ['some', 'values', 'here'])
```
Пример генерации:
```
name some
     values
     here;
```

## Блок параметров. ##
```
{'name': 'location', 'param': '/', 'value': [('param1', '2000'), ('use', 'kqueue')]}
```
Пример генерации:
```
location / {
    param1 2000;
    use kqueue;
}
```

# Получение параметров: #
```
nc[0]
```
или
```
nc.get('user')
```

# Получение блоков: #
```
nc.get(('events',))
```
```
nc.get_value(nc.get([('http',), ('server',), ('location', '/404.html')]))
```

# Получение параметра в блоке #
```
nc.get_value(nc.get([('http',), ('server',), ('location', '/404.html'), 'charset']))
```

## Получение значений ##
```
nc.get_value(nc.get('user'))
```

## Изменение данных параметра. ##
```
nc.set([('events',), 'connections'], '100')
```

## Удаление параметров. ##
```
nc.remove('user')
nc.remove(['user'])
```
```
# Обратите внимание на запятые
nc.remove([('http',), ('server',), ('location', '/404.html'), 'root'])
```

## Удаление блоков. ##
```
nc.remove([('http',), ('server',), ('location', '/404.html')])

nc.remove([('http', '')])
nc.remove(('http', ''))
```