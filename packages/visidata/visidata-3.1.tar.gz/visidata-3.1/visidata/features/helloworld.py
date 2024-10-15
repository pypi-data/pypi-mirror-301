'''
Hello world minimal plugin.  Press F2 to show options.hello_world on the status line.

.visidatarc: `import plugins.hello`
'''
from visidata import vd, BaseSheet

vd.option('hello_world', '¡Hola mundo!', 'shown by the hello-world command')

BaseSheet.addCommand('KEY_F(2)', 'hello-world', 'status(options.hello_world)', 'print greeting to status')
