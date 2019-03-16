#!/usr/bin/env python3

import subprocess
          
data = open('neh.txt', 'r') 
f = open("dummy.txt", 'w')
 
for line in data:                                
    if not line.strip():
        f.close()
        cutted_file = data.readline().rstrip() + ".txt"
        f = open(cutted_file, 'w')
    else:
        f.write(line)
subprocess.call("./removecolon.sh", shell=True)
