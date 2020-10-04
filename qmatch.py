#!/usr/bin/env python3

import sys
import string

def vlog(msg):
    sys.stderr.write('%s\n' % msg)

def ow(msg):
    sys.stdout.write('%s\n' % msg)
    
def qmatch(paragraph, lnb, lne):
    lines_desc = "Lines: [%d, %d]" % (lnb + 1, lne)
    qsingle = []
    for qc in ("`", "'"):
        b = 0
        while b >= 0:
            w = paragraph[b:].find(qc)
            if w >= 0:
                w += b
            cbefore = paragraph[w - 1] if w > 0 else ' '
            cafter = paragraph[w + 1] if w + 1 < len(paragraph) else ' '
            # vlog('%s, qc=%s, w=%d' % (lines_desc, qc, w))
            if ((w >= 0) and ((w == 0) or (paragraph[w - 1] != qc)) and
                ((w + 1 == len(paragraph) or (paragraph[w + 1] != qc))) and
                (cbefore not in string.ascii_letters or
                 cafter not in string.ascii_letters) and
                (not ((cbefore == 's') and (cafter == ' '))) and
                (cbefore != '``')
            ):
                qsingle.append((w, qc))
            b = (w + 1 if w >= 0 else -1)
            
    qsingle.sort()
    # vlog('qsingle: %s' % str(qsingle))
    level = 0
    for (pos, qc) in qsingle:
        level += (1 if qc == "`" else -1)
        if level < 0:
            ow('Qsingle error @ %s, pos=%d' % (lines_desc, pos))
    if level != 0:
        ow('Qsingle error @ %s, level=%d' % (lines_desc, level))
            
def qqmatch(paragraph, lnb, lne):
    lines_desc = "Lines: [%d, %d]" % (lnb + 1, lne)
    qqsingle = []
    for qc in ("``", "''"):
        b = 0
        while b >= 0:
            w = paragraph[b:].find(qc)
            # vlog('%s, w=%d' % (lines_desc, w))
            if w >= 0:
                w += b
            if ((w >= 0) and ((w == 0) or (paragraph[w - 1] != qc)) and
                ((w + 1 == len(paragraph) or (paragraph[w + 1] != qc)))):
                qqsingle.append((w, qc))
            b = (w + 2 if w >= 0 else -1)
            
    qqsingle.sort()
    level = 0
    for (pos, qc) in qqsingle:
        level += (1 if qc == "``" else -1)
        if level < 0:
            ow('Qdouble error @ %s, pos=%d' % (lines_desc, pos))
    if level != 0:
        ow('Qdouble error @ %s, level=%d' % (lines_desc, level))
            
def clean(fin):
    lines = fin.readlines()
    vlog('Input lines: %d' % len(lines))
    para = ''
    n_paragraphs = 0
    n_modified = 0
    nq_modified = 0
    nl = 0
    par_line_begin = 0
    for ln in range(len(lines)):
        line = lines[ln]
        if (line == '\n') and (len(para) > 0):
            n_paragraphs += 1
            qmatch(para, par_line_begin, ln)
            qqmatch(para, par_line_begin, ln)
            para = new_para = ''
            par_line_begin = ln + 1
        else:
            para += line
    vlog('%d paragraphs' % n_paragraphs)

if __name__ == '__main__':
    fn_in = sys.argv[1]
    fin = open(fn_in)
    clean(fin)
    fin.close()
    sys.exit(0)
