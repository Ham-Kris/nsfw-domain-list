# 部署指南

## GitHub 自动更新设置

### 1. 创建GitHub仓库

1. 访问 [GitHub](https://github.com)
2. 点击 "New repository"
3. 填写仓库信息：
   - Repository name: `surge-nsfw-rules` (或你喜欢的名称)
   - Description: `自动更新的Surge NSFW规则列表`
   - 选择 Public 或 Private
4. **不要**初始化README、.gitignore或license（因为我们已经有了）

### 2. 上传代码到GitHub

```bash
# 初始化git仓库（如果还没有）
git init

# 添加所有文件
git add .

# 提交初始版本
git commit -m "Initial commit: Add NSFW rules converter and auto-update workflow"

# 添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# 推送到GitHub
git push -u origin main
```

### 3. 启用GitHub Actions

1. 进入你的GitHub仓库页面
2. 点击 "Settings" 标签
3. 在左侧菜单中找到 "Actions" → "General"
4. 在 "Actions permissions" 部分选择：
   - ✅ Allow all actions and reusable workflows
5. 在 "Workflow permissions" 部分选择：
   - ✅ Read and write permissions
   - ✅ Allow GitHub Actions to create and approve pull requests

### 4. 验证设置

1. 进入 "Actions" 标签页
2. 你应该能看到 "Update NSFW Rules" 工作流
3. 点击工作流名称查看详情
4. 工作流应该已经开始运行（因为我们推送了代码）

### 5. 手动触发更新（可选）

如果想立即测试工作流：

1. 进入 "Actions" 标签页
2. 点击 "Update NSFW Rules" 工作流
3. 点击 "Run workflow" 按钮
4. 选择分支（通常是main）
5. 点击 "Run workflow"

## 工作流功能

### 自动触发条件

- **定时任务**: 每天早上8点UTC (北京时间16点)
- **手动触发**: 在Actions页面手动运行
- **代码变更**: 当 `convert_abp_to_surge.py` 或工作流文件变更时

### 工作流程

1. 下载最新的ABP NSFW规则
2. 转换为Surge格式
3. 检查是否有变更
4. 如果有变更，自动提交到仓库
5. 如果执行失败，创建Issue提醒

## 监控和维护

### 查看更新历史

- 进入 "Actions" 标签页查看每次运行的状态
- 进入 "Commits" 查看提交历史
- 每次成功更新都会生成带时间戳的提交信息

### 故障排除

如果工作流失败：

1. 检查 "Actions" 标签页的错误日志
2. 查看是否创建了Issue（自动故障报告）
3. 可能的原因：
   - 网络连接问题
   - ABP规则源站不可用
   - GitHub Actions配额不足

### 自定义配置

#### 修改更新频率

编辑 `.github/workflows/update-nsfw-rules.yml` 中的cron表达式：

```yaml
schedule:
  - cron: '0 8 * * *'  # 每天8点UTC
```

更多cron表达式：https://crontab.guru/

#### 修改规则源

如果要使用其他ABP规则源，修改 `convert_abp_to_surge.py` 中的URL：

```python
url = "https://your-custom-source.com/rules.txt"
```

## 使用规则文件

在Surge配置中添加：

```ini
[Rule]
RULE-SET,https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO_NAME/main/nsfw_rules.list,REJECT
```

记得将 `YOUR_USERNAME` 和 `YOUR_REPO_NAME` 替换为实际值。

## 注意事项

- 确保仓库设置为Public（如果想让其他人使用规则文件）
- 定期检查Actions使用情况，避免超出免费额度
- 工作流运行可能需要几分钟时间，请耐心等待
