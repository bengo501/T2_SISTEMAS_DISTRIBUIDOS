# Como Compilar e Executar

## Problema de Múltiplos Main

O projeto tem dois executáveis diferentes:
- `main.go` - Para iniciar um nó Raft
- `benchmark_main.go` - Para executar o benchmark

Para resolver isso, usamos **build tags** do Go.

## Compilar e Executar

### 1. Compilar e executar nó Raft (padrão)

```bash
go run main.go --id 1 --port 8000
```

Ou compilar:

```bash
go build -o raft-node main.go
./raft-node --id 1 --port 8000
```

### 2. Compilar e executar benchmark

```bash
go run -tags benchmark benchmark_main.go --duracao 180 --cargas 1,2,3,4
```

Ou compilar:

```bash
go build -tags benchmark -o benchmark benchmark_main.go
./benchmark --duracao 180 --cargas 1,2,3,4
```

## Build Tags

- `main.go` usa `//go:build !benchmark` - compila quando a tag `benchmark` NÃO está presente
- `benchmark_main.go` usa `//go:build benchmark` - compila quando a tag `benchmark` está presente

## Exemplos

### Iniciar cluster (3 nós)

Terminal 1:
```bash
go run main.go --id 1 --port 8000
```

Terminal 2:
```bash
go run main.go --id 2 --port 8001
```

Terminal 3:
```bash
go run main.go --id 3 --port 8002
```

### Executar benchmark

```bash
go run -tags benchmark benchmark_main.go --duracao 180 --cargas 1,2,3,4,6,8,10,12
```

