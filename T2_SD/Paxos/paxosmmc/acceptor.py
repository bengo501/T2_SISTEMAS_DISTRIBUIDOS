import json
import time
from pathlib import Path
from utils import PValue
from process import Process
from message import P1aMessage, P1bMessage, P2aMessage, P2bMessage

class Acceptor(Process):
    def __init__(self, env, id, log_file=None):
        Process.__init__(self, env, id)
        self.ballot_number = None
        self.accepted = set()
        self.log_file = log_file
        self.env.addProc(self)
        
        if log_file and Path(log_file).exists():
            self._load_from_log()

    def _save_to_log(self, pvalue):
        if self.log_file:
            decision = {
                "ballot_round": pvalue.ballot_number.round,
                "ballot_leader": str(pvalue.ballot_number.leader_id),
                "slot_number": pvalue.slot_number,
                "command": "%s:%d:%s" % (pvalue.command.client, pvalue.command.req_id, pvalue.command.op),
                "timestamp": time.time()
            }
            try:
                with open(self.log_file, 'a') as f:
                    f.write(json.dumps(decision) + "\n")
            except Exception as e:
                print(f"[acceptor {self.id}] erro ao salvar log: {e}")

    def _load_from_log(self):
        try:
            with open(self.log_file, 'r') as f:
                for line in f:
                    try:
                        decision = json.loads(line.strip())
                        from utils import BallotNumber
                        ballot_round = decision.get("ballot_round", 0)
                        ballot_leader = decision.get("ballot_leader", "")
                        ballot = BallotNumber(ballot_round, ballot_leader)
                        cmd_str = decision.get("command", "")
                        slot = decision.get("slot_number", 0)
                        from utils import Command
                        cmd = Command(cmd_str.split(":")[0] if ":" in cmd_str else cmd_str, 
                                     int(cmd_str.split(":")[1]) if ":" in cmd_str and len(cmd_str.split(":")) > 1 else 0,
                                     cmd_str.split(":")[2] if ":" in cmd_str and len(cmd_str.split(":")) > 2 else cmd_str)
                        pvalue = PValue(ballot, slot, cmd)
                        self.accepted.add(pvalue)
                    except Exception as e:
                        continue
            print(f"[acceptor {self.id}] recuperou {len(self.accepted)} decisões do log")
        except Exception as e:
            print(f"[acceptor {self.id}] erro ao carregar log: {e}")

    def body(self):
        print("[acceptor %s] aqui estou" % self.id)
        while True:
            msg = self.getNextMessage()
            if isinstance(msg, P1aMessage):
                if self.ballot_number is None or msg.ballot_number > self.ballot_number:
                    self.ballot_number = msg.ballot_number
                    print("[acceptor %s] promete para ballot %s" % (self.id, msg.ballot_number))
                self.sendMessage(msg.src,
                                 P1bMessage(self.id,
                                            self.ballot_number,
                                            self.accepted))
            elif isinstance(msg, P2aMessage):
                if self.ballot_number == msg.ballot_number:
                    pvalue = PValue(msg.ballot_number,
                                    msg.slot_number,
                                    msg.command)
                    self.accepted.add(pvalue)
                    self._save_to_log(pvalue)
                    print("[acceptor %s] aceita pvalue %s" % (self.id, pvalue))
                self.sendMessage(msg.src,
                                 P2bMessage(self.id,
                                            self.ballot_number,
                                            msg.slot_number))

