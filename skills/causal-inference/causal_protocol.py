"""
Causal Inference Protocol Implementation

Manual causal reasoning and outcome prediction.
Usage:
    python3 causal_protocol.py predict send_email recipient_type=warm
    python3 causal_protocol.py log send_email context='{}' pre_state='{}'
    python3 causal_protocol.py outcome action_id outcome=positive post_state='{}'
    python3 causal_protocol.py query send_time reply_probability
    python3 causal_protocol.py stats
"""

import json
import sys
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional


# 配置路径
CAUSAL_DIR = Path("~/.openclaw/workspace/memory/causal").expanduser()
ACTION_LOG = CAUSAL_DIR / "action_log.jsonl"
CONFIG_FILE = CAUSAL_DIR / "config.yaml"
GRAPHS_DIR = CAUSAL_DIR / "graphs"
ESTIMATES_DIR = CAUSAL_DIR / "estimates"


def _ensure_dirs():
    """确保目录存在"""
    CAUSAL_DIR.mkdir(parents=True, exist_ok=True)
    GRAPHS_DIR.mkdir(parents=True, exist_ok=True)
    ESTIMATES_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> Dict:
    """加载配置文件"""
    _ensure_dirs()
    if CONFIG_FILE.exists():
        import yaml
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            cfg = yaml.safe_load(f)
            return cfg or {}
    return {}


def save_config(config: Dict):
    """保存配置"""
    _ensure_dirs()
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
    _ensure_dirs()
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
            cfg = yaml.safe_load(f)
            if cfg:
                # 获取 edges
                domain_data = list(cfg.values())[0] if cfg else {}
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
        "expected_utility": round(probability * (1 - uncertainty), 2)
    }


def log_action(action: str, context: Dict, pre_state: Dict) -> str:
    """
    记录行动
    
    Returns:
        action_id: 行动 ID
    """
    _ensure_dirs()
    action_id = f"action_{uuid.uuid4().hex[:12]}"
    
    entry = {
        "action_id": action_id,
        "action": action,
        "context": context,
        "pre_state": pre_state,
        "timestamp": datetime.now().isoformat()
    }
    
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
    
    updated = False
    for entry in actions:
        if entry.get('action_id') == action_id:
            entry['outcome'] = outcome
            entry['post_state'] = post_state
            entry['outcome_timestamp'] = datetime.now().isoformat()
            updated = True
            break
    
    if updated:
        # 原子写入：先写临时文件
        temp_file = ACTION_LOG.with_suffix('.tmp')
        with open(temp_file, 'w', encoding='utf-8') as f:
            for e in actions:
                f.write(json.dumps(e, ensure_ascii=False) + '\n')
        temp_file.replace(ACTION_LOG)
    
    return updated


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
    _ensure_dirs()
    
    est_file = ESTIMATES_DIR / f"{treatment}_{outcome}.json"
    
    if est_file.exists():
        with open(est_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    return {
        "treatment": treatment,
        "outcome": outcome,
        "estimates": {},
        "confidence": 0.5,
        "sample_size": 0,
        "note": "No historical data yet"
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
                "action": entry.get('action'),
                "context": entry.get('context'),
                "outcome": entry.get('outcome'),
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
        "neutral_outcomes": sum(1 for a in actions if a.get('outcome') == 'neutral'),
        "pending": sum(1 for a in actions if not a.get('outcome'))
    }


def cli():
    """命令行接口"""
    _ensure_dirs()
    
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    cmd = sys.argv[1]
    
    if cmd == "predict" and len(sys.argv) >= 4:
        action = sys.argv[2]
        # 解析 context: key=value
        context = {}
        for arg in sys.argv[3:]:
            if '=' in arg:
                k, v = arg.split('=', 1)
                context[k] = v
        result = predict(action, context)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif cmd == "log" and len(sys.argv) >= 5:
        action = sys.argv[2]
        context = json.loads(sys.argv[3]) if sys.argv[3] else {}
        pre_state = json.loads(sys.argv[4]) if sys.argv[4] else {}
        aid = log_action(action, context, pre_state)
        print(f"Action ID: {aid}")
    
    elif cmd == "outcome" and len(sys.argv) >= 5:
        action_id = sys.argv[2]
        outcome = sys.argv[3]
        if outcome not in ("positive", "negative", "neutral"):
            print("Error: outcome must be positive/negative/neutral")
            return
        post_state = json.loads(sys.argv[4]) if sys.argv[4] else {}
        success = log_outcome(action_id, outcome, post_state)
        print(f"Updated: {success}")
    
    elif cmd == "query" and len(sys.argv) >= 4:
        treatment = sys.argv[2]
        outcome = sys.argv[3]
        result = query_pattern(treatment, outcome)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif cmd == "stats":
        stats = get_stats()
        print(json.dumps(stats, indent=2, ensure_ascii=False))
    
    elif cmd == "debug" and len(sys.argv) >= 3:
        result = debug_failure(sys.argv[2])
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    else:
        print(__doc__)


if __name__ == "__main__":
    cli()
