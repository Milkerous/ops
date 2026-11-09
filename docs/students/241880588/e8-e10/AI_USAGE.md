# AI使用记录

工具/模型/日期：
- DeepSeek Harness 编码代理（deepseek-flash），2026-11-08。

输入上下文与问题：
- 输入：DevOps_E8_E10_20261031.zip 中的 A 组手册、`labs/e8e10/lab.py`、`test_profile.py` 与模板；问题：在本人服务器账号下按手册完整跑通 E8—E10，保留真实证据并生成个人测试与报告。

模型建议：
- 建议按手册 0—7/0—10/0—13 步逐步执行，使用 `lab_new_run` 每次新建 OUT；建议新增“config.h 间接 include extra.h”的单测，并给出独立预期。

采纳/拒绝及理由：
- 采纳：分步执行命令、证据目录命名、单测设计、报告与 ADR 草稿。
- 未采纳：模型曾建议用一键 `run_lab.py e8/e9/e10` 代替手册步骤；因手册要求保留逐步 steps 日志，改为逐块执行 `lab_python`。

人工修改：
- 本人核对每个 `STEP_EXIT_CODE`、`BASELINE_PASS`/`REUSE_PASS`/`C1_REUSE_PASS`/`C2_REFRESH_PASS`/`C3_RESOLVED_PASS`/`MATRIX_PASS`，确认 30 行 equal 全为 True 后才提交；报告中的 OUT、SHA、镜像 ID 均取自本人实际运行文件。

实际验证命令/输入/结果：
- `lab_ready`、`lab_new_run e8/e9/e10 A`、各步 `lab_python`；`docker run ... python3 -m unittest ...` 合并 main 后 11 项 OK（其中 3 项来自组内其他成员，本人新增 1 项）；E10 `gate.json` passed=true、rows=30；最终 BuildChecker status=SUCCEEDED。

未调用模型时写明未调用；记录参考实现和自己的贡献边界：
- 参考实现（fixture/scan/patch/buildchecker）来自课程实验包，本人未改写 `lab.py`；本人贡献为新增单测、实际运行证据、报告与 ADR。AI 用于命令执行与文档草稿，结论以本人复核的实际输出为准。
