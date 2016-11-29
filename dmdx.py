#!/usr/bin/env python3
import os
fdir = os.path.dirname(os.path.realpath(__file__))
os.chdir(fdir)
from site import addsitedir
addsitedir('src/')
from order_gen import assemble


# Get presentation frames
frames = assemble(frames=True,config='src/config.json')

# Process Frames
sessions = []
for f in frames:
    p_sess = []
    for i in f:
        p = ('-' if i[0] == 1 else '^', i.img, i.wrd)
        p_sess.append(p)
    sessions.append(p_sess)

dmdx_ln = '{0}{1} *<ms% 350> <bmp> "p{1}", <ms% 350> <bmp> "w{2}"/ <ms% 150> /;  '

dmdx_intersess = '0 <Line -2> "You have finished Block {0}. You may now take a short break.", <Line 1> "Press the SPACEBAR to begin the next block of pictures.";'

dmdx_end = '0 <Line -2> "You are now finished with this part of the experiment.", <Line 1> "The experimenter will now give you instructions for the second portion.";'

lines = []

for i,sess in enumerate(sessions):
    if i > 0:
        ln = dmdx_intersess.format(i)
        lines.append(ln)
    for frame in sess:
        ln = dmdx_ln.format(*frame)
        lines.append(ln)

lines.append(dmdx_end)

try:
    with open('src/nonce.txt','r',encoding='UTF-8') as fp:
        nonce = int(fp.read())
except: nonce = 0

with open('templates/dmdx_header.txt', 'r', encoding='UTF-8') as fp:
    dmdx_header = fp.read()

with open('output/dmdx_sess_{}.txt'.format(nonce), 'w', encoding='UTF-8') as fp:
    ln = lambda l: fp.write(l + '\n')
    ln(dmdx_header)
    for l in lines: ln(l)

with open('src/nonce.txt', 'w', encoding='UTF-8') as fp:
    fp.write(str(nonce + 1))

print('DMDX Session File Generated...')






