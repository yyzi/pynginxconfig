# NginX configuration files parser and generator (NginxConfig) #
# Парсер и генератор конфигурационных файлов NginX (NginxConfig) #

## Quick links | Ссылки ##
[Download](https://pypi.python.org/packages/source/p/pynginxconfig/pynginxconfig-0.3.3.tar.gz#md5=0c0ca3150d4bafbb264a2906a30ec5a4)
[Documentation](http://code.google.com/p/pynginxconfig/wiki/Documentation) [(rus)](http://code.google.com/p/pynginxconfig/wiki/Documentation_ru)

### Check out trunk version here! | Оцените новую версию! ###
It is not compatible with version in this repo, but more stable and elegant! [Check it out](https://github.com/Winnerer/pynginxconfig)!
Новая версия лежит на github, более стабильная и красивая [Оцените](https://github.com/Winnerer/pynginxconfig)!

## About | О программе ##
**NginxConfig** is a python module for parsing and generating NginX configuration files. Module can parse blocks and single values of unlimited nesting.

---

**NginxConfig** - это модуль, предназначенный для разбора (парсинга) и генерации конфигурационных файлов NginX. Позволяет разбирать и генерировать конфигурационные файлы неограниченной вложенности.

## Features | Особенности ##
  * Generate syntactically correct configs
  * Works with Python 2 and 3 (by using a single code base)

---

  * Генерирует синтаксически правильные конфигурационные файлы NginX
  * Работает с версиями Python 2 и 3

## Quick start | Быстрый старт ##
```
pip install pynginxconfig
```
```
from pynginxconfig import NginxConfig
nc = NginxConfig()
nc.load('''
user  www www;
worker_processes  2;

events {
    connections   2000;
    ip_hash;

    # use [ kqueue | rtsig | epoll | /dev/poll | select | poll ];
    use kqueue;
}''')
print(nc.gen_config())
```
[More examples](http://code.google.com/p/pynginxconfig/wiki/Documentation) [(rus)](http://code.google.com/p/pynginxconfig/wiki/Documentation_ru)
<br>

<h2>Timeline</h2>
15.03.13 - ver. 0.1 released<br>
17.03.13 - 0.2 - New delete interface<br>
17.03.13 - 0.2.2 - Fixed double new line in generating config<br>
18.03.13 - 0.3.0 - Rewritten get, get_value, remove; added set (modify).<br>
20.03.13 - 0.3.1 - Bugfixes, added savef, loadf (saves and loads from file)<br>
0.3.2 is just repack of 0.3.1<br>
08.12.13 - 0.3.3 - Updated function to load and safe from file; Fix parameters without value<br>

<h2>TODO</h2>
<ul><li>Add more exceptions and checks<br>
</li><li>Add comments parsing (?)<br>
</li><li>Add sorting of parameters (first params, then blocks)<br>
</li><li>Add documentation for exceptions