#!/usr/bin/env python3
from collections import namedtuple
import random
import json


def mkindex(ta_count,na_count,buff=2,head=2,tail=2,**kwargs):
    # Generate an ordering map of ta and na instances
    # Let 1 represent ta instances & 0 represent na instance
    ta = [1 for i in range(ta_count)]  # Generate ta markers
    na = [0 for i in range(na_count)]  # Gereate na markers
    head = [na.pop() for i in range(head)]  # Sequester head markers
    tail = [na.pop() for i in range(tail)]  # Sequester tail markers
    order = ta + na  # Join body components
    random.shuffle(order)  # Shuffle body order
    index = [order.pop(0)]  # Initialize body index
    while len(order) > 0:  # Construct body
        i =  order.pop(0)  # Pop off a marker
        w = min(len(index),buff)  # Choose optimal range for search
        if not 1 in index[-w:] or i == 0:  # Do if i is na or if no ta in seach
            index.append(i)  # Add selected marker to index
        elif len(index) > buff * 2:  # Check if internal search viable
            w = random.randrange(len(index) - buff) + buff  # Internal search var
            if not i in index[w-buff:w+buff-1]:  # Check if i in internal search
                index.insert(w,i)  # Insert i at search index
            else: order.append(i)  # Else re-add i to order
        else: order.append(i)  # Else re-add i to order
    return head + index + tail  # Concatenate head, body, & tail


def mkorder(ta,na,index,phase=1,prefix=False):
    if prefix:
        for i in range(phase - 1): index.append(index.pop(0))
    if phase > 1:  # Remove excess na indexes
        ie = []
        for i in [x[0] for x in enumerate(index) if x[1] == 1]:
            for r in range(phase - 1):
                ie.append(i + r + 1)
        index = [x[1] for x in enumerate(index) if x[0] not in ie]
    i = index.pop(0)
    order = [na.pop(0) if i == 0 else ta.pop(0)]
    while len(index) > 0:
        i = index.pop(0)
        ins = na.pop(0) if i == 0 else ta.pop(0)
        if not order[-1][1] == ins[1]:
            order.append(ins)
        elif len(order) > 3:
            r = random.randrange(1,len(order)-1)
            if order[r][0] == i:
                if not order[r-1][1] == ins[1] and not order[r+1][1] == ins[1]:
                    if i == 0: na.append(order[r])
                    else: ta.append(order[r])
                    index.insert(0,i)
                    order[r] = ins
                else:
                    index.insert(0,i)
                    if i==0: na.append(ins)
                    else: ta.append(ins)
            else:
                index.insert(0,i)
                if i==0: na.append(ins)
                else: ta.append(ins)
        else:
            index.insert(0,i)
            if i==0: na.append(ins)
            else: ta.append(ins)
    return order


def mkcase(ta,na,index,bank=[0,100],phase=1,strict=False,prefix=False):
    # Kwargs: bank, prefix, ta/ta rep, & na/ta strict.
    phases = [x for x in range(phase)]
    rp = lambda: random.randrange(phase)
    pl = (bank[1]-bank[0])//phase # Phased Bank Length
    bank = [x + bank[0] for x in range(pl)]
    random.shuffle(bank)
    if strict:
        ta_vals = [(1,bank.pop()) for x in range(ta * len(index))]
    else: ta_vals = [(1,bank[x]) for x in range(ta * len(index))]
    na_vals = [(0,x) for x in bank] * phase
    orders = []
    for i in index:
        ta_stack = [ta_vals.pop() for x in range(ta)]
        random.shuffle(na_vals)
        na_stack = [na_vals[x] for x in range(na)]
        order = []
        for o in mkorder(ta_stack,na_stack,i,phase=phase,prefix=prefix):
            if o[0] == 0:
                order.append((0,o[1] + (pl * rp())))
            else:
                random.shuffle(phases)
                order += [(1,o[1] + (pl * x)) for x in phases]
        orders.append(order)
    return orders

# Assembles stimulus cases
# Produces a dictionary of orders for all cases

def assemble_cases(ta,na,index,**kwargs):
    if not 'cases' in kwargs:
        raise Exception('Must define 1 or more cases')
    cases = {}
    for c in kwargs['cases']:
        i = [[y for y in x] for x in index]
        cases[c] = mkcase(ta,na,i,**kwargs['cases'][c])
    return cases


# Produces a list of indexes determining ta and na placement
def assemble_indexes(ta,na,**kwargs):
    index = []
    for i in range(kwargs['sess']):
        index.append(mkindex(ta,na,
        **kwargs))
    return index


def assemble(frames=False,config='config.json'):
    with open(config) as conf:
        kwargs = json.load(conf)
    index = assemble_indexes(**kwargs)
    cases = assemble_cases(**kwargs,index=index)
    if frames:
        return mk_frames(index,cases)
    return {'index':index, **cases}


def mk_frames(index,cases):
    ck = [k for k in cases]
    t = namedtuple('frame',['index'] + ck)
    r = []
    for i in enumerate(index):
        ir = []
        for e in enumerate(i[1]):
            er = [e[1]]
            for k in ck:
                er.append(cases[k][i[0]][e[0]][1])
            ir.append(t(*er))
        r.append(ir)
    return r

