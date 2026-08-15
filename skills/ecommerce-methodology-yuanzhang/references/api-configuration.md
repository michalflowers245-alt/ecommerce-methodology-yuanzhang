# 1688 与拼多多 API 配置规范

## 目的

本文件只说明配置契约，不保存任何密钥。1688 和拼多多的官方开放能力、授权方式、接口名称和权限会变化，必须以你实际申请的官方开放平台或明确授权的服务商文档为准。不要把来路不明的“万能接口”当成官方 API。

## 推荐配置方式

优先使用 Codex/运行环境的安全密钥配置。不要把值写入 Skill、对话、Markdown、Git 仓库、截图或普通表格。

环境变量名称建议如下：

```text
ECOMMERCE_1688_API_BASE_URL
ECOMMERCE_1688_API_KEY       # 如果服务商使用 API Key
ECOMMERCE_1688_ACCESS_TOKEN  # 如果使用 OAuth/Token
ECOMMERCE_1688_APP_KEY       # 只有接口文档要求时配置
ECOMMERCE_1688_APP_SECRET    # 只有接口文档要求时配置

ECOMMERCE_PDD_API_BASE_URL
ECOMMERCE_PDD_API_KEY
ECOMMERCE_PDD_ACCESS_TOKEN
ECOMMERCE_PDD_CLIENT_ID
ECOMMERCE_PDD_CLIENT_SECRET
```

每个平台至少需要：

1. 一个明确的 API Base URL；
2. 一种有效授权方式：Access Token，或 API Key，或文档要求的 Client/App ID + Secret；
3. 与任务相符的权限，例如商品检索、商品详情、推广/佣金、店铺/订单或数据报表；
4. 调用配额、限流和数据时间范围；
5. 一次成功的最小测试请求。

不要同时把多个服务商的字段混在一起。若 1688 使用官方 OAuth，PDD 使用第三方聚合服务，要分别记录提供方、授权范围、费用、数据口径和服务商条款。

## 配置完成标准

“已配置”不等于环境里有一串字符串。只有以下条件都满足，Skill 才能进入正式分析：

- 1688 授权成功；
- 拼多多授权成功；
- 两个平台都能返回与本次问题相关的最小字段；
- 返回结果包含时间或版本信息；
- API 权限、限流或错误状态可以被识别；
- 密钥不会出现在终端输出、日志和最终报告中。

## 最小能力清单

### 1688

至少需要其中的商品/供应检索能力：

- 关键词或类目搜索；
- 商品详情和规格；
- 供货价、起批量、库存或发货信息；
- 供应商/店铺基础信息；
- 退换货、分销或代发字段（若接口提供）。

### 拼多多

至少需要其中的需求/竞争检索能力：

- 关键词或类目搜索；
- 商品详情、售价和规格；
- API 实际提供的销量、评价、活动或佣金字段；
- 商品/店铺公开信息；
- 用户评论或问答字段（若接口提供）。

“若接口提供”非常重要：没有权限或接口不返回的字段必须留空并报告缺口，不能从标题或搜索排名臆造销量、利润或转化率。

## 标准化返回结构

适配器应尽量把平台结果映射成：

```json
{
  "platform": "1688|pdd",
  "provider": "官方平台或明确服务商名称",
  "retrieved_at": "ISO-8601 时间",
  "query": "原始检索词",
  "items": [
    {
      "item_id": "平台商品 ID",
      "title": "商品标题",
      "category": "类目",
      "price": {"value": null, "currency": "CNY", "unit": "件"},
      "sales_signal": {"value": null, "unit": "provider-defined", "as_of": null},
      "supplier": {"name": null, "location": null},
      "fulfillment": {"stock": null, "lead_time": null, "shipping": null},
      "after_sales": {"return_policy": null, "defect_policy": null},
      "source_url": null,
      "raw_fields_available": []
    }
  ],
  "warnings": []
}
```

适配器可以保留平台原始字段，但分析层只使用有来源、有时间、有口径的字段。

## 连接失败时的处理

- 未授权：停止实时推荐，告诉用户缺少授权范围。
- Token 过期：要求重新授权，不索取并回显旧 Token。
- 限流：记录时间和错误码，降低请求频率或等待，不绕过限制。
- 字段缺失：标记“未提供”，不使用猜测值。
- 第三方接口不可验证：标记服务商来源、费用和风险，不能称为官方数据。
- 搜索结果为空：调整关键词、类目或时间窗口，并把调整记录下来。

## 当前配置回复模板

用户未配置时只需要回复：

```text
当前还不能进行实时电商检索，因为以下 API 尚未完成配置：
- 1688：缺少 [接口地址/授权方式/权限]
- 拼多多：缺少 [接口地址/授权方式/权限]

请按 api-configuration.md 配置到安全环境，不要把密钥发在聊天里。
配置后回复“已配置”，我会先做连通性检查，再执行选品、供货、竞争和利润分析。
```
