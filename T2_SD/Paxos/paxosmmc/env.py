import os
import signal
import sys
import time
from pathlib import Path
from acceptor import Acceptor
from leader import Leader
from message import RequestMessage
from process import Process
from replica import Replica
from utils import *

NACCEPTORS = 3
NREPLICAS = 2
NLEADERS = 2
NREQUESTS = 10
NCONFIGS = 2

class Env:
    def __init__(self, log_dir="logs"):
        self.procs = {}
        self.log_dir = log_dir
        Path(log_dir).mkdir(exist_ok=True)

    def sendMessage(self, dst, msg):
        if dst in self.procs:
            self.procs[dst].deliver(msg)

    def addProc(self, proc):
        self.procs[proc.id] = proc
        proc.start()

    def removeProc(self, pid):
        if pid in self.procs:
            del self.procs[pid]

    def run(self):
        initialconfig = Config([], [], [])
        c = 0

        for i in range(NREPLICAS):
            pid = "replica: %d" % i
            log_file = f"{self.log_dir}/replica_{i}.log"
            Replica(self, pid, initialconfig, log_file=log_file)
            initialconfig.replicas.append(pid)
        for i in range(NACCEPTORS):
            pid = "acceptor: %d.%d" % (c,i)
            log_file = f"{self.log_dir}/acceptor_{c}_{i}.log"
            Acceptor(self, pid, log_file=log_file)
            initialconfig.acceptors.append(pid)
        for i in range(NLEADERS):
            pid = "leader: %d.%d" % (c,i)
            Leader(self, pid, initialconfig, use_backoff=True)
            initialconfig.leaders.append(pid)
        
        time.sleep(1)
        
        for r in initialconfig.replicas:
            pid = "master: %d.%d" % (c,0)
            cmd = Command(pid,0,"operation %d.%d" % (c,0))
            self.sendMessage(r, RequestMessage(pid, cmd))
            time.sleep(1)

        for c in range(1, NCONFIGS):
            config = Config(initialconfig.replicas, [], [])
            for i in range(NACCEPTORS):
                pid = "acceptor: %d.%d" % (c,i)
                log_file = f"{self.log_dir}/acceptor_{c}_{i}.log"
                Acceptor(self, pid, log_file=log_file)
                config.acceptors.append(pid)
            for i in range(NLEADERS):
                pid = "leader: %d.%d" % (c,i)
                Leader(self, pid, config, use_backoff=True)
                config.leaders.append(pid)
            
            for r in config.replicas:
                pid = "master: %d.%d" % (c,0)
                cmd = ReconfigCommand(pid,0,str(config))
                self.sendMessage(r, RequestMessage(pid, cmd))
                time.sleep(1)
            
            for i in range(WINDOW-1):
                pid = "master: %d.%d" % (c,i)
                for r in config.replicas:
                    cmd = Command(pid,0,"operation noop")
                    self.sendMessage(r, RequestMessage(pid, cmd))
                    time.sleep(1)
            
            for i in range(NREQUESTS):
                pid = "client: %d.%d" % (c,i)
                for r in config.replicas:
                    cmd = Command(pid,0,"operation %d.%d" % (c,i))
                    self.sendMessage(r, RequestMessage(pid, cmd))
                    time.sleep(1)

    def terminate_handler(self, signal, frame):
        self._graceexit()

    def _graceexit(self, exitcode=0):
        sys.stdout.flush()
        sys.stderr.flush()
        os._exit(exitcode)

def main():
    e = Env()
    e.run()
    signal.signal(signal.SIGINT, e.terminate_handler)
    signal.signal(signal.SIGTERM, e.terminate_handler)
    signal.pause()

if __name__=='__main__':
    main()

