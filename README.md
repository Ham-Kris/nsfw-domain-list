# Surge NSFW规则列表

本仓库自动从 [OISD NSFW列表](https://oisd.nl/) 获取ABP格式的NSFW规则，并转换为Surge规则列表格式。

## 文件说明

- `nsfw_rules.list` - 转换后的Surge NSFW规则列表
- `convert_abp_to_surge.py` - 转换脚本
- `Rule_example.list` - Surge规则格式示例

## 自动更新

本仓库使用GitHub Actions自动更新规则列表：

- **更新频率**: 每天早上8点UTC (北京时间16点)
- **触发方式**:
  - 定时任务 (cron)
  - 手动触发 (workflow_dispatch)
  - 脚本文件变更时自动触发

### 工作流功能

1. 从 `https://cdn.jsdelivr.net/gh/sjhgvr/oisd@main/abp_nsfw.txt` 下载最新规则
2. 转换为Surge格式
3. 检查是否有变更
4. 自动提交更新（如果有变更）

## 本地使用

### 手动转换

```bash
# 直接运行转换脚本
python3 convert_abp_to_surge.py

# 保存到文件
python3 convert_abp_to_surge.py > nsfw_rules.list
```

### 开发

```bash
# 克隆仓库
git clone https://github.com/Ham-Kris/nsfw-domain-list
cd nsfw-domain-list

# 运行脚本
python3 convert_abp_to_surge.py > nsfw_rules.list
```

## Surge配置

在Surge配置文件中添加：

```ini
[Rule]
RULE-SET,https://raw.githubusercontent.com/Ham-Kris/nsfw-domain-list/refs/heads/main/nsfw_rules.list,REJECT
```

## 统计信息

- **规则数量**: 约40万条
- **文件大小**: 约13MB
- **更新频率**: 每日更新

## 许可证

本项目仅用于技术研究和学习目的，请遵守相关法律法规。
