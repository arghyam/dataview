import imp
import os
import sys
import inspect
import plugins

def list_of_files(folder):
    files = []
    for dirname, dirnames, filenames in os.walk(folder):
        # print path to all filenames.
        for filename in filenames:
            files.append(os.path.join(dirname, filename))

    return files


def list_plugins(folder):
    files = []
    for filenames in os.walk(folder):
        # print path to all filenames.
        for filename in filenames:           
            for f in filename:
                if str(f) in ['__init__.py','template_plugin.py']:
                    pass                
                elif str(f).endswith(".py"):
                    f = f[:-3]
                    print str(f)
                    files.append(f)
    return files



def load_from_file(filepath):
    mod_name,file_ext = os.path.splitext(os.path.split(filepath)[-1])

    if file_ext.lower() == '.py':
        py_mod = imp.load_source(mod_name, filepath)

    elif file_ext.lower() == '.pyc':
        py_mod = imp.load_compiled(mod_name, filepath)

def getClassNameFromFileName(file_name):
    names = file_name.split("_")
    className = ""
    for name in names:
        className = className + name.title()
    return className



def get_class( kls ):
    parts = kls.split('.')
    module = ".".join(parts[:-1])
    m = __import__( module )
    for comp in parts[1:]:
        m = getattr(m, comp)            
    return m