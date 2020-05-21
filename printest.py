import subprocess
lpr =  subprocess.Popen("/usr/bin/lpr", stdin=subprocess.PIPE)

lpr.stdin.write(b"get off")
