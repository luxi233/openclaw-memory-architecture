"""
Causal Inference Protocol Implementation

Manual causal reasoning and outcome prediction.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional


CAUSAL_DIR = Path("~/.openclaw/workspace/memory/causal").expanduser()
ACTION_LOG = CAUSAL_DIR / "action_log.jsonl"
CONFIG_FILE = CAUSAL_DIR / "config.yaml"
GRAPHS_DIR = CAUSAL_DIR / "graphs"
ESTIMATES_DIR = CAUSAL_DIR / "estimates"


def load_config() -> Dict:
    """加载配置文件"""
    if CONFIG_FILE.exists():
        import yaml
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    return {}


def save_config(config: Dict):
    """保存配置"""
    import yaml
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(config, f)


def predict(action: str, context: Dict) -> Dict[str, Any]:
    """
    预测行动结果
    
    Args:
        action: 行动类型 (send_email, create_meeting, etc.)
        context: 行动上下文
        
    Returns:
        Dict with probability, uncertainty, expected_utility
    """
    config = load_config()
    
    # 默认值
    probability = 0.5
    uncertainty = 0.3
    
    # 从因果图加载信息
    action_type = action.split('_')[0]
    graph_file = GRAPHS_DIR / f"{action_type}.yaml"
    
    if graph_file.exists():
        import yaml
        with open(graph_file, 'r', encoding='utf-8') as f:
            graph = yaml.safe_load(f)
        
        if graph:
            # 获取 edges
            domain_data = list(graph.values())[0] if graph else {}
            edges = domain_data.get('edges', [])
            
            # 检查上下文是否匹配
            for edge in edges:
                source = edge[0] if isinstance(edge, list) else edge.get('source')
                for key in context:
                    if key == source:
                        probability = 0.7
                        break
    
    return {
        "probability": probability,
        "uncertainty": uncertainty,
        "expected_utility": probability * (1 - uncertainty)
    }


def log_action(action: str, context: Dict, pre_state: Dict) -> str:
    """
    记录行动
    
    Returns:
        action_id: 行动 ID
    """
    action_id = f"action_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    entry = {
        "action_id": action_id,
        "action": action,
        "context": context,
        "pre_state": pre_state,
        "timestamp": datetime.now().isoformat()
    }
    
    CAUSAL_DIR.mkdir(parents=True, exist_ok=True)
    with open(ACTION_LOG, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    return action_id


def log_outcome(action_id: str, outcome: str, post_state: Dict) -> bool:
    """
    记录结果
    
    Args:
        action_id: 行动 ID
        outcome: 结果 ("positive", "negative", "neutral")
        post_state: 行动后状态
        
    Returns:
        bool: 是否成功
    """
    if not ACTION_LOG.exists():
        return False
    
    actions = []
    with open(ACTION_LOG, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                try:
                    actions.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    
    for entry in actions:
        if entry.get('action_id') == action_id:
            entry['outcome'] = outcome
            entry['post_state'] = post_state
            entry['outcome_timestamp'] = datetime.now().isoformat()
            
            with open(ACTION_LOG, 'w', encoding='utf-8') as f:
                for e in actions:
                    f.write(json.dumps(e, ensure_ascii=False) + '\n')
            return True
    
    return False


def read_action_log() -> List[Dict]:
    """读取行动日志"""
    if not ACTION_LOG.exists():
        return []
    
    actions = []
    with open(ACTION_LOG, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                try:
                    actions.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return actions


def query_pattern(treatment: str, outcome: str) -> Dict:
    """
    查询因果模式
    
    Returns:
        Dict with estimates and confidence
    """
    return {
        "treatment": treatment,
        "outcome": outcome,
        "estimates": {},
        "confidence": 0.5,
        "sample_size": 0
    }


def debug_failure(action_id: str) -> Dict:
    """
    调试失败原因
    
    Returns:
        Dict with root_cause, chain, recommendations
    """
    actions = read_action_log()
    
    for entry in actions:
        if entry.get('action_id') == action_id:
            return {
                "action_id": action_id,
                "root_cause": "需分析因果链",
                "chain": [],
                "recommendations": ["检查因果图配置", "收集更多数据"]
            }
    
    return {"error": "Action not found"}


def get_stats() -> Dict:
    """获取统计信息"""
    actions = read_action_log()
    return {
        "total_actions": len(actions),
        "positive_outcomes": sum(1 for a in actions if a.get('outcome') == 'positive'),
        "negative_outcomes": sum(1 for a in actions if a.get('outcome') == 'negative'),
    }


if __name__ == "__main__":
    print("🧪 Testing Causal Inference Protocol...")
    
    # 1. 预测
    pred = predict("send_email", {"recipient_type": "warm_lead"})
    print(f"✅ 预测: {pred}")
    
    # 2. 记录行动
    aid = log_action(
        action="send_email",
        context={"recipient": "test@company.com"},
        pre_state={"days_since_contact": 7}
    )
    print(f"✅ 行动已记录: {aid}")
    
    # 3. 记录结果
    log_outcome(aid, "positive", {"reply_received": True, "reply_hours": 4})
    print(f"✅ 结果已记录")
    
    # 4. 统计
    stats = get_stats()
    print(f"✅ 统计: {stats}")
