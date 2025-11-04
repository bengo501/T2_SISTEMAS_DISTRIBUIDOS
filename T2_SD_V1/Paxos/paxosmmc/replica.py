import json
import time
from pathlib import Path
from process import Process
from message import ProposeMessage,DecisionMessage,RequestMessage
from utils import *

class Replica(Process):
    def __init__(self, env, id, config, log_file=None):
        Process.__init__(self, env, id)
        self.slot_in = self.slot_out = 1
        self.proposals = {}
        self.decisions = {}
        self.requests = []
        self.config = config
        self.log_file = log_file
        self.env.addProc(self)
        
        if log_file and Path(log_file).exists():
            self._load_from_log()

    def _save_to_log(self, slot_number, command):
        if self.log_file:
            decision = {
                "slot_number": slot_number,
                "command": "%s:%d:%s" % (command.client, command.req_id, command.op),
                "timestamp": time.time()
            }
            try:
                with open(self.log_file, 'a') as f:
                    f.write(json.dumps(decision) + "\n")
            except Exception as e:
                print(f"[replica {self.id}] erro ao salvar log: {e}")

    def _load_from_log(self):
        try:
            with open(self.log_file, 'r') as f:
                for line in f:
                    try:
                        decision = json.loads(line.strip())
                        slot = decision["slot_number"]
                        cmd_str = decision.get("command", "")
                        parts = cmd_str.split(":")
                        if len(parts) >= 3:
                            cmd = Command(parts[0], int(parts[1]), parts[2])
                        else:
                            cmd = Command(cmd_str, 0, cmd_str)
                        self.decisions[slot] = cmd
                        if slot >= self.slot_out:
                            self.slot_out = slot + 1
                    except Exception as e:
                        continue
            print(f"[replica {self.id}] recuperou {len(self.decisions)} decisões do log, slot_out={self.slot_out}")
        except Exception as e:
            print(f"[replica {self.id}] erro ao carregar log: {e}")

    def propose(self):
        while len(self.requests) != 0 and self.slot_in < self.slot_out+WINDOW:
            if self.slot_in > WINDOW and self.slot_in-WINDOW in self.decisions:
                if isinstance(self.decisions[self.slot_in-WINDOW],ReconfigCommand):
                    r,a,l = self.decisions[self.slot_in-WINDOW].config.split(';')
                    self.config = Config(r.split(','),a.split(','),l.split(','))
                    print("[replica %s] nova config: %s" % (self.id, self.config))
            if self.slot_in not in self.decisions:
                cmd = self.requests.pop(0)
                self.proposals[self.slot_in] = cmd
                for ldr in self.config.leaders:
                    self.sendMessage(ldr, ProposeMessage(self.id,self.slot_in,cmd))
            self.slot_in +=1

    def perform(self, cmd):
        for s in range(1, self.slot_out):
            if self.decisions[s] == cmd:
                self.slot_out += 1
                return
        if isinstance(cmd, ReconfigCommand):
            self.slot_out += 1
            return
        print("[replica %s] perform %s : %s" % (self.id, self.slot_out, cmd))
        self._save_to_log(self.slot_out, cmd)
        self.slot_out += 1

    def body(self):
        print("[replica %s] aqui estou" % self.id)
        while True:
            msg = self.getNextMessage()
            if isinstance(msg, RequestMessage):
                self.requests.append(msg.command)
            elif isinstance(msg, DecisionMessage):
                self.decisions[msg.slot_number] = msg.command
                while self.slot_out in self.decisions:
                    if self.slot_out in self.proposals:
                        if self.proposals[self.slot_out]!=self.decisions[self.slot_out]:
                            self.requests.append(self.proposals[self.slot_out])
                        del self.proposals[self.slot_out]
                    self.perform(self.decisions[self.slot_out])
            else:
                print("[replica %s] tipo de mensagem desconhecida" % self.id)
            self.propose()

