# Raft Distribuído - Instruções

## Resposta: É possível tornar o Raft verdadeiramente distribuído?

**SIM, é totalmente possível!** A implementação atual (`raft_distribuido.py`) permite executar nós Raft em máquinas diferentes, comunicando-se via HTTP.

## Implementação

O arquivo `raft_distribuido.py` implementa uma versão distribuída do Raft onde:
- Cada nó executa um servidor HTTP
- Comunicação entre nós via HTTP/REST API
- Nós podem estar em máquinas/hosts diferentes
- Protocolo Raft mantido (eleição, heartbeats, votação)

## Como Executar Distribuído

### Opção 1: Máquinas Diferentes (Verdadeiramente Distribuído)

Em cada máquina, execute:

**Máquina 1:**
```bash
python raft_distribuido.py --id 0 --host 192.168.1.10 --port 8000 \
  --peers http://192.168.1.11:8001 http://192.168.1.12:8002
```

**Máquina 2:**
```bash
python raft_distribuido.py --id 1 --host 192.168.1.11 --port 8001 \
  --peers http://192.168.1.10:8000 http://192.168.1.12:8002
```

**Máquina 3:**
```bash
python raft_distribuido.py --id 2 --host 192.168.1.12 --port 8002 \
  --peers http://192.168.1.10:8000 http://192.168.1.11:8001
```

Substitua os IPs pelos IPs reais das máquinas no laboratório.

### Opção 2: Terminais Diferentes na Mesma Máquina (Simulação Local)

Para testar localmente, abra 3 terminais e execute em cada um:

**Terminal 1:**
```bash
cd T2_SD_V1/Raft
python raft_distribuido.py --id 0 --host localhost --port 8000 \
  --peers http://localhost:8001 http://localhost:8002
```

**Terminal 2:**
```bash
cd T2_SD_V1/Raft
python raft_distribuido.py --id 1 --host localhost --port 8001 \
  --peers http://localhost:8000 http://localhost:8002
```

**Terminal 3:**
```bash
cd T2_SD_V1/Raft
python raft_distribuido.py --id 2 --host localhost --port 8002 \
  --peers http://localhost:8000 http://localhost:8001
```

### Opção 3: Script Automático (Local)

Para teste rápido local:
```bash
cd T2_SD_V1/Raft
python iniciar_raft_distribuido.py
```

Este script inicia os 3 nós automaticamente em processos separados.

## Diferenças entre Versões

### raft_example.py (Didático)
- ✅ Simulação local em uma única máquina
- ✅ Comunicação via chamadas de método Python
- ✅ Útil para entender o algoritmo
- ✅ Mais simples para testes

### raft_distribuido.py (Distribuído)
- ✅ Execução em múltiplas máquinas/hosts
- ✅ Comunicação via HTTP/REST API
- ✅ Verdadeiramente distribuído
- ✅ Adequado para laboratório distribuído

## Requisitos

- Python 3.9+
- Bibliotecas padrão apenas (sem dependências externas)
- Conexão de rede entre as máquinas (para execução distribuída)

## Verificação de Status

Você pode verificar o status de qualquer nó fazendo uma requisição HTTP:

```bash
curl http://localhost:8000/status
```

Retorna JSON com:
```json
{
  "id": 0,
  "state": "Leader",
  "term": 1,
  "voted_for": 0
}
```

## Observações

- A implementação usa HTTP simples para comunicação
- Em produção, seria recomendado usar gRPC ou protocolo binário mais eficiente
- Para testes reais distribuídos, configure firewall/portas adequadamente
- Cada nó precisa conhecer os URLs de todos os outros peers

## Conclusão

A implementação distribuída está pronta e funcional. Para usar no laboratório:

1. Configure os IPs/hosts das máquinas
2. Execute um nó por máquina
3. Configure os peers com os URLs corretos
4. O cluster irá eleger um líder e manter consenso distribuído

