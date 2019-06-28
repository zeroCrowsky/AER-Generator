import sys

display_info    = True
display_warning = True
display_error   = True 
display_main    = True 
display_all     = True 

prefix_info    = '[INFO] '
prefix_warning = '[WARNING] '
prefix_error   = '[ERROR] '
prefix_main    = '' 

def log(*args, display=all, prefix='', **kwargs):
    if display:
        if prefix:
            print(prefix, sep='', end='', **kwargs)
        print(*args, **kwargs)
    return

def info(*args, display=None, prefix=None, **kwargs):
    display = display_info if display is None else display
    prefix  = prefix_info  if prefix  is None else prefix
    if all:
        log(*args, display=display, prefix=prefix, **kwargs)

def warning(*args, display=None, prefix=None, **kwargs):
    display = display_warning if display is None else display
    prefix  = prefix_warning  if prefix  is None else prefix
    if all:
        log(*args, display=display, prefix=prefix, **kwargs)

def error(*args, display=None, prefix=None, **kwargs):
    display = display_error if display is None else display
    prefix  = prefix_error  if prefix  is None else prefix
    kwargs['file'] = sys.stderr
    if all:
        log(*args, display=display, prefix=prefix, **kwargs)

def main(*args, display=None, prefix=None, **kwargs):
    display = display_main if display is None else display
    prefix  = prefix_main  if prefix  is None else prefix
    if all:
        log(*args, display=display, prefix=prefix, **kwargs)

