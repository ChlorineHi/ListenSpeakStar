# AI赋能的英语听说训练智能平台

这是一个面向大学生的英语听说训练智能平台，提供四六级、雅思、托福等难度的听力材料及口语训练功能，通过自适应推送和智能反馈帮助学生提升英语听力和口语能力。

## 项目特点

- **多层次听力材料**：提供四六级、雅思、托福等不同难度的听力材料，覆盖多种话题。
- **智能水平评估**：通过评估试题精准检测用户的英语听力水平，为其推荐最适合的学习材料。
- **口语实时测评**：提供听后口语训练功能，AI技术实时评估发音、流利度和内容准确性。
- **智能学习反馈**：根据学习情况，提供重要单词、表达、背景知识和听力结构分析。
- **个性化学习路径**：自动推荐进阶材料，打造个性化学习路径。
- **Agent智能推荐系统**：基于LangChain和LangGraph构建的多Agent协作系统，深度分析用户学习情况，提供精准的材料推荐。

## Agent推荐系统

平台新增了基于LangChain和LangGraph构建的Agent智能推荐系统，通过多个专业Agent的协作，为用户提供更精准的学习材料推荐：

### Agent角色设计

1. **分析Agent (Analysis Agent)**
   - 职责：分析用户错题模式、识别薄弱领域
   - 输入：用户答题数据（包含错题信息）
   - 输出：用户能力分析报告

2. **推荐Agent (Recommendation Agent)**
   - 职责：基于分析结果推荐最合适的材料套题
   - 输入：用户能力分析报告、材料库信息
   - 输出：推荐材料列表及理由

3. **协调Agent (Orchestrator)**
   - 职责：管理整个工作流程，协调各Agent工作
   - 输入：用户请求
   - 输出：最终推荐结果

### 技术架构

- **LangChain**: 构建与大模型交互的组件
- **LangGraph**: 构建Agent工作流和状态管理
- **DeepSeek API**: 提供大语言模型能力

## 技术栈

### 后端
- Flask (Python)
- RESTful API设计
- DeepSeek API集成
- LangChain和LangGraph（Agent系统）
- JSON文件存储

### 前端
- Vue 3
- Vue Router
- Axios
- Tailwind CSS
- Wavesurfer.js (音频播放)

## 项目结构

```
english_training_platform/
├── backend/                  # Flask后端
│   ├── app.py                # Flask主应用
│   ├── routes/               # API路由
│   │   ├── listening.py      # 听力相关API
│   │   ├── speaking.py       # 口语相关API
│   │   ├── favorites.py      # 收藏功能API
│   │   ├── recommendation.py # Agent推荐系统API
│   ├── services/             # 业务逻辑服务
│   │   ├── deepseek.py       # DeepSeek API调用
│   │   ├── material_manager.py # 材料管理
│   │   ├── langchain_agent.py # Agent推荐系统实现
│   ├── data/                 # 数据存储
│   │   ├── materials.json    # 听力材料数据
│   │   ├── favorites.json    # 用户收藏数据
├── frontend/                 # Vue前端
│   ├── src/                  # 源代码
│   │   ├── components/       # Vue组件
│   │   ├── views/            # 页面视图
│   │   │   ├── AgentRecommendation.vue # Agent推荐页面
│   │   ├── router/           # 路由配置
│   │   ├── App.vue           # 主组件
│   │   ├── main.js           # 入口文件
│   ├── public/               # 静态资源
```

## 功能模块

1. **听力材料管理**：按难度和话题分类的听力材料，包含音频、文本和习题。
2. **听力训练与评估**：评估听力水平，智能推荐适合难度的材料。
3. **听后口语训练**：基于听力内容生成口语练习题，提供实时反馈。
4. **学习反馈**：提供词汇、表达、背景知识等全方位学习反馈。
5. **收藏功能**：支持收藏材料，方便复习。
6. **Agent智能推荐**：基于LangChain和LangGraph的多Agent协作推荐系统，深度分析用户学习情况，提供精准推荐。

## 安装与运行

### 后端

```bash
cd english_training_platform/backend
pip install -r requirements.txt
python app.py
```

### 前端

```bash
cd english_training_platform/frontend
npm install
npm run serve
```

## API接口

### 听力相关

- `GET /api/listening/materials` - 获取所有听力材料
- `GET /api/listening/materials/topic/:topic` - 按话题获取材料
- `GET /api/listening/materials/difficulty/:difficulty` - 按难度获取材料
- `GET /api/listening/material/:id` - 获取单个材料详情
- `GET /api/listening/assessment` - 获取评估试题
- `POST /api/listening/assessment/evaluate` - 评估听力水平
- `POST /api/listening/feedback` - 获取学习反馈
- `GET /api/listening/advanced/:level` - 获取进阶材料

### 口语相关

- `GET /api/speaking/tasks/:material_id` - 获取口语任务
- `POST /api/speaking/evaluate` - 评估口语
- `GET /api/speaking/sample-tasks` - 获取示例任务

### 收藏相关

- `GET /api/favorites/list/:user_id` - 获取收藏列表
- `POST /api/favorites/add` - 添加收藏
- `POST /api/favorites/remove` - 移除收藏
- `POST /api/favorites/check` - 检查是否已收藏

### Agent推荐系统

- `POST /api/recommendation/recommend` - 获取基于Agent系统的智能推荐

## 环境要求

- Python 3.8+
- Node.js 14+
- DeepSeek API密钥 (设置为环境变量 DEEPSEEK_API_KEY)
- LangChain 0.1.0+
- LangGraph 0.0.10+

## License

MIT 

## 材料目录结构

听力材料存放在 `frontend/public/materials/` 目录下，按照难度级别或考试年份组织：

```
materials/
├── CET4/                 # 四级模拟题
├── CET6/                 # 六级模拟题
├── IELTS/                # 雅思模拟题
├── TOEFL/                # 托福模拟题
├── 2022_06/              # 2022年6月真题
├── 2022_09/              # 2022年9月真题
└── ...
```

每个材料目录包含以下文件：
- `materials.json` - 材料元数据、问题和答案
- 音频文件 (.mp3)
- 可选的文本资料 (.docx, .pdf等)

## 最近更新

### 2025年06月16日 - 推荐匹配度显示修复

- 修复了推荐结果中匹配度显示为"%NaN%"的问题
- 优化了RecommendationResult组件，添加getMatchScore方法处理无效匹配度值
- 改进了RecommendationService中的validateRecommendations方法，确保每个推荐项都有有效的match_score值
- 为无效匹配度设置默认值(0.7)或显示"N/A"，提高用户体验

### 2025年06月15日 - 导航和数据传递优化

- 修复了提交答案按钮无法跳转到反馈页面的问题
- 优化了ListeningDetail和RecommendationPage组件间的数据传递
- 增强了本地存储答题数据的可靠性，添加了详细日志记录
- 改进了从听力练习到推荐页面的路由参数传递机制

### 2025年06月14日 - Agent系统日志优化

- 增强了Agent系统的日志记录功能，清晰标记工作流各阶段
- 使用专业的logging模块替代简单的print语句
- 添加了时间戳和日志级别，便于调试和监控
- 明确区分各个Agent的执行过程和状态变化

### 2025年06月13日 - 推荐系统优化

- 修复了推荐系统推送不存在材料的问题
- 优化了RecommendationService，添加材料可用性检查
- 改进了推荐验证流程，确保只推荐存在的材料
- 实现了安全的默认推荐机制，提高推荐系统的可靠性

### 2025年06月12日 - 错误处理优化

- 添加了全局错误处理组件ErrorMessage，提供统一的错误提示界面
- 优化了ListeningDetail和RecommendationPage组件的错误处理逻辑
- 改进了MaterialService中的材料获取逻辑，增强了错误处理能力
- 添加了友好的用户提示和重试功能，提升用户体验

### 2025年06月10日 - 添加Agent智能推荐系统

- 基于LangChain和LangGraph构建的多Agent协作系统
- 深度分析用户答题情况，识别薄弱环节
- 根据用户能力特点，精准推荐最适合的学习材料
- 提供个性化的学习建议和提升方向

### 2025年06月07日 - 材料加载问题修复

- 修复了无法加载年份格式材料（如2022_06、2023_06_1）的问题
- 改进了MaterialService.js中的材料ID匹配逻辑
- 添加了新材料添加指南，规范了材料目录和文件命名
- 详细信息请参考 `frontend/工作日志.md`

## 开发指南

### 环境要求

- Node.js 14+
- Vue.js 3.x
- Express 4.x

### 安装和运行

1. 克隆仓库
```
git clone https://github.com/yourusername/english_training_platform.git
cd english_training_platform
```

2. 安装依赖
```
# 安装前端依赖
cd frontend
npm install

# 安装后端依赖
cd ../backend
npm install
```

3. 运行开发服务器
```
# 运行前端
cd frontend
npm run serve

# 运行后端
cd ../backend
npm run dev
```

### 添加新材料

请参考 `frontend/public/materials/新材料添加指南.txt` 了解如何添加新的听力材料。

## 贡献指南

欢迎提交问题报告和功能请求。如果您想贡献代码，请遵循以下步骤：

1. Fork 仓库
2. 创建您的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开一个 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 LICENSE 文件 