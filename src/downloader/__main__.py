import subprocess
import random
import string
import fcntl
import os

def randomString():
    letters = [random.choice(string.ascii_letters) for i in range(32)]
    return ''.join(letters)

class ShellProc:
    def __init__(self, args=["bash"]):
        self.proc = None
        self.args = args
        self.connected = False
    
    def connect(self):
        self.proc = subprocess.Popen(
            self.args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=0)
        
        self.connected = True
        self.exec('echo')
    
    def exec(self, command):
        if not self.connected:
            self.connect()

        tail = randomString()
        self.proc.stdin.write(f'({command}); echo {tail}\n'.encode('utf8'))
        resultLines = []
        while line := self.proc.stdout.readline():
            if line.endswith(f'{tail}\n'.encode('utf8')):
                line = line[:-len(tail)-1]
                resultLines.append(line)
                break
            else:
                resultLines.append(line)
        
        return b''.join(resultLines).decode('utf8')
    
    def close(self):
        self.proc.stdin.close()
        self.proc.kill()


if __name__ == '__main__':
    daemonShell = ShellProc()
    daemonShell.exec("ipfs daemon")


