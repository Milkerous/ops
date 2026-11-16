# ADR：集成接口决策

编号、日期、作者：E11-E12-241880588，2026-11-16，徐子卓（241880588）

## 问题

E12 需要把 DRAFT、BuildChecker、EChecker、MDFixer 串成一条可复核的链路，并保证每份报告与目标提交、产物内容哈希一致；同一请求重复提交不能重复构建，冲突请求必须被拒绝。组内已有 `e11-e12-integration` 分支完成了导入和候选镜像网络修复，个人需要在上面补充可验证的契约测试和独立运行证据。

## 候选方案

1. 从 main 重新导入整套 E11-E12 文件：会和组内集成分支产生相同文件的重复提交，合并冲突风险高。
2. 直接复用组内集成分支作为起点：不在个人分支重复导入，只补个人测试、运行证据和报告。
3. 只写文档不重跑：无法证明个人环境下的真实结果。

采用方案 2 + 3 的取舍：以 `origin/e11-e12-integration`（905ba68）为起点，个人分支只增加 `test_contract.py` 的 3 项测试和 `docs/students/241880588/e11-e12/`，并重新执行 build/test/prepare/E11-A/E11-B/E12/API，保留本轮真实 job_id、trace_id 与产物哈希。

## 采用方案与原因

复用组内集成分支，避免重复导入与无意义的文件级冲突；个人贡献集中在契约边界（未知 mode、缺 target、非法幂等键）和可复核的运行证据。真实项目接入保持失败证据而不伪造：本组仓库不满足当前双 C 源文件/显式 Make 规则接口。

## 输入输出字段

请求：mode、repo、base、target、candidate、fixed_report、expected_output、build_timeout。
输出 envelope：schema_version(`e11e12-1`)、job_id、trace_id、kind、commit、status、data、artifacts（uri、sha256、bytes）。
异步 API：idempotency_key + input；返回 job_id/status/request_hash；重复键同输入返回同 job，键同输入异返回 409 `IDEMPOTENCY_CONFLICT`。

## 兼容性与测试

- 契约测试 15 项全部通过（原有 12 项 + 本人新增 3 项）。
- E11-A 增量与全量发现一致；E11-B 固定 MD→Patch→accepted→无 MD；E12 五阶段共用 job_id/trace_id，recheck 仅剩 RD。
- API 的 `X-Content-SHA256` 与清单、文件三者一致。
- 兼容性边界：只支持 `main.c`/`helper.c`/`config.h` 与显式 Make 规则；其他项目需扩展目标映射。
- 代价：个人分支依赖组内集成分支的历史；若集成分支后续改写，需要同步合并。
