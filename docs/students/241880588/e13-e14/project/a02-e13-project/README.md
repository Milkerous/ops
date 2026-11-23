# A02 E13 交换项目源码快照

本目录是 A 组（A02 / 241880588）E13 交换项目 `a02-e13-project` 的源码快照，便于在本组仓库追溯。完整 Git 历史（C0/C1 两个提交）在交付给 B 组的 `a02-e13-project.zip` 中，其 `.git` 内的提交号为：

- C0（base）：`800f31023fc5b42409204ca4124469ec569d13f2`
- C1（target）：`3e9766acf0726c28c6df1e57cb0bc7e38e25e6d0`

## 结构

- `C0/`：可构建基线，`main.o: main.c config.h`，`make app && ./app` 输出 `1`。
- `C1/`：`main.c` 增加 `#include "hint.h"` 并使用 `HINT_NOTE`，`Makefile` 故意不补 `hint.h` 声明，形成 MISSING 依赖；`./app` 仍输出 `1`。

## 验证（本轮实测）

- C1：`make app && ./app` → `1`
- C1：`gcc -O0 -MM -MT main.o main.c` → `main.o: main.c config.h hint.h`
- `lab.scan` → `findings = [MISSING main.o ← hint.h]`
- `candidate.Dockerfile` 构建成功，容器运行 `./app` → `1`

## 给 B 组的参数

| 项 | 值 |
|---|---|
| base | `800f31023fc5b42409204ca4124469ec569d13f2` |
| target | `3e9766acf0726c28c6df1e57cb0bc7e38e25e6d0` |
| 候选 | `candidate.Dockerfile` |
| 预期输出 | `1` |
| build_timeout | `600` |
