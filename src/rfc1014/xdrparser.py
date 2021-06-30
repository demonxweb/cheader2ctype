import re
pats = {
'end' : re.compile(r'^}\s*(?P<v>[a-zA-Z0-9_*<>\[\]]+)?\s*;'),
'enum' : re.compile(r'^enum\s+(?P<k>[a-zA-Z0-9_]+)\s*{'),
'enum_val' : re.compile(r'^(?P<k>[a-zA-Z0-9_]+)\s*=\s*(?P<v>[a-zA-Z0-9_]+)[,]?'),

'const' : re.compile(r'^const\s+(?P<k>[a-zA-Z0-9_]+)\s*=\s*(?P<v>[a-zA-Z0-9_]+)\s*;'),
'struct' : re.compile(r'^struct\s+(?P<k>[a-zA-Z0-9_]+)\s*{'),

'opt_struct' : re.compile(r'^union\s+(?P<k>[a-zA-Z0-9_]+)\s+switch\s+\((?P<tp_d>[a-zA-Z0-9_]+)\s+(?P<d>[a-zA-Z0-9_]+)\)\s*{'),
'case' : re.compile(r'^(case\s+(?P<v>[a-zA-Z0-9_]+)|default)\s*:'),
'void' : re.compile(r'^(?P<v>void)\s*;'),
'val' : re.compile(r'^(?P<tp>[a-zA-Z0-9_]+)\s+(?P<v>[a-zA-Z0-9_*<>\[\]]+)\s*;'),

'typedef' : re.compile(r'^typedef\s+(?P<tp_d>[a-zA-Z0-9_]+)\s+(?P<v>[a-zA-Z0-9_*<>\[\]]+)\s*;'),
'enumdef' : re.compile(r'^(?P<tp_d>enum)\s+(?P<v>[a-zA-Z0-9_*<>\[\]]+)\s*;'),
'comment': re.compile(r'^(?P<c>#.*)\n')
}
def search(tp,s):
    s = s.strip()
    m = re.search(pats.get(tp), s)
    if not m:
        return s,None
    pos = m.span()[-1]
    s = s[pos:].strip()
    dat = {}
    dat.update(m.groupdict())
    dat['type'] = tp
    return s,dat

def parse_enum(s):
    s,enum = search('enum',s)
    if not enum:
        return s,None
    enum['child'] = []
    while True:
        s,end = search('end',s)
        if end:
            break
        s,val = search('enum_val',s)
        if not val:
            raise Exception('Struct Error:{}'.format(s[:100]))
        enum['child'].append(val)

    return s,enum

def parse_struct(s):
    s,struct = search('struct',s)
    if not struct:
        return s,None
    struct['child'] = []
    while True:
        s,end = search('end',s)
        if end:
            break
        s,val = search('val',s)
        if not val:
            raise Exception('Struct Error:{}'.format(s[:100]))
        struct['child'].append(val)

    return s,struct

def parse_opt_struct(s):
    s,struct = search('opt_struct',s)
    if not struct:
        return s,None
    struct['child'] = []
    while True:
        s,end = search('end',s)
        if end:
            break
        s,case = parse_case(s)
        if not case:
            raise Exception('Case Error: {}'.format(s[:100]))
        struct['child'].append(case)


    return s,struct

def parse_case(s):
    s,case = search('case',s)

    if not case:
        return s,None
    case['subcase'] = []
    while True:
        s, scase = search('case', s)
        if not scase:
            break
        case['subcase'].append(scase)


    s,val = search('void',s)
    if val:
        case['ident'] = val
        return s,case
    s,val = search('val',s)
    if val:
        case['ident'] = val
        return s,case

    return s,case

def parse(s):
    result = {'struct':[],'opt_struct':[],'const':[],'enum':[],'typedef':[]}
    while True:
        s, struct = parse_struct(s)
        if struct:
            result['struct'].append(struct)
            continue

        s, opt_struct = parse_opt_struct(s)
        if opt_struct:
            result['opt_struct'].append(opt_struct)
            continue

        s,enum = parse_enum(s)
        if enum:
            result['enum'].append(enum)
            continue

        s,typedef = search('typedef',s)
        if typedef:
            result['typedef'].append(typedef)
            continue
        s, typedef = search('enumdef', s)
        if typedef:
            result['typedef'].append(typedef)
            continue

        s,const = search('const',s)
        if const:
            result['const'].append(const)
            continue
        s,comment = search('comment',s)
        if comment:
            continue
        comment
        if s:
            raise Exception('Parse Error: {}'.format(s[:100]))
        break

    return result


