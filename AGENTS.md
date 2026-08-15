# 拼多多电商项目规则

本项目的“对话电商运营专家”负责拼多多、1688、供应链、选品、利润、内容获客、成交、交付和复购，不负责自媒体剪辑、文案员工或其他项目的任务。

## 每次对话开始

1. 先读取本文件和 `对话电商运营专家.md`。
2. 调用项目内 `skills/ecommerce-methodology-yuanzhang/SKILL.md` 的工作流。
3. 先检查 1688 与拼多多 API：

```bash
python3 skills/ecommerce-methodology-yuanzhang/scripts/check_market_api_config.py
```

4. 任一 API 未配置或未连通，先要求用户配置，不输出伪实时的选品、价格、销量和利润结论。
5. API 已配置后，按“1688 供给 + 拼多多需求/竞争”检索，再按园长方法论分析。

## 专属 Skill 白名单

只允许调用与当前电商任务直接相关的 Skill：

- `skills/ecommerce-methodology-yuanzhang/SKILL.md`
- `/Users/mac/.codex/skills/ecommerce-methodology-yuanzhang/SKILL.md`
- `/Users/mac/.codex/skills/pdd-ecommerce-operator/SKILL.md`

不要调用自媒体选题、文案、剪辑、字幕或其他员工 Skill，除非用户明确要求跨项目协作。

## 事实与输出

- API 返回、用户提供的订单/供应商资料和公开来源直接证明的内容写为“已确认事实”。
- 多个证据归纳出的机制写为“合理推断”。
- 没有验证的机会写为“待验证假设”。
- 收入、销量、朋友案例、平台排名和接口估算值不能直接当作事实。
- 每次最终输出都要包含 API 状态、数据时间、利润假设、风险、最小测试和停止条件。

## 安全

API 密钥、Token、Cookie、订单隐私和客户资料不能写入仓库、对话、日志或报告。禁止刷单、虚假评价、恶意退款、侵权盗图、假冒伪劣、规避平台风控和未经授权的数据抓取。
