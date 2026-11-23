# A02 E13 交换项目源码快照

本目录是 A 组（A02 / 241880588）E13 交换项目 `a02-e13-project` 的源码快照，便于在本组仓库追溯。给 B 组的完整 Git 历史在 `a02-E13-C1-for-B.zip` 中，其 `.git` 内的提交号为：

- C0（base）：`f384d66a8fd4b05a0c2429908aeac4af54e38047`
- C1（target）：`3f226a7e0803398fe551d49ef3b406e35eb0ae9b`

## 结构

- `C0/`：可构建基线，`main.o: main.c config.h`，`make app && ./app` 输出 `1`。
- `C1/`：`main.c` 增加 `#include "hint.h"` 并使用 `HINT_NOTE`，`Makefile` 故意不补 `hint.h` 声明，形成 MISSING 依赖；`./app` 仍输出 `1`。
- `handoff/`：A 侧 E11-A 的当次报告交接文件（`fixed-md.json`、`request-e11-b.json`，timeout=1800）。

## 验证（本轮实测）

- C1：`make app && ./app` → `1`
- C1：`gcc -O0 -MM -MT main.o main.c` → `main.o: main.c config.h hint.h`
- `lab.scan` → `findings = [MISSING main.o ← hint.h]`
- A 侧 E11-A：job_id `job-c4fd5c931bd840dd9a93ebf963c847ed`，trace_id `trace-1ab718ffcc154383a49b487c66adb81e`
- 交接报告 SHA256：`fbf8c6be2c55eef536bfc3241e366112b1ca9d24c53e4582148c64cce3aa0a54`

## 给 B 组的参数

| 项 | 值 |
|---|---|
| base | `f384d66a8fd4b05a0c2429908aeac4af54e38047` |
| target | `3f226a7e0803398fe551d49ef3b406e35eb0ae9b` |
| 候选 | `candidate.Dockerfile` |
| 预期输出 | `1` |
| build_timeout | `1800` |
