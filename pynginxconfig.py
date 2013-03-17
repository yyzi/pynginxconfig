'''
======================================================================================================
Copyright (c) 2013, Makarov Yurii 

               All rights reserved.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial
portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
======================================================================================================
'''

class NginxConfig:
    def __init__(self, offset_char=' '):
        self.i = 0 #char iterator for parsing
        self.length = 0
        self.config = ''
        self.data = []
        self.off_char = offset_char

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, value):
        self.data[index] = value

    def __delitem__(self, index):
        del self.data[index]
    
    def get(self, item, data=[], param=None):
        if data == []:
            data = self.data
        for d in data:
            if isinstance(d, tuple) and d[0] == item:
                return d
            elif isinstance(d, dict):
                if (d['name'] == item) and (param is None or param == d['param']):
                    return d
        return None

    def get_value(self, item, data=[], param=None):
        rez = self.get(item, data, param)
        if isinstance(rez, tuple):
            return rez[1]
        elif isinstance(rez, dict):
            return rez['value']
        else:
            return rez

    def append(self, item, root=[], position=None):
        if root == []:
            root = self.data
        elif root is None:
            raise AttributeError('Root element is None')
        if position:
            root.insert(position, item)
        else:
            root.append(item)

    def remove(self, item_arr, data=[]):
        if data == []:
            data = self.data
        if type(item_arr) in [str, tuple]:
            item = item_arr
        elif isinstance(item_arr, list):
            if len(item_arr) == 1:
                item = item_arr[0]
            else:
                elem = item_arr.pop(0)
                if isinstance(elem, str):
                    self.remove(item_arr, self.get_value(elem, data))
                elif isinstance(elem, tuple):
                    self.remove(item_arr, self.get_value(elem[0], data, param=elem[1]))
                    return

        if isinstance(item, str):
            for i,elem in enumerate(data):
                if isinstance(elem, tuple):
                    if elem[0] == item:
                        del data[i]
                        return
        elif isinstance(item, tuple):
            for i,elem in enumerate(data):
                if isinstance(elem, dict):
                    if (elem['name'], elem['param']) == item:
                        del data[i]
                        return
        else:
            raise AttributeError("Unknown item type '%s' in item_arr" % item.__class__.__name__)

    def load(self, config):
        self.config = config
        self.length = len(config) - 1
        self.i = 0
        self.data = self.parse_block()

    def parse_block(self, name=''):
        data = []
        param_name = None
        param_value = None
        buf = ''
        while self.i < self.length:
            if self.config[self.i] == '\n': #multiline value
                if buf and param_name:
                    if param_value is None:
                        param_value = []
                    param_value.append(buf.strip())
                    buf = ''
            elif self.config[self.i] == ' ':
                if not param_name and len(buf.strip()) > 0:
                    param_name = buf.strip()
                    buf = ''
                else:
                    buf += self.config[self.i]
            elif self.config[self.i] == ';':
                if isinstance(param_value, list):
                    param_value.append(buf.strip())
                else:
                    param_value = buf.strip()
                data.append((param_name, param_value))
                param_name = None
                param_value = None
                buf = ''
            elif self.config[self.i] == '{':
                self.i += 1
                block = self.parse_block(name+':'+param_name)
                data.append({'name':param_name, 'param':buf.strip(), 'value':block})
                param_name = None
                param_value = None
                buf = ''
            elif self.config[self.i] == '}':
                self.i += 1
                return data
            elif self.config[self.i] == '#': #skip comments
                while self.i < self.length and self.config[self.i] != '\n':
                    self.i += 1
            else:
                buf += self.config[self.i]
            self.i += 1
        return data

    def gen_block(self, blocks, offset):
        subrez = '' # ready to return string
        block_name = None
        block_param = ''
        for i, block in enumerate(blocks):
            if isinstance(block, tuple):
                if isinstance(block[1], str):
                    subrez += self.off_char * offset + '%s %s;\n' % (block[0], block[1])
                else: #multiline
                    subrez += self.off_char * offset + '%s %s;\n' % (block[0], 
                        self.gen_block(block[1], offset + len(block[0]) + 1))

            elif isinstance(block, dict):
                block_value = self.gen_block(block['value'], offset + 4)
                if block['param']:
                    param = block['param'] + ' '
                else:
                    param = ''
                if subrez != '':
                    subrez += '\n'
                subrez += '%(offset)s%(name)s %(param)s{\n%(data)s%(offset)s}\n' % {
                    'offset':self.off_char * offset, 'name':block['name'], 'data':block_value,
                    'param':param}

            elif isinstance(block, str): #multiline params
                if i == 0:
                    subrez += '%s\n' % block
                else:
                    subrez += '%s%s\n' % (self.off_char * offset, block)

        if block_name:
            return '%(offset)s%(name)s %(param)s{\n%(data)s%(offset)s}\n' % {
                'offset':self.off_char * offset, 'name':block_name, 'data':subrez,
                'param':block_param}
        else:
            return subrez

    def gen_config(self, offset_char=' '):
        self.off_char = offset_char
        return self.gen_block(self.data, 0)
