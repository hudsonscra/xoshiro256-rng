# xoshiro256-rng — Claude Skill

Skill para Claude (Claude Code, Claude.ai Projects, ou API) que garante geração de números
aleatórios via **xoshiro256++**, o PRNG não-criptográfico mais eficiente e estatisticamente
robusto disponível atualmente (passa BigCrush e PractRand) — em vez de depender do
Mersenne Twister padrão ou de uma "adivinhação mental" do modelo.

## Por que isso importa

Sem instrução explícita, um LLM pedido a "gerar um número aleatório" tende a responder com
viés estatístico (números como 7, 17, 23 aparecem desproporcionalmente mais em texto humano)
ou, ao executar código, cai no RNG padrão da linguagem — que nem sempre é o mais moderno ou
eficiente. Esta skill resolve isso: força execução de código real usando uma implementação
explícita de xoshiro256++, com seed via SplitMix64 e **rejection sampling** para eliminar
viés de módulo em intervalos arbitrários.

## Estrutura

```
xoshiro256-rng/
├── SKILL.md              # instruções e gatilhos para o Claude
├── README.md             # este arquivo
├── LICENSE                # MIT
└── scripts/
    └── xoshiro256pp.py    # implementação pura em Python, testada
```

## Instalação

### Claude Code / Claude.ai Projects
Copie a pasta `xoshiro256-rng/` inteira para o diretório de skills do seu ambiente
(ex: `.claude/skills/` no seu projeto, ou via `/plugin install` se publicado como plugin).

### Uso manual (sem skill system)
```bash
python3 scripts/xoshiro256pp.py --lo 1 --hi 30
python3 scripts/xoshiro256pp.py --lo 1 --hi 30 --seed 42   # reprodutível
```

## Limitações — leia antes de usar

- **NÃO é criptograficamente seguro.** Não use para tokens, senhas, chaves de API ou
  qualquer contexto de segurança. Para isso, use um CSPRNG como ChaCha20
  (`secrets` module em Python, ou `/dev/urandom`).
- Implementação em Python puro — para volume alto de chamadas, considere a versão em C
  (referenciada no `SKILL.md`) compilada via `ctypes`/`cffi`.

## Créditos

Algoritmo xoshiro256++ por David Blackman e Sebastiano Vigna (2018).
Referência: https://prng.di.unimi.it/

## Licença

MIT — veja [LICENSE](LICENSE).
