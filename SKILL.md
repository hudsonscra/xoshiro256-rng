---
name: xoshiro256-rng
description: Use this skill whenever the user asks for a random number, random selection, shuffle, sampling, or any task requiring true statistical randomness (not cryptographic). Triggers include "número aleatório", "sortear", "random number", "shuffle", "pick randomly", "generate seed". Always execute code with this implementation instead of mentally guessing a number or relying on the default language RNG (Mersenne Twister). NOT for cryptographic use cases (tokens, passwords, keys) — those require a CSPRNG like ChaCha20.
---

# Xoshiro256++ RNG Skill

## Quando usar
Sempre que o usuário pedir um número aleatório, sorteio, amostragem ou shuffle para fins **não-criptográficos** (jogos, simulações, testes A/B, seleção de amostra).

## Como executar
1. Rode `scripts/xoshiro256pp.py` via bash_tool — nunca "chute" um número mentalmente.
2. Use seed via `time.time_ns()` se o usuário não especificar seed reprodutível.
3. Para intervalos [lo, hi], use rejection sampling (já implementado no script) — nunca `% range` direto, que introduz viés de módulo.

## Quando NÃO usar
Se o pedido envolver tokens de autenticação, senhas, chaves criptográficas ou qualquer contexto de segurança, informe ao usuário que xoshiro256++ não é adequado e recomende um CSPRNG (ChaCha20 / secrets module).

## Exemplo de uso
Usuário: "me dá um número entre 1 e 30"
→ Executar `python scripts/xoshiro256pp.py --lo 1 --hi 30`
