from xdrparser import parse
import re
tab = ' '*4
default_type = ['int','uint','bool','opaque','hyper','uhyper','enum']
def convert_const(fd,const):
    k = ''
    for dat in const:
        kk = dat.get('k').split('_')[0]
        if kk!=k:
            fd.write('\n#{}\n'.format(kk))
            k = kk
        fd.write('{} = {}\n'.format(dat.get('k'),dat.get('v')))

def convert_enum(fd,enum):
    for dat in enum:
        k = dat.get('k')
        fd.write('\n#{}\n'.format(k))
        for c in dat.get('child'):
            fd.write('{} = {}\n'.format(c.get('k'), c.get('v')))
        fd.write('\n')
        fd.write(k+' = {\n')
        for c in dat.get('child'):
            fd.write('\'{k}\' : {v}, {v} : \'{k}\',\n'.format(k=c.get('k'), v=c.get('v')))
        fd.write('}\n')


def convert(xdr):
    fd = open('const.py','w')
    convert_const(fd,xdr.get('const'))
    convert_enum(fd, xdr.get('enum'))
    fd.close()

def get_ogrin_type(tp):
    if tp in ['opaque','string','utf8str_cis']:
        return 'opaque'
    return tp
def convert_n(n):
    if n is None:
        return 'None'
    if re.search('^[0-9]+$',n):
        return n
    else:
        return 'const.'+n

def parse_v(v):
    m = re.search('^(?P<v>[0-9a-zA-Z_]+)<(?P<n>[0-9a-zA-Z_]+)?>', v)
    if m:
        n = convert_n(m.groupdict().get('n'))
        v = m.groupdict().get('v')
        return {'n':n,'v':v,'v_tp':'limit'}
    m = re.search('^(?P<v>[0-9a-zA-Z_]+)\[(?P<n>[0-9a-zA-Z_]+)?\]', v)
    if m:
        n = convert_n(m.groupdict().get('n'))
        v = m.groupdict().get('v')
        return {'n':n,'v':v,'v_tp':'fixed'}

    m = re.search('^\*(?P<v>[0-9a-zA-Z_]+)', v)
    if m:
        v = m.groupdict().get('v')
        return { 'v': v, 'v_tp': 'recursive'}

def packer_val(fd,c,parent=None,ispack=True):
    tp = get_ogrin_type(c.get('tp'))
    info = parse_v(c.get('v'))
    if not info:
        if ispack:
            fd.write(tab * 2 + 'self.{tp}(pk.{v})\n'.format(**c))
        else:
            fd.write(tab * 2 + 'pk.{v} = self.{tp}()\n'.format(**c))
        return

    # print(info)
    if info.get('v_tp') in ['fixed','limit']:
        if tp in ['opaque']:
            if ispack:
                fd.write(tab * 2 + 'self.opaque(pk.{v},{v_tp}={n})\n'.format(tp=tp,**info))
            else:
                fd.write(tab * 2 + 'pk.{v} = self.opaque({v_tp}={n})\n'.format(tp=tp,**info))
        else:
            if ispack:
                fd.write(tab * 2 + 'self._array(pk.{v},self.{tp},{v_tp}={n})\n'.format(tp=tp,**info))
            else:
                fd.write(tab * 2 + 'pk.{v} = self._array(self.{tp},{v_tp}={n})\n'.format(tp=tp,**info))
        return

    if info.get('v_tp') == 'recursive':
        fd.write(tab * 2 + '# recursive {tp} {v} \n'.format(v=c.get('v'), tp=tp))

        if tp in ['opaque']:
            if ispack:
                fd.write(tab * 2 + 'self.opaque(pk.{v})\n'.format(tp=tp,**info))
            else:
                fd.write(tab * 2 + 'pk.{v} = self.opaque()\n'.format(tp=tp,**info))
        else:
            if ispack:
                fd.write(tab * 2 + 'self._array(pk.{v},self.{tp})\n'.format(tp=tp,**info))
            else:
                fd.write(tab * 2 + 'pk.{v} = self._array(self.{tp})\n'.format(tp=tp,**info))
        return


def write_typedef(fd,xdr,ispack=True):

    for dat in xdr.get('typedef'):
        tp = get_ogrin_type(dat.get('tp_d'))

        v = dat.get('v')
        info = parse_v(dat.get('v'))
        if not info:
            if tp in default_type:
                if ispack:
                    fd.write(tab + '{v} = Packer.{tp}\n'.format(v=v, tp=tp))
                else:
                    fd.write(tab + '{v} = UnPacker.{tp}\n'.format(v=v, tp=tp))
            else:
                fd.write(tab + '{v} = {tp}\n'.format(v=v, tp=tp))
            continue

        if tp in ['opaque'] and info.get('n') == 'None':
            if tp in default_type:
                if ispack:
                    fd.write(tab + '{v} = Packer.{tp}\n'.format(v=info.get('v'), tp=tp))
                else:
                    fd.write(tab + '{v} = UnPacker.{tp}\n'.format(v=info.get('v'), tp=tp))
            else:
                fd.write(tab + '{v} = {tp}\n'.format(v=info.get('v'), tp=tp))
            continue
        if ispack:
            fd.write(tab + 'def {fna}(self,x):\n'.format(fna=info.get('v')))
        else:
            fd.write(tab + 'def {fna}(self):\n'.format(fna=info.get('v')))
            # fd.write(tab * 2 + 'pk = Pack(\'{fna}\')\n'.format(fna=info.get('v')))


        if info.get('v_tp') in ['fixed','limit']:
            if tp in ['opaque']:
                if ispack:
                    fd.write(tab * 2 + 'self.opaque(x,{v_tp}={n})\n'.format(tp=tp,**info))
                else:
                    fd.write(tab * 2 + 'return self.opaque({v_tp}={n})\n'.format(tp=tp,**info))
            else:
                if ispack:
                    fd.write(tab * 2 + 'return self._array(x,self.{tp},{v_tp}={n})\n'.format(tp=tp,**info))
                else:
                    fd.write(tab * 2 + 'return self._array(self.{tp},{v_tp}={n})\n'.format(tp=tp,**info))
        fd.write('\n')

def write_struct(fd, xdr, ispack=True):
    for dat in xdr.get('struct'):
        fna = dat.get('k')
        if ispack:
            fd.write(tab+'def {fna}(self,pk):\n'.format(fna=fna))
        else:
            fd.write(tab + 'def {fna}(self):\n'.format(fna=fna))
            fd.write(tab*2 + 'pk = Pack(\'{fna}\')\n'.format(fna=fna))

        for c in dat.get('child'):
            packer_val(fd,c,dat,ispack=ispack)

        if ispack:
            pass
        else:
            fd.write(tab*2 +'return pk\n')

        fd.write('\n')

def write_opt_struct(fd,xdr,ispack=False):
    for dat in xdr.get('opt_struct'):
        fna = dat.get('k')
        d = dat.get('d')
        if ispack:
            fd.write(tab+'def {fna}(self,pk):\n'.format(fna=fna))
            fd.write(tab * 2 + 'self.{tp_d}(pk.{d})\n'.format(**dat))
        else:
            fd.write(tab + 'def {fna}(self):\n'.format(fna=fna))
            fd.write(tab*2 + 'pk = Pack(\'{fna}\')\n'.format(fna=fna))
            fd.write(tab * 2 + 'pk.{d} = self.{tp_d}()\n'.format(**dat))
        idx = 0
        default = None
        for c in dat.get('child'):
            if c.get('v') is None:
                default = c
                continue
            if c.get('ident').get('type') in ['void']:
                continue
            ls = []
            ls.append(convert_n(c.get('v')))
            for case in c.get('subcase'):
                ls.append(convert_n(case.get('v')))
            if not ls:
                continue

            enum = ','.join(ls)

            if idx ==0:
                fd.write(tab * 2 + 'if pk.{d} in [{enum}]:\n'.format(d=d,enum=enum,**c))
            else:
                fd.write(tab * 2 + 'elif pk.{d} in [{enum}]:\n'.format(d=d,enum=enum,**c))

            if ispack:
                fd.write(tab * 3 + 'self.{tp}(pk.{v})\n'.format(**c.get('ident')))
            else:
                fd.write(tab * 3 + 'pk.{v} = self.{tp}()\n'.format(**c.get('ident')))
            idx+=1
        if default:
            if default.get('ident').get('type') in ['void']:
                pass
                # fd.write(tab * 3 +'pass\n')
            else:
                fd.write(tab * 2 + 'else:\n'.format(d=d, enum=enum, **default))
                if ispack:
                    fd.write(tab * 3 + 'self.{tp}(pk.{v})\n'.format(**default.get('ident')))
                else:
                    fd.write(tab * 3 + 'pk.{v} = self.{tp}()\n'.format(**default.get('ident')))

        if ispack:
            pass
        else:
            fd.write(tab*2 +'return pk\n')

def write_stream(xdr,classname='NFS'):
    fd = open('packer.py', 'w')
    fd.write('from cgfsm.nfsv4.nfsstruct import const\n')
    fd.write('from cgfsm.nfsv4.nfsstruct.pack import Pack,Packer,UnPacker\n')
    fd.write('class {}Packer(Packer):\n'.format(classname))
    write_typedef(fd,xdr, ispack=True)
    write_struct(fd, xdr, ispack=True)
    write_opt_struct(fd,xdr,ispack=True)

    fd.write('class {}UnPacker(UnPacker):\n'.format(classname))
    write_typedef(fd, xdr, ispack=False)
    write_struct(fd, xdr, ispack=False)
    write_opt_struct(fd, xdr, ispack=False)

    fd.close()

if __name__=='__main__':
    fls = ['typedef','enum_define','struct_define','operation_define']
    s=''
    for f in fls:
        fd = open(f,'r')
        s += fd.read()
        fd.close()

    result = parse(s)
    convert(result)
    write_stream(result)

