# 🧠 OpenClaw Memory Architecture

<div align="center">

![Memory Architecture](docs/images/architecture.png)

**为 OpenClaw AI 助手打造的完整记忆系统**

[English](README_EN.md) | [中文](README.md)

</div>

---

## 📋 目录

- [🎯 概述](#-概述)
- [🏗️ 架构设计](#️-架构设计)
- [📦 组件详解](#-组件详解)
- [🚀 快速开始](#-快速开始)
- [⚙️ 配置指南](#️-配置指南)
- [📝 使用文档](#-使用文档)
- [🔧 开发指南](#-开发指南)
- [🤝 贡献指南](#-贡献指南)
- [📄 许可证](#-许可证)

---

## 🎯 概述

### 什么是记忆架构？

OpenClaw Memory Architecture 是一套**完整的记忆管理系统**，为 AI 助手提供：

- ✅ **持久化记忆** - 跨会话保存重要信息
- ✅ **上下文管理** - 永远不丢失当前任务状态
- ✅ **因果推理** - 预测行动结果，从经验中学习
- ✅ **语义搜索** - 快速找到相关内容
- ✅ **三层记忆** - 情景/语义/程序性记忆

### 核心设计原则

1. **永不丢失** - 即使上下文被压缩，也能恢复状态
2. **互补协作** - 每个组件专注特定功能，互相补充
3. **自动管理** - 减少手动操作，自动化处理
4. **可扩展性** - 易于添加新组件或修改现有组件

---

## 🏗️ 架构设计

### 整体架构图

```
┌─────────────────────────────────────────────────────────────────────┐
│                    OpenClaw Memory System                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌────────────────────┐    ┌────────────────────┐                  │
│  │ bulletproof-memory │    │    agent-memory     │                  │
│  │     (WAL 协议)     │    │   (SQLite 持久化)   │                  │
│  │                    │    │                    │                  │
│  │ • SESSION-STATE   │    │ • Facts            │                  │
│  │ • 主动写入        │    │ • Lessons          │                  │
│  │ • 上下文恢复      │    │ • Entities         │                  │
│  └────────────────────┘    └────────────────────┘                  │
│                                                                       │
│  ┌────────────────────┐    ┌────────────────────┐                  │
│  │   memory-manager   │    │       QMD          │                  │
│  │     (三层记忆)      │    │    (向量搜索)      │                  │
│  │                    │    │                    │                  │
│  │ • Episodic        │    │ • 语义搜索         │                  │
│  │ • Semantic        │    │ • 相似度匹配       │                  │
│  │ • Procedural      │    │ • 自动索引         │                  │
│  └────────────────────┘    └────────────────────┘                  │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    causal-inference                            │  │
│  │                 (因果推理与行动预测)                             │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

### 组件分工

| 组件 | 类型 | 存储位置 | 主要功能 |
|------|------|---------|---------|
| **bulletproof-memory** | WAL 协议 | `SESSION-STATE.md` | 活跃任务上下文防丢失 |
| **agent-memory** | SQLite | `~/.agent-memory/` | Facts/Lessons/Entities 持久化 |
| **causal-inference** | 推理引擎 | `memory/causal/` | 因果推理与行动预测 |
| **memory-manager** | 文件系统 | `memory/` | 三层记忆管理 |
| **QMD** | 向量数据库 | `~/.cache/qmd/` | 语义搜索与相似度匹配 |

### 数据流

```
用户输入
    │
    ├──► WAL 协议 ──► SESSION-STATE.md (立即写入)
    │
    ├──► agent_memory.remember() ──► SQLite
    │
    ├──► memory-manager ──► daily notes
    │
    └──► QMD ──► 向量索引
```

---

## 📦 组件详解

### 1. bulletproof-memory 🛡️

**功能**: 使用 Write-Ahead Log (WAL) 协议，确保活跃任务永远不会丢失。

**核心特点**:
- 用户输入时**立即写入**文件
- 不依赖 agent 记忆，可靠性极高
- 会话压缩后自动恢复

**文件位置**: `skills/bulletproof-memory/`

**关键文件**:
```
bulletproof-memory/
├── SKILL.md              # 使用文档
├── SESSION-STATE.md      # 活跃任务模板
└── README.md            # 详细说明
```

**SESSION-STATE.md 模板**:

```markdown
# Current Task
[当前任务描述]

# Immediate Context
[重要上下文]

# Key Files
- [文件1]
- [文件2]

# Recent Decisions
- [决定1]
- [决定2]
```

### 2. agent-memory 🗄️

**功能**: 跨会话持久化存储，保存事实、教训和实体信息。

**核心特点**:
- SQLite 数据库存储
- 支持标签和查询
- 自动学习从经验中

**文件位置**: `skills/agent-memory/`

**核心功能**:

```python
from agent_memory import AgentMemory

mem = AgentMemory()

# 记忆事实
mem.remember("用户喜欢简洁的汇报", tags=["preference", "communication"])

# 从经验学习
mem.learn(
    action="使用了复杂的长句",
    context="汇报",
    outcome="negative",
    insight="应该用简洁的短句"
)

# 搜索记忆
facts = mem.recall("用户 汇报 风格")

# 获取教训
lessons = mem.get_lessons(context="汇报", outcome="negative")
```

### 3. causal-inference 🎯

**功能**: 为行动添加因果推理，预测结果而非盲目行动。

**核心特点**:
- 预测行动结果
- 调试失败原因
- 从历史中学习
- 安全约束保护

**文件位置**: `skills/causal-inference/`

**使用场景**:

| 场景 | 示例 |
|------|------|
| **预测结果** | "如果我现在发邮件，会回复吗？" |
| **调试失败** | "为什么这个任务失败了？" |
| **回填历史** | "分析我过去的行为模式" |
| **规划干预** | "我应该现在做还是等会儿？" |

**工作流程**:

```python
# 行动前
1. 记录 pre_state
2. 查询因果模型预测结果
3. 高风险时确认用户

# 行动后
1. 记录 action + context + time
2. 设置提醒检查结果

# 结果观察后
1. 更新 action log
2. 重新估计因果效应
```

### 4. memory-manager 📚

**功能**: 三层记忆管理 - 情景/语义/程序性记忆。

**核心特点**:
- Episodic (情景) - 发生了什么
- Semantic (语义) - 知道什么
- Procedural (程序) - 如何做

**文件位置**: `skills/memory-manager/`

**三层记忆**:

```
memory/
├── episodic/           # 情景记忆
│   └── YYYY-MM-DD.md  # 每日日志
├── semantic/          # 语义记忆
│   └── topics/       # 主题知识库
└── procedural/       # 程序记忆
    └── workflows/    # 工作流程
```

### 5. QMD 🔍

**功能**: 向量数据库，提供语义搜索和相似度匹配。

**核心特点**:
- 语义搜索
- 相似度匹配
- 自动索引
- 快速检索

**文件位置**: `skills/qmd/`

**使用示例**:

```bash
# 搜索记忆
qmd search "用户偏好"

# 查找相似
qmd similar "之前的一个任务"

# 索引新内容
qmd index ./memory/semantic/
```

---

## 🚀 快速开始

### 环境要求

- Python 3.8+
- OpenClaw 最新版本
- SQLite 3
- 至少 100MB 空闲空间

### 安装步骤

#### 步骤 1: 克隆仓库

```bash
git clone https://github.com/infinitelab/openclaw-memory-architecture.git
cd openclaw-memory-architecture
```

#### 步骤 2: 安装依赖

```bash
# 核心依赖
pip install -r requirements.txt

# 可选依赖
pip install -r requirements-optional.txt
```

#### 步骤 3: 配置 OpenClaw

编辑 `~/.openclaw/openclaw.json`：

```json
{
  "skills": {
    "entries": {
      "bulletproof-memory": {
        "enabled": true
      },
      "agent-memory": {
        "enabled": true
      },
      "causal-inference": {
        "enabled": true
      },
      "memory-manager": {
        "enabled": true
      }
    }
  }
}
```

#### 步骤 4: 初始化数据目录

```bash
# 创建必要目录
mkdir -p ~/.openclaw/workspace/memory/causal/{graphs,estimates}
mkdir -p ~/.agent-memory/

# 初始化数据库
python scripts/init_agent_memory.py

# 创建配置文件
cp config/causal-config.yaml ~/.openclaw/workspace/memory/causal/config.yaml
```

#### 步骤 5: 重启 OpenClaw

```bash
openclaw gateway restart
```

### 验证安装

```bash
# 检查各组件状态
python scripts/check_status.py

# 预期输出:
# ✅ bulletproof-memory: 正常
# ✅ agent-memory: 正常
# ✅ causal-inference: 正常
# ✅ memory-manager: 正常
# ✅ QMD: 正常
```

---

## ⚙️ 配置指南

### 完整配置示例

```yaml
# ~/.openclaw/workspace/memory/causal/config.yaml

# 启用域
domains:
  - email
  - calendar
  - messaging
  - tasks
  - files

# 安全阈值
thresholds:
  max_uncertainty: 0.3      # 不确定性 >30% 时不行动
  min_expected_utility: 0.1  # 预期收益 <10% 时不行动

# 保护操作 (需要用户确认)
protected_actions:
  - delete_email
  - cancel_meeting
  - send_to_new_contact
  - financial_transaction
  - delete_file
  - git_force_push

# 文件路径
graph_file: memory/causal/graphs/default.yaml
action_log: memory/causal/action_log.jsonl
```

### 环境变量

```bash
# 可选配置
export MEMORY_DIR=~/.openclaw/workspace/memory
export AGENT_MEMORY_DB=~/.agent-memory/memory.db
export QMD_CACHE=~/.cache/qmd
```

### OpenClaw 集成配置

```json
{
  "skills": {
    "entries": {
      "bulletproof-memory": {
        "enabled": true,
        "options": {
          "auto_write": true,
          "recovery_enabled": true
        }
      },
      "agent-memory": {
        "enabled": true,
        "options": {
          "auto_learn": true,
          "tags_enabled": true
        }
      },
      "causal-inference": {
        "enabled": true,
        "options": {
          "predict_before_action": true,
          "log_outcomes": true
        }
      }
    }
  }
}
```

---

## 📝 使用文档

### 日常使用

#### 会话开始时

```python
# 自动执行的流程 (由 bulletproof-memory 处理)
1. 读取 SESSION-STATE.md
2. 加载 MEMORY.md
3. 读取今日日志
4. 从 agent-memory 加载最近教训
```

#### 会话进行中

```python
# 用户输入重要信息时 (WAL 协议)
update_session_state(
    task="当前任务",
    context="重要上下文",
    decisions=["决定1", "决定2"]
)

# 记录新事实时
mem.remember("用户偏好", tags=["preference"])

# 从经验学习时
mem.learn(
    action="执行的操作",
    context="情境",
    outcome="结果 (positive/negative)",
    insight="学到的教训"
)

# 预测行动结果时
predicted_outcome = causal_inference.predict(
    action="send_email",
    context={"recipient": "新客户"},
    options=["now", "later"]
)
```

#### 会话结束时

```python
# 自动执行的流程
1. 整理今日学到的东西
2. 更新 agent-memory
3. 更新 memory-manager
4. 刷新 SESSION-STATE.md
```

### 高级用法

#### 因果图配置

```yaml
# memory/causal/graphs/email.yaml

email:
  nodes:
    send_time: "发送时间 (morning/afternoon/evening)"
    subject_style: "主题风格"
    recipient_type: "收件人类型"

  edges:
    - [send_time, reply_prob, "发送时间影响回复概率"]
    - [subject_style, open_rate, "主题风格影响打开率"]

  estimates:
    send_time→reply_prob:
      morning: 0.35
      afternoon: 0.28
      evening: 0.22
```

#### 向量搜索

```python
# 语义搜索
results = qmd.search(
    query="用户的技术偏好",
    top_k=5,
    threshold=0.7
)

# 相似文档
similar = qmd.find_similar(
    document_id="doc_123",
    top_k=3
)
```

### 故障排除

#### 问题: agent-memory 无法连接

```bash
# 检查数据库
ls -la ~/.agent-memory/

# 重新初始化
python scripts/reinit_agent_memory.py

# 检查错误日志
tail -50 ~/.openclaw/logs/memory.log
```

#### 问题: QMD 索引损坏

```bash
# 重建索引
qmd rebuild --force

# 验证索引
qmd verify
```

#### 问题: SESSION-STATE.md 恢复失败

```bash
# 检查备份
ls -la ~/.openclaw/workspace/.backups/

# 手动恢复
cp ~/.openclaw/workspace/.backups/SESSION-STATE.md.backup ~/.openclaw/workspace/SESSION-STATE.md
```

---

## 🔧 开发指南

### 项目结构

```
openclaw-memory-architecture/
├── README.md                 # 主文档
├── README_EN.md             # 英文版
├── requirements.txt         # 核心依赖
├── requirements-optional.txt # 可选依赖
├── LICENSE                   # 许可证
│
├── skills/                  # Skills 目录
│   ├── bulletproof-memory/ # WAL 协议
│   ├── agent-memory/       # SQLite 持久化
│   ├── causal-inference/   # 因果推理
│   ├── memory-manager/     # 三层记忆
│   └── qmd/                # 向量搜索
│
├── docs/                    # 文档
│   ├── images/             # 图片
│   ├── architecture.md    # 架构详解
│   ├── api/                # API 文档
│   └── examples/           # 示例
│
├── scripts/                 # 工具脚本
│   ├── init_agent_memory.py
│   ├── check_status.py
│   ├── backup.py
│   └── migrate.py
│
├── config/                  # 配置模板
│   ├── causal-config.yaml
│   ├── memory-config.yaml
│   └── qmd-config.yaml
│
└── examples/               # 使用示例
    ├── basic_usage.py
    ├── causal_examples.py
    └── workflow_examples.py
```

### 添加新组件

1. 创建目录: `skills/<component-name>/`
2. 添加 `SKILL.md` 文档
3. 在 `docs/architecture.md` 中添加说明
4. 更新 `README.md`
5. 编写测试用例

### 扩展现有组件

#### 扩展 agent-memory

```python
# skills/agent-memory/extensions/custom_plugin.py

from agent_memory import AgentMemory

class CustomPlugin:
    def __init__(self, mem: AgentMemory):
        self.mem = mem
    
    def custom_function(self):
        """自定义功能"""
        pass

# 注册插件
AgentMemory.register_plugin("custom", CustomPlugin)
```

#### 扩展因果图

```yaml
# skills/causal-inference/domains/custom.yaml

custom_domain:
  nodes:
    custom_var1: "变量1"
    custom_var2: "变量2"
  
  edges:
    - [custom_var1, custom_var2, "关系描述"]
```

### 测试

```bash
# 运行所有测试
pytest tests/

# 运行特定组件测试
pytest tests/test_agent_memory.py
pytest tests/test_causal_inference.py

# 生成测试覆盖率
pytest --cov=skills tests/
```

---

## 🤝 贡献指南

### 贡献方式

1. **报告 Bug** - 在 Issues 中提交
2. **提出功能建议** - 在 Discussions 中讨论
3. **提交代码** - Fork 后 Pull Request
4. **改进文档** - 直接编辑 README

### 开发环境设置

```bash
# Fork 并克隆
git clone https://github.com/YOUR_USERNAME/openclaw-memory-architecture.git
cd openclaw-memory-architecture

# 创建开发分支
git checkout -b feature/new-component

# 安装开发依赖
pip install -r requirements-dev.txt

# 运行测试
pytest tests/ -v

# 提交更改
git add .
git commit -m "Add: 新功能描述"
git push origin feature/new-component
```

### 代码规范

- Python: PEP 8 + Black 格式化
- 文档: Markdown + 简洁示例
- 提交: Conventional Commits

---

## 📄 许可证

本项目采用 MIT 许可证。

详见 [LICENSE](LICENSE) 文件。

---

## 🙏 致谢

- [OpenClaw](https://github.com/openclaw/openclaw) - AI 助手框架
- [AgentMemory](https://github.com/) - 记忆库
- [QMD](https://github.com/) - 向量搜索
- 所有贡献者！

---

<div align="center">

**如果这个项目对你有帮助，请 ⭐ Star 支持！**

Made with 🦭 by Luxi & infinitelab

</div>
