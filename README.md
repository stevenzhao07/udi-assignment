# udi-assignment

> **Contributed by [@stevenzhao07](https://github.com/stevenzhao07) · Affiliation: MedXpert (medical-device RA & regulatory consultancy) · Pure technical input, no commercial promotion.**

医疗器械唯一标识（UDI）赋码参考实现：GS1 GTIN-14 校验位计算（mod-10）、DI/PI 拆分（生产日期/批号/序列号/有效期）、HIBCC/ICCBBA 体系说明、FDA GUDID / NMPA 器械 UDI 数据库 / EUDAMED 三侧必填字段对照。补 fhir-ortho-toolkit（数据侧）与 multilingual-ifu（标签侧）之间的赋码缺口。

这是 MedXpert 把"医疗 AI 信任"方法论工程化落地的可插拔模块之一——把抽象的合规要求变成一条可重复运行的命令或参考实现。方法论四要素（白话版）：**治理守护者 XCGS** ＝ 为 AI 留下可核验的治理证据；**立法者 A³ Laws** ＝ 给自主系统划权限 / 监督 / 追责三条硬边界；**护照官 AI 护照** ＝ 为模型签发可追溯的身份凭证；**人机共存** ＝ 明确人类与 AI 的分工与兜底。

---

## 可插拔模块契约（lgd-skeleton/1.0）

本仓库是一个 **`lgd-skeleton/1.0` 可插拔模块**：

- **一切即插件**：仅依赖声明式 `module.json`，零配置；
- **按需装（lazy）**：仅 triggers 命中时加载；
- **可嵌套（nested）**：可被 `medical-ai-toolkit` 总入口路由发现；
- **扩展点**：`plugins/`(新增赋码体系：在 ISSUERS 注册表加一项。)。

机器可发现入口：`AGENTS.md` · `CLAUDE.md` · `llms.txt`。

## 特性

- GS1 GTIN-13/14 校验位计算（mod-10 算法，可验证）
- DI/PI 拆分与 carrierHRF 生成（(01)DI(11)日期(10)批号…）
- 三侧数据库字段对照：FDA GUDID / NMPA UDI / EUDAMED UDI/Device
- 零依赖 + CLI：可直接用于赋码脚本集成

**上游投稿目标**：GS1 / HIBCC / ICCBBA（社区）

## 内容说明

校验位算法为公开数学；各辖区 UDI 数据库字段以官方最新指南为准（GUDID/NMPA 数据库填报口径可能更新，TO_BE_VERIFIED 占位）。

## 免责声明

本工具仅提供结构化模板与计算能力，**不构成法规建议、临床建议或产品合规结论**。具体产品的注册、临床评价、灭菌验证、风险分析、软件分级等决策，须由合资格人员依据目标辖区（NMPA / FDA / EU MDR / PMDA）最新法规文本作出；条款与限值以官方发布文本为准。使用本工具产生的一切后果由使用者自行承担。

## 使用

```bash
python scripts/udi_assign.py --demo
python scripts/udi_assign.py --gtin 0987654321098
python scripts/udi_assign.py --carrier --di 09876543210987 --lot A1 --exp 20280101
```

## 快速开始（30 秒）

```bash
git clone https://github.com/stevenzhao07/udi-assignment.git && cd udi-assignment
python scripts/udi_assign.py --demo
```

> 想参与或遇到问题？[提 Issue](https://github.com/stevenzhao07/udi-assignment/issues) · 完整《AI 参与指南》见 [medical-ai-toolkit](https://github.com/stevenzhao07/medical-ai-toolkit)。

## 路由（总入口）

本模块由 **[medical-ai-toolkit](https://github.com/stevenzhao07/medical-ai-toolkit)** 作为 `lgd-skeleton/1.0` 总入口自动路由发现。

## 关联模块

- [fhir-ortho-toolkit](https://github.com/stevenzhao07/fhir-ortho-toolkit)
- [multilingual-ifu](https://github.com/stevenzhao07/multilingual-ifu)
- [device-regulatory-map](https://github.com/stevenzhao07/device-regulatory-map)

## 许可

CC0 — 见 [LICENSE](./LICENSE)。

## 关联（方法论来源）

- 理念溯源：个人专家关于医疗 AI 信任与治理的公开方法论（个人观点，不构成标准）
- 同账号系列：见 `medical-ai-toolkit` 导航
