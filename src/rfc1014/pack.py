import struct
from io import BytesIO

class Pack:
    def __init__(self,na=None):
        self.__name__ = na
    def __repr__(self):
        s = 'Pack<{}>'.format(self.__name__)
        for k,v in self.__dict__.items():
            if k=='__name__':
                continue
            if v.__class__==self.__class__:
                s += '\n\t- {} Pack<{}>'.format(k, v.__name__)
            else:
                s+='\n\t- {} <{}>'.format(k,v)
        return s
    def get(self,k):
        return self.__dict__.get(k)
    def set(self,k,v):
        self.__dict__[k]=v
    def keys(self):
        return self.__dict__.keys()

class Packer:
    def __init__(self):
        self.reset()
    def reset(self):
        self.__buf = BytesIO()
    def get_buffer(self):
        return self.__buf.getvalue()
    def _fstring(self, n, s):
        if n < 0:
            raise ValueError('fstring size must be nonnegative')
        data = s[:n]
        n = ((n+3)//4)*4
        data = data + (n - len(data)) * b'\0'
        self.__buf.write(data)
    def _array(self,ary,typedef,limit=None,fixed=None):
        n = len(ary)
        if not fixed is None:
            n = fixed
        elif not limit is None:
            n = min(n,limit)
        self.uint32_t(n)
        idx=0
        while idx<n:
            typedef(ary[idx])
            idx+=1
    def bool(self,x):
        if x: self.__buf.write(b'\0\0\0\1')
        else: self.__buf.write(b'\0\0\0\0')

    def opaque(self,s,fixed=None,limit=None):
        n = len(s)
        if not fixed is None:
            n = fixed
        elif not limit is None:
            n = min(n,limit)
            self.uint32_t(n)
        else:
            self.uint32_t(n)
        self._fstring(n, s)

    def int(self,x):
        self.__buf.write(struct.pack('>l', x))
    enum = int
    def uint(self,x):
        self.__buf.write(struct.pack('>L', x))
    def hyper(self,x):
        self.__buf.write(struct.pack('>q', x))
    def uhyper(self,x):
        self.__buf.write(struct.pack('>Q', x))

class UnPacker:
    def __init__(self, data=None):
        if data:
            self.read(data)
    def _info(self):
        print(self.__pos,len(self.__buf))
    def read(self, data):
        self.__buf = data
        self.__pos = 0
    def done(self):
        if self.__pos < len(self.__buf):
            raise Exception('unextracted data remains')
    def _fstring(self, n):
        if n < 0:
            raise ValueError('fstring size must be nonnegative')
        i = self.__pos
        j = i + (n+3)//4*4
        if j > len(self.__buf):
            raise EOFError
        self.__pos = j
        return self.__buf[i:i+n]
    def _array(self,typedef,limit=None,fixed=None):
        n = self.uint32_t()
        result = []
        idx=0
        while idx<n:
            result.append(typedef())
            idx+=1
        return result

    def bool(self):
        return bool(self.int())
    def opaque(self,fixed=None,limit=None):
        if fixed is None:
            n = self.uint32_t()
        else:
            n = fixed
        return self._fstring(n)
    string = opaque
    def int(self):
        i = self.__pos
        self.__pos = j = i+4
        data = self.__buf[i:j]
        if len(data) < 4:
            raise EOFError
        return struct.unpack('>l', data)[0]
    enum = int
    def uint(self):
        i = self.__pos
        self.__pos = j = i+4
        data = self.__buf[i:j]
        if len(data) < 4:
            raise EOFError
        return struct.unpack('>L', data)[0]

    def hyper(self):
        i = self.__pos
        self.__pos = j = i+8
        data = self.__buf[i:j]
        if len(data) < 8:
            raise EOFError
        return struct.unpack('>q', data)[0]
    def uhyper(self):
        i = self.__pos
        self.__pos = j = i+8
        data = self.__buf[i:j]
        if len(data) < 8:
            raise EOFError
        return struct.unpack('>Q', data)[0]