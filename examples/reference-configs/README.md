# 参考配置文件

> ⚠️ **注意**: 这些文件来自实际生产环境，**仅供学习参考**。请勿直接复制使用，请根据实际情况调整。

## 目录结构

```
examples/reference-configs/
├── SESSION-STATE.md              # 活跃任务状态模板
├── MEMORY.md                      # 长期记忆配置
├── AGENTS.md                      # Agent 配置
├── config-memory-manager.json     # memory-manager 状态
│
├── config-memory-causal/          # 因果推理配置
│   ├── action_log.jsonl          # 行动日志
│   ├── config.yaml               # 因果推理配置
│   └── graphs/
│       └── default.yaml           # 默认因果图
│
└── skills/                        # Skills 实现参考
    ├── agent-memory-hook.py      # 会话 Hook 脚本
    └── memory.py                  # agent-memory 核心实现
```

## 文件说明

### SESSION-STATE.md
bulletproof-memory 的活跃任务状态文件模板，包含：
- Current Task
- Immediate Context
- Recent Decisions
- Open Threads
- Key Files

### MEMORY.md
长期记忆配置文件，包含：
- 身份信息
- 账户凭证
- 核心规则
- 记忆系统架构

### AGENTS.md
Agent 配置文件，包含：
- 记忆协议（WAL、Compaction Recovery、Memory Flush）
- 因果推理规则
- 心跳检查配置

### config-memory-causal/
因果推理的实际配置：
- `action_log.jsonl` - 真实行动日志示例
- `config.yaml` - 完整配置
- `graphs/default.yaml` - 因果图定义

### skills/
Skills 的实际实现代码：
- `agent-memory-hook.py` - 会话自动化 Hook
- `memory.py` - agent-memory 核心逻辑

## 使用方法

1. **学习配置格式**: 查看这些文件了解如何配置
2. **参考最佳实践**: 学习实际使用中的模式
3. **按需调整**: 根据你的需求修改配置

## 注意事项

- 🔒 **敏感信息已清理**: API keys、密码等已移除
- 📝 **实际生产配置**: 这些是真实使用的配置
- ⚡ **按需修改**: 不要直接复制，请按实际情况调整
