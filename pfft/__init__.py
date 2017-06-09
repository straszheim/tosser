import sys, pkgutil, subprocess, os, os.path, inspect, collections
from pfft.serv import *

from blessings import Terminal
term = Terminal('ansi')

Compiler = collections.namedtuple('Compiler', ['exe', 'includes', 'cppflags',
                                               'ldflags', 'ldflags_shared'])

clang38 = Compiler(exe='clang-3.8',
                   includes=['/usr/include/python3.5',
                             'pybind11/include'],
                   cppflags=['-std=c++14', '-fPIC'],
                   ldflags=['-lstdc++'],
                   ldflags_shared=['-shared'])

ctx = collections.ChainMap(dict(compiler=clang38))

def subexec(tag, args):
    print("%-10s %s" % (tag, ' '.join(args)),)
    cproc = subprocess.run(args)
    if cproc.returncode > 0:
        print("ERROR")
        print(cproc)
        exit(1)

def opt_mtime(fname):
    try:
        modtime = os.stat(fname).st_mtime
    except:
        modtime = -1.0
    return modtime

def buildstep(inputs, outputs, fn):
    maxin = max([opt_mtime(i) for i in inputs])
    minout = min([opt_mtime(o) for o in outputs])
    if maxin > minout or maxin == -1.0:
        print("{t.yellow} {outputs} {t.green} {inputs} {t.normal}".format(t=term, outputs=outputs, inputs=inputs))
        fn()
    else:
        print("outputs: {t.green} {outputs} {t.normal}".format(t=term, outputs=outputs))

def compile(src, trg, ctx=ctx):
    args = [ctx['compiler'].exe] + ['-I%s' % k for k in ctx['compiler'].includes] + ctx['compiler'].cppflags + ['-c', src, '-o', trg]
    subexec("compile", args)

def link(src, trg, ctx=ctx):
    args = [ctx['compiler'].exe] + src + ['-o', trg] + ctx['compiler'].ldflags
    subexec("link", args)

def link_shared(src, trg, ctx=ctx):
    args = [ctx['compiler'].exe] + src + ['-o', trg] + ctx['compiler'].ldflags + ctx['compiler'].ldflags_shared
    subexec("link_so", args)

def cpp_obj(src, trg, ctx=ctx):
    buildstep([src], [trg], lambda: compile(src, trg, ctx=ctx))

def cpp_exe(objs, trg, ctx=ctx):
    buildstep(objs, [trg], lambda: link(objs, trg, ctx=ctx))

def cpp_so(objs, trg, ctx=ctx):
    buildstep(objs, [trg], lambda: link_shared(objs, trg, ctx=ctx))


thisdir = os.path.dirname(sys.modules[__name__].__file__)
bindings_stems = ['bindings']
bindings_objs = [thisdir + '/' + stem + ".o" for stem in bindings_stems]

[cpp_obj(thisdir + '/' + stem + ".cpp",
         thisdir + '/' + stem + ".o",
         ctx=ctx) for stem in bindings_stems]

cpp_so(bindings_objs, "bindings.so", ctx=ctx)

from bindings import *

print("calling pfft built pybindings: {}".format(funcy()))
