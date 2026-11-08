# 决策记录

背景与约束：
- 本轨道为 A 组（buildchecker/EChecker），在受限 C/Make 样例上验证依赖图复用与保守刷新；实验必须在个人分支完成并保留可复核证据。
- 环境为既有 `course-e8e10:241880588` 镜像，禁止联网，构建与采集都在容器内进行。

选择与替代方案：
- A（缓存何时失效、配置身份如何绑定）：选择“预处理指令 + 配方 + CFLAGS + 编译器版本”的整体 key；key 完全相同且目标在旧 actual 中才复用，否则对该目标重跑 `gcc -MM`。替代方案是按文件 mtime/内容哈希判断，它更便宜但会漏掉宏和 include 结构变化；替代方案二是每次全量扫描，正确但失去增量意义。选保守 key 是为避免“错误复用”这一更严重的方向。
- B（共享变量怎样处理、失败怎样保证原目录不变）：本组 A 轨道不涉及 patch 写入，仅在 E8/E9/E10 读取 Makefile 变量并展开；失败时实验脚本以非零退出，证据目录保留，不覆盖旧 OUT。补丁路径的共享变量与回滚策略属 B 组轨道，本报告不冒充实现。

代价与覆盖范围：
- 保守 key 使 include/flags/header 三类变化都刷新两个目标，增量耗时接近全量（比值约 0.93—0.99），这是“宁可多刷、不可错用”的代价。
- 覆盖范围仅两个对象目标、显式规则和固定 CFLAGS 白名单；隐式规则、多目录、完整系统调用归并不在教学实现内。

验证命令与实际证据：
- E8：`work/e8-A-manual.golbo2`（baseline.json、buildchecker/、incremental.json、结论.txt）。
- E9：`work/e9-A-manual.NLQtOw`（baseline.json、C1/C2/C3.json、C0/C1/C2-build.log）。
- E10：`work/e10-A-manual.Z0vSKZ`（matrix/results.csv 30 行、performance-summary.csv、gate.json、final-buildchecker/）。
- 单测：`work/unit-tests-20261108-171156.log`，8 项 OK。
