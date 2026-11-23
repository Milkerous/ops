# A02 E13 C/Make 交换项目

本仓库是 A 组（A02 / 241880588）在 E13 使用的 C/Make 项目，基于课程 E8–E10 的 C/Make 样例改写，不是原封不动的课程生成样例。

## 提交

- `C0`：可构建基线。`main.c` 使用 `config.h` 的 `VALUE` 与 `helper.c` 的 `compute()`，`Makefile` 声明 `main.o: main.c config.h`。
- `C1`：`main.c` 新增 `#include "hint.h"` 读取 `HINT_NOTE`，但 `Makefile` 故意未补 `hint.h` 声明，用于制造真实的 MISSING 依赖。

## 构建与运行

```bash
make clean && make app
./app     # 输出 1
gcc -O0 -MM -MT main.o main.c   # C1 下应出现 hint.h
```

## 候选镜像

`candidate.Dockerfile` 安装 build-essential 后执行 `make app`，容器运行 `./app` 输出 `1`。
