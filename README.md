# 六親合体ゴッドにゃ〜ず / ROKUSHIN GATTAI GOD NYĀZU

> **0Bモデルを、合体させて使う。**  
> **Compose 0B models into one working system.**

[日本語](#日本語) · [English](#english)

---

## 日本語

### これは何？

**六親合体ゴッドにゃ〜ず**は、0Bモデルを含む異なる能力を組み合わせ、全体として仕事を成立させるための実験的ランタイムです。

イメージは **『スイミー』** や **『がんばれ！ベアーズ』**。

```text
0B model / your model / your tool / ...
                 |
              GATTAI
                 |
                 v
            GOD NYĀZU
```

公開仕様は意図的に薄くしています。実運用で使うモデル名称、内部構成要素、役割、接続構造、合体規則、観測・選択・最適化ロジックは公開仕様ではありません。

### まず使う

ランタイム自体はcloneだけで使えます。

```bash
git clone https://github.com/hopeless-t/rokushin-gattai-god-nyas.git
cd rokushin-gattai-god-nyas
python -m unittest discover -s tests -v
```

### 公式default 0B初期アセット

公式の0Bスターターは**本体とは別配布**です。初回だけ取得し、その後はローカルコピーを使えます。

```bash
python examples/default_0b_demo.py "ベンチ回して"
```

または:

```python
from godnyas import load_default_0b

model = load_default_0b()  # 未取得なら公式配布元から一度だけ取得
print(model.respond("ベンチ回して"))
```

公式0Bアセットには**別ライセンス**が適用されます。再配布・ミラーは禁止です。公式配布が終了した場合、新規取得は終了しますが、既に正規取得したローカルコピーはそのライセンスの範囲で使い続けられます。

公式0Bがなくても、六親合体ゴッドにゃ〜ず本体は残ります。好きなLLM、ローカルモデル、自作モデル、ツールなどへ差し替えて構いません。

### Public reference shell

```python
from godnyas import GodNyasSet

system = GodNyasSet(parts=[part_a, part_b], composer=my_composer)
result = system.run(task)
```

`part_a` / `part_b` が実運用の何に対応するかは公開仕様ではありません。

### License

**六親合体ゴッドにゃ〜ず本体:** Apache License 2.0  
**公式default 0B asset:** separate asset license (not Apache-2.0)

Copyright 2026 Kiyotaka Tonegawa.

---

## English

### What is this?

**ROKUSHIN GATTAI GOD NYĀZU** is an experimental runtime for composing different capabilities—including 0B models—into one working system.

Think **Swimmy** or **The Bad News Bears**.

```text
0B model / your model / your tool / ...
                 |
              GATTAI
                 |
                 v
            GOD NYĀZU
```

The public specification is intentionally thin. Production model names, internal component identities and roles, topology, composition policy, and internal observation/selection/optimization logic are not part of the public specification.

### Quick start

The runtime itself works directly after clone:

```bash
git clone https://github.com/hopeless-t/rokushin-gattai-god-nyas.git
cd rokushin-gattai-god-nyas
python -m unittest discover -s tests -v
```

### Official default 0B starter asset

The official 0B starter is **distributed separately**. It is fetched once and then used from the local copy.

```bash
python examples/default_0b_demo.py "benchmark"
```

Or:

```python
from godnyas import load_default_0b

model = load_default_0b()  # fetches once from the official distribution point
print(model.respond("benchmark"))
```

The official 0B asset has a **separate license**. Redistribution and mirroring are not permitted. If official distribution ends, new acquisition ends; lawfully obtained local copies may continue to be used under that asset license.

God Nyāzu itself remains usable without the official 0B asset. Replace it with any LLM, local model, custom model, tool, or component you want.

### Public reference shell

```python
from godnyas import GodNyasSet

system = GodNyasSet(parts=[part_a, part_b], composer=my_composer)
result = system.run(task)
```

What `part_a` and `part_b` correspond to in production is not part of the public specification.

### License

**Rokushin Gattai God Nyāzu runtime:** Apache License 2.0  
**Official default 0B asset:** separate asset license (not Apache-2.0)

Copyright 2026 Kiyotaka Tonegawa.

---

Small alone. Different together.  
**合体すれば、なんとかなる。**
