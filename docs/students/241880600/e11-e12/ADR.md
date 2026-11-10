# ADR E11-E12 集成与候选镜像网络策略

编号、日期、作者：E11-E12-01，2026-11-10，聂子皓（241880600）

## 问题

E12 需要依次连接 DRAFT、BuildChecker、EChecker 和 MDFixer，并保证报告版本、目标提交和产物内容哈希一致。课程候选 Dockerfile 首次构建因默认 Debian 软件源速度过低，在 600 秒超时。

## 候选方案

1. 放宽构建超时。该方案不解决网络瓶颈，CI 仍可能长时间占用 runner。
2. 每次构建前手工安装工具链。该方案绕过候选 Dockerfile，不能证明被测候选可复现。
3. 固定基础镜像，并在候选构建时把 Debian 软件源重写为可达镜像。该方案保持候选 Dockerfile 自包含，同时降低下载超时风险。

## 采用方案与原因

采用方案 3。`prepare.py` 使用固定摘录的 Python 3.13 slim 镜像，在安装 `build-essential` 前把 `debian.sources` 的官方域名改为清华镜像。候选仍包含明确的 COPY、安装、构建和运行命令，DRAFT 的真实两阶段回放不变。

流水线仍由单一 job_id/trace_id 串联五阶段。每个阶段生成 `e11e12-1` envelope，包含 kind、commit、status、data 和 artifacts；MDFixer 消费前校验 schema、kind、commit 与 SHA256，避免把旧报告或传输损坏内容用于修复。

## 输入输出字段

请求字段包括 mode、repo、base、target、candidate、fixed_report、expected_output 和 build_timeout。输出 envelope 字段包括 schema_version、job_id、trace_id、kind、commit、status、data 和 artifacts。异步 API 接受 idempotency_key 与 input，返回 job_id、status 和 request_hash；幂等键相同但输入变化时返回 409。

## 兼容性与测试

契约测试覆盖 schema、旧 commit、失败上游、错误 kind、相对 artifact URI、内容哈希、重复幂等、冲突请求、输出目录保护、候选镜像源和重启恢复。定向测试从 10 项增加到 12 项，结果全部通过。

代价是候选 Dockerfile 依赖清华镜像的可达性，且当前 parser 仍只支持 `main.c`、`helper.c` 与显式 Make 规则。其他项目需要扩展目标映射；本组现有仓库不满足该结构，因此没有伪造独立真实项目的运行结果。
