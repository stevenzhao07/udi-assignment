# AGENTS.md · udi-assignment

> 机器可发现入口（AI 编码代理 / Codex / Claude / Cursor）。单一事实源：本文件。

## 这是什么
医疗器械唯一标识（UDI）赋码参考实现：GS1 GTIN-14 校验位计算（mod-10）、DI/PI 拆分（生产日期/批号/序列号/有效期）、HIBCC/ICCBBA 体系说明、FDA GUDID / NMPA 器械 UDI 数据库 / EUDAMED 三侧必填字段对照。补 fhir-ortho-toolkit（数据侧）与 multilingual-ifu（标签侧）之间的赋码缺口。

## 运行
```bash
python scripts/udi_assign.py --demo
python scripts/udi_assign.py --help
```

## 扩展契约（lgd-skeleton/1.0）
- **一切即插件**：仅依赖声明式 `module.json`，零配置。
- **按需装（lazy）**：仅 triggers 命中时加载。
- **可嵌套（nested）**：可被 `medical-ai-toolkit` 总入口路由。
- **扩展点**：`plugins/`(新增赋码体系：在 ISSUERS 注册表加一项。)

## 红线
纯技术贡献，不含商业营销；MedXpert 仅作为贡献者署名（@stevenzhao07）。
