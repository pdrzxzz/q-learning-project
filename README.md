# Q-Learning Platform Navigation

Um projeto de aprendizado por reforço que implementa o algoritmo Q-Learning para treinar um agente a navegar em um ambiente de plataformas.

## 📋 Visão Geral

Este projeto utiliza Q-Learning para treinar um agente que navega entre plataformas em um ambiente 2D. O agente aprende a tomar decisões ótimas (pular, mover para esquerda ou direita) baseado em seu estado atual e nas recompensas recebidas.

## 🎯 Funcionalidades

- **Algoritmo Q-Learning**: Implementação completa com parâmetros configuráveis
- **Ambiente de Plataformas**: 24 plataformas com 4 direções possíveis (96 estados totais)
- **Três Ações**: `left`, `right`, `jump`
- **Estratégia Epsilon-Greedy**: Balanceamento entre exploração e explotação
- **Persistência**: Salvamento automático da Q-table durante o treinamento

## 🏗️ Estrutura do Projeto

```
Qlearning/
├── __pycache__/            # Cache do Python
├── executables/            # Executáveis do ambiente
├── scripts/
│   ├── client.py           # Script principal do agente Q-Learning
│   └── connection.py       # Módulo de conexão TCP com o servidor
├── data/
│   ├── initial_q_table.txt # Q-table inicial (zeros)
│   └── new_q_table.txt     # Q-table atualizada após treinamento
├── LICENSE                 # Licença MIT
├── README.md              # Este arquivo
└── specifications.pdf     # Especificações do projeto
```

## ⚙️ Parâmetros de Configuração

| Parâmetro | Valor | Descrição |
|-----------|-------|-----------|
| `LEARNING_RATE` | 0.5 | Taxa de aprendizado (α) |
| `DISCOUNT_FACTOR` | 0.5 | Fator de desconto (γ) |
| `EPSILON` | 0.3 | Taxa de exploração (ε) |
| `num_actions` | 100000 | Número de ações de treinamento |

## 🚀 Como Usar

### Pré-requisitos

- Python 3.x
- NumPy
- Servidor do ambiente de plataformas rodando na porta 2037

### Instalação

1. Clone o repositório:
```bash
git clone [url-do-repositorio]
cd Qlearning
```

2. Instale as dependências:
```bash
pip install numpy
```

### Execução

1. Certifique-se de que o servidor do ambiente está rodando na porta 2037
2. Execute o cliente Q-Learning:
```bash
python scripts/client.py
```

O agente começará a treinar automaticamente, salvando a Q-table a cada ação em `data/new_q_table.txt`.

## 🧠 Como Funciona

### Representação do Estado

O estado é representado por um número binário de 7 bits:
- **Bits 6-5**: Direção (00=Norte, 01=Leste, 10=Sul, 11=Oeste)
- **Bits 4-0**: ID da plataforma (0-23)

### Algoritmo Q-Learning

O agente utiliza a equação de Bellman para atualizar os valores Q:

```
Q(s,a) = Q(s,a) + α * (r + γ * max(Q(s',a')) - Q(s,a))
```

Onde:
- `s`: estado atual
- `a`: ação tomada
- `r`: recompensa recebida
- `s'`: próximo estado
- `α`: taxa de aprendizado
- `γ`: fator de desconto

### Estratégia de Seleção de Ação

- **Exploração** (30%): Ação aleatória
- **Explotação** (70%): Melhor ação conhecida (maior valor Q)

## 📊 Estrutura da Q-Table

- **Dimensões**: 96 x 3 (96 estados × 3 ações)
- **96 Estados**: 24 plataformas × 4 direções
- **3 Ações**: left, right, jump

## 🔧 Personalização

Para ajustar o comportamento do agente, modifique os parâmetros no início de `client.py`:

```python
LEARNING_RATE = 0.5        # Velocidade de aprendizado
DISCOUNT_FACTOR = 0.5     # Importância de recompensas futuras
EPSILON = 0.3               # Taxa de exploração
num_actions = 100000       # Número de ações de treinamento
```

## 📈 Monitoramento

O script exibe informações em tempo real:
- Estado atual e recompensa
- Ação selecionada (aleatória ou ótima)
- Direção do agente
- Progresso do treinamento

## 👨‍💻 Autores

- Aline Acioly  
- Emanuel Pedroza  
- Julio Sobral

