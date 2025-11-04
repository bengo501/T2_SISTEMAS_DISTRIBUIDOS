import time
import random
from utils import BallotNumber
from process import Process
from commander import Commander
from scout import Scout
from message import ProposeMessage,AdoptedMessage,PreemptedMessage

class Leader(Process):
    def __init__(self, env, id, config, use_backoff=True):
        Process.__init__(self, env, id)
        self.ballot_number = BallotNumber(0, self.id)
        self.active = False
        self.proposals = {}
        self.config = config
        self.use_backoff = use_backoff
        self.backoff_time = 0.1
        self.failed_attempts = 0
        self.env.addProc(self)

    def body(self):
        print("[leader %s] aqui estou" % self.id)
        Scout(self.env, "scout:%s:%s" % (str(self.id), str(self.ballot_number)),
              self.id, self.config.acceptors, self.ballot_number)
        while True:
            msg = self.getNextMessage()
            if isinstance(msg, ProposeMessage):
                if msg.slot_number not in self.proposals:
                    self.proposals[msg.slot_number] = msg.command
                    if self.active:
                        print("[leader %s] criando commander para slot %s com comando %s" % 
                              (self.id, msg.slot_number, msg.command))
                        Commander(self.env,
                                  "commander:%s:%s:%s" % (str(self.id),
                                                          str(self.ballot_number),
                                                          str(msg.slot_number)),
                                  self.id, self.config.acceptors, self.config.replicas,
                                  self.ballot_number, msg.slot_number, msg.command)

            elif isinstance(msg, AdoptedMessage):
                if self.ballot_number == msg.ballot_number:
                    pmax = {}
                    for pv in msg.accepted:
                        if pv.slot_number not in pmax or \
                              pmax[pv.slot_number] < pv.ballot_number:
                            pmax[pv.slot_number] = pv.ballot_number
                            self.proposals[pv.slot_number] = pv.command
                    for sn in self.proposals:
                        Commander(self.env,
                                  "commander:%s:%s:%s" % (str(self.id),
                                                          str(self.ballot_number),
                                                          str(sn)),
                                  self.id, self.config.acceptors, self.config.replicas,
                                  self.ballot_number, sn, self.proposals.get(sn))
                    self.active = True
                    self.failed_attempts = 0
                    self.backoff_time = 0.1
                    print("[leader %s] [OK] adotado para ballot %s, ativo" % (self.id, self.ballot_number))
            elif isinstance(msg, PreemptedMessage):
                if msg.ballot_number > self.ballot_number:
                    print("[leader %s] [PREEMPTED] preemptado por ballot %s (atual: %s)" % 
                          (self.id, msg.ballot_number, self.ballot_number))
                    self.ballot_number = BallotNumber(msg.ballot_number.round+1,
                                                      self.id)
                    self.active = False
                    
                    if self.use_backoff:
                        self.failed_attempts += 1
                        backoff = self.backoff_time * (2 ** self.failed_attempts)
                        backoff = min(backoff, 2.0)
                        print("[leader %s] aguardando backoff de %.2fs antes de tentar novamente..." % 
                              (self.id, backoff))
                        time.sleep(backoff)
                    else:
                        print("[leader %s] sem backoff - tentando novamente imediatamente..." % self.id)
                    
                    print("[leader %s] iniciando novo scout para ballot %s" % 
                          (self.id, self.ballot_number))
                    Scout(self.env, "scout:%s:%s" % (str(self.id),
                                                     str(self.ballot_number)),
                          self.id, self.config.acceptors, self.ballot_number)
                else:
                    print("[leader %s] preempted ignorado (ballot %s <= %s)" % 
                          (self.id, msg.ballot_number, self.ballot_number))
            else:
                print("[leader %s] tipo de mensagem desconhecida" % self.id)

