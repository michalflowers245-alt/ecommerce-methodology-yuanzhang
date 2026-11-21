# 电商方法论园长 Skill

面向电商机会判断、选品、供给、利润、内容获客、成交、交付和复购的结构化分析 Skill。项目强调证据、API 状态、假设与风险分开记录。

## 使用入口

- Skill 主文件：[`skills/ecommerce-methodology-yuanzhang/SKILL.md`](skills/ecommerce-methodology-yuanzhang/SKILL.md)
- API 配置说明：[`references/api-configuration.md`](skills/ecommerce-methodology-yuanzhang/references/api-configuration.md)
- 配置检查脚本：[`check_market_api_config.py`](skills/ecommerce-methodology-yuanzhang/scripts/check_market_api_config.py)
- 本地帖子关键词扫描脚本：[`scan_posts.py`](skills/ecommerce-methodology-yuanzhang/scripts/scan_posts.py)

配置检查脚本只核验环境变量是否存在，不发起网络请求，也不会打印密钥。帖子扫描脚本读取本地 JSON；原始帖子导出数据不包含在此仓库。

## 许可证

项目原创代码、Skill 指令和说明性分析文本按 [MIT License](LICENSE) 开放。具体范围与第三方材料边界见 [LICENSE-SCOPE.md](LICENSE-SCOPE.md)。
