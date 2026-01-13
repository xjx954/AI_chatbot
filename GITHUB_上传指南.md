# GitHub上传指南

## 📋 上传前准备

### 1. 检查文件

确保以下文件已准备好：
- ✅ 所有Python源代码文件
- ✅ `requirements.txt` 依赖文件
- ✅ `README.md` 项目说明
- ✅ `.gitignore` 文件（已创建，会忽略`.env`等敏感文件）

### 2. 确认敏感信息已排除

**重要！** 确保 `.env` 文件不会被上传：
- ✅ `.gitignore` 文件中已包含 `.env`
- ✅ 不要手动添加 `.env` 文件到Git

## 🚀 上传步骤

### 方法1: 使用Git命令行（推荐）

#### 步骤1: 初始化Git仓库

```bash
# 在项目目录下执行
cd E:\A_study
git init
```

#### 步骤2: 添加文件

```bash
# 添加所有文件（.gitignore会自动排除.env等文件）
git add .

# 查看将要提交的文件（确认没有.env文件）
git status
```

#### 步骤3: 提交代码

```bash
# 创建第一次提交
git commit -m "Initial commit: AI模型调用工具包和披萨订餐机器人"
```

#### 步骤4: 在GitHub创建仓库

1. 登录 GitHub: https://github.com
2. 点击右上角 "+" -> "New repository"
3. 填写仓库信息：
   - Repository name: `ai-chatbot-toolkit` (或你喜欢的名字)
   - Description: `AI模型调用工具包，支持多种AI服务，包含披萨订餐机器人示例`
   - 选择 Public 或 Private
   - **不要**勾选 "Initialize this repository with a README"（因为本地已有）
4. 点击 "Create repository"

#### 步骤5: 连接远程仓库并推送

```bash
# 添加远程仓库（将YOUR_USERNAME替换为你的GitHub用户名）
git remote add origin https://github.com/YOUR_USERNAME/ai-chatbot-toolkit.git

# 或者使用SSH（如果你配置了SSH密钥）
# git remote add origin git@github.com:YOUR_USERNAME/ai-chatbot-toolkit.git

# 推送代码到GitHub
git branch -M main
git push -u origin main
```

### 方法2: 使用GitHub Desktop（图形界面）

1. **下载GitHub Desktop**: https://desktop.github.com/
2. **安装并登录**你的GitHub账号
3. **创建新仓库**:
   - File -> New Repository
   - 选择本地路径: `E:\A_study`
   - 填写仓库名称和描述
   - 点击 "Create Repository"
4. **提交代码**:
   - 在左侧选择要提交的文件
   - 在底部填写提交信息: "Initial commit: AI模型调用工具包"
   - 点击 "Commit to main"
5. **发布到GitHub**:
   - 点击 "Publish repository"
   - 选择是否公开
   - 点击 "Publish repository"

### 方法3: 使用VS Code（如果使用VS Code）

1. **打开项目**: 在VS Code中打开 `E:\A_study`
2. **初始化Git**: 
   - 点击左侧源代码管理图标
   - 点击 "Initialize Repository"
3. **提交代码**:
   - 点击 "+" 暂存所有文件
   - 输入提交信息
   - 点击 "✓" 提交
4. **发布到GitHub**:
   - 点击 "..." -> "Publish to GitHub"
   - 选择是否公开
   - 填写仓库名称
   - 点击 "Publish"

## ✅ 上传后检查

上传完成后，访问你的GitHub仓库，确认：

1. ✅ 所有代码文件都已上传
2. ✅ `README.md` 显示正常
3. ✅ `.env` 文件**没有**被上传（重要！）
4. ✅ `requirements.txt` 存在
5. ✅ `.gitignore` 文件存在

## 🔒 安全提示

### 如果意外上传了 `.env` 文件

如果发现 `.env` 文件被上传了，立即执行以下步骤：

```bash
# 1. 从Git历史中删除.env文件
git rm --cached .env

# 2. 提交删除
git commit -m "Remove .env file"

# 3. 推送到GitHub
git push

# 4. 重要：立即去GitHub更换你的API密钥！
```

## 📝 后续更新

以后更新代码时：

```bash
# 1. 查看修改
git status

# 2. 添加修改的文件
git add .

# 3. 提交
git commit -m "更新说明"

# 4. 推送到GitHub
git push
```

## 🎯 推荐仓库设置

上传后，建议在GitHub仓库设置中：

1. **添加描述**: 在仓库主页点击 ⚙️ Settings -> 填写描述
2. **添加Topics**: 添加标签如 `python`, `ai`, `chatbot`, `deepseek`
3. **添加README徽章**: 可以在README中添加一些徽章展示项目状态

## 📚 参考资源

- Git官方文档: https://git-scm.com/doc
- GitHub帮助: https://docs.github.com/
- Git命令速查: https://education.github.com/git-cheat-sheet-education.pdf

---

**提示**: 如果遇到问题，可以查看GitHub的帮助文档或搜索相关错误信息。
