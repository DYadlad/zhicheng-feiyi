# 智承非遗 - 传统文化数字化保护与传播平台

基于多模态AI的传统文化数字化保护与传播平台，提供非遗文化展示、图片修复和智能问答功能。

## 功能特点

1. **非遗文化展示**
   - 展示剪纸、昆曲、皮影、木雕四大非遗类别
   - 详细介绍历史渊源、技艺特点、主要流派和代表作品
   - 交互式标签切换，便于浏览不同类别

2. **图片修复**
   - 支持上传非遗老照片
   - 利用AI技术进行超分辨率修复
   - 实时预览和下载修复后的图片

3. **智能问答**
   - 对接通义千问大模型
   - 提供专业的非遗文化知识咨询服务
   - 支持连续对话和快速提问

## 技术栈

- **后端**: Python Flask
- **前端**: HTML5, CSS3, JavaScript
- **AI服务**: 通义千问API, DeepAI图片修复API

## 项目结构

```
jishe/
├── app.py                 # Flask主应用文件
├── requirements.txt       # Python依赖包
├── static/               # 静态资源目录
│   ├── css/
│   │   └── style.css     # 样式文件
│   ├── js/
│   │   ├── main.js       # 首页交互脚本
│   │   ├── showcase.js   # 展示页面脚本
│   │   ├── restore.js    # 修复页面脚本
│   │   └── chat.js       # 问答页面脚本
│   └── images/           # 图片资源目录
├── templates/            # HTML模板目录
│   ├── index.html        # 首页
│   ├── showcase.html     # 展示页面
│   ├── restore.html      # 修复页面
│   └── chat.html         # 问答页面
└── uploads/              # 上传文件目录
```

## 安装步骤

1. **克隆或下载项目**

2. **创建虚拟环境（推荐）**
   ```bash
   python -m venv venv
   ```

3. **激活虚拟环境**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

## 配置说明

### 配置通义千问API

在 [app.py](app.py) 文件中，找到以下代码行：

```python
api_key = "sk-your-api-key-here"
```

将 `sk-your-api-key-here` 替换为您的通义千问API密钥。

获取API密钥：
1. 访问 [阿里云百炼平台](https://bailian.console.aliyun.com/)
2. 注册/登录账号
3. 创建API-KEY

### 配置图片修复API

项目默认使用DeepAI的免费API进行图片修复。如需更换为其他服务，请修改 [app.py](app.py) 中的 `/api/restore` 路由。

## 运行项目

1. **启动Flask服务器**
   ```bash
   python app.py
   ```

2. **访问应用**
   打开浏览器访问: `http://localhost:5000`

## 使用说明

### 首页
- 浏览平台特色和非遗文化概览
- 点击导航栏切换不同功能模块

### 非遗展示
- 点击顶部标签切换不同非遗类别
- 查看详细的历史、技艺和代表作品信息

### 图片修复
- 点击或拖拽上传图片
- 点击"开始修复"按钮进行AI修复
- 修复完成后可下载修复后的图片

### 智能问答
- 在输入框中输入问题
- 点击"发送"或按Enter键提交
- 可使用快速提问按钮快速提问

## 注意事项

1. **API密钥安全**: 请勿将API密钥提交到公共代码仓库
2. **文件大小限制**: 图片上传最大支持16MB
3. **网络要求**: 需要稳定的网络连接以访问AI服务
4. **浏览器兼容**: 建议使用现代浏览器（Chrome、Firefox、Edge等）

## 常见问题

### Q: 图片修复失败怎么办？
A: 请检查网络连接，或稍后重试。如持续失败，可能是API服务暂时不可用。

### Q: 智能问答没有回复？
A: 请确认已正确配置通义千问API密钥，并检查网络连接。

### Q: 如何更换AI服务提供商？
A: 修改 [app.py](app.py) 中相应的API调用代码即可。

## 开发说明

### 添加新的非遗类别
1. 在 [app.py](app.py) 的 `get_heritage_data` 函数中添加新类别数据
2. 在 [showcase.html](templates/showcase.html) 中添加对应的标签按钮

### 自定义样式
修改 [static/css/style.css](static/css/style.css) 文件即可自定义页面样式。

## 许可证

本项目仅供学习和研究使用。

## 联系方式

如有问题或建议，欢迎反馈。
