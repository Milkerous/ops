# 缺陷 Issue 与修复 PR

## Issue E13-ENV-001

- 用例编号与发现方：H1-H3 首次运行，A 组
- 输入仓库及完整 SHA：三个教师发放固定项目，SHA 见个人报告
- 预期 / 实际：broken Dockerfile 应稳定复现 MISSING_MAKE；实际在基础镜像 metadata 阶段被 INFRASTRUCTURE 阻断
- 失败阶段、错误码和原始日志：DRAFT iter-01，`failed to resolve source metadata`，日志位于 `work/e13-H1-jsmn-01/draft-build/iter-01/build-stderr.log`
- 严重度：非阻断环境问题
- 最小复现：DRAFT 容器执行 `docker build` 且基础镜像只有本地 digest、没有对应标签；daemon 代理为 `127.0.0.1:17897`
- 是否影响其他任务：会影响所有未缓存基础镜像的隔离测试

处理：将本机已存在的固定 digest 镜像标记为原始基础镜像标签，不修改上游源码或候选 Dockerfile。之后使用新目录运行 H1-H3，全部通过。建议服务器管理员移除失效 daemon 代理配置，或在 CI 保持正常 registry 网络。

## 已解决项 E13-C1

- 最终输入：A02 项目及 B 组 `number-guess-c`，完整 base/target 和 Git bundle 已保存。
- 实际结果：A02 E11-A、A02 到 B 路线交接、number-guess-c E11-A、number-guess-c 完整 E12 均 SUCCEEDED。
- 四服务复测：`number-guess-c` 通过 E14 Compose 五阶段，job `job-20137bc04cf848b5b49e7dcaae2924b4`，160 个产物哈希一致。
- 后续：E13-E14 PR 合并后可创建 `v0.9-rc`。
