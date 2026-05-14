import math
from dataclasses import dataclass
from typing import List

@dataclass
class BurstPoint:
    """熱狂の座標を定義するオープン版データ構造"""
    peak_sec: int        # 熱狂の頂点（秒）
    in_sec: int          # 固定バッファによる遡行開始地点
    out_sec: int         # 固定バッファによる終了地点
    score: float         # 標準偏差ベースの重要度スコア
    level: str           # ULTRA / HIGH / LOW

class ClippeaksCore:
    """
    Clippeaks Core — Multi-Window SMA Time-Series Engine (Open Edition)
    
    6つの時間窓（5s, 10s, 15s, 30s, 60s, 120s）の加重移動平均（SMA）を用いて、
    時系列イベントログからバーストポイントを検出する統計解析エンジン。
    """

    def __init__(self, multiplier: float = 3.0, context_before: int = 15, context_after: int = 10):
        self.multiplier = multiplier
        self.context_before = context_before
        self.context_after = context_after
        self.windows = [5, 10, 15, 30, 60, 120]
        self.weights = [0.30, 0.22, 0.18, 0.14, 0.10, 0.06]

    def analyze(self, raw_counts: List[int]) -> List[BurstPoint]:
        """
        時系列ストリームから相対的な盛り上がり地点を抽出。
        ※本オープン版では、単一ストリーム（Row Count）の解析に特化しています。
        """
        if not raw_counts:
            return []

        # Step 1: Multi-Window SMA Composite
        composite = [0.0] * len(raw_counts)
        for w, weight in zip(self.windows, self.weights):
            for i in range(len(raw_counts)):
                start = max(0, i - w + 1)
                sma = sum(raw_counts[start:i+1]) / (i - start + 1)
                composite[i] += sma * weight

        # Step 2: Dynamic Threshold & Scoring
        mean_val = sum(composite) / len(composite)
        variance = sum((x - mean_val) ** 2 for x in composite) / len(composite)
        std_val = math.sqrt(variance) if variance > 0 else 1.0
        threshold = mean_val + (self.multiplier * std_val)

        # Step 3: Emit Coordinates
        points = []
        for i, val in enumerate(composite):
            if val > threshold:
                score = (val - threshold) / std_val
                
                # オープン版仕様：一律の固定窓によるIN/OUT生成
                in_sec = max(0, i - self.context_before)
                out_sec = min(len(raw_counts) - 1, i + self.context_after)
                
                points.append(BurstPoint(
                    peak_sec=i,
                    in_sec=in_sec,
                    out_sec=out_sec,
                    score=round(score, 1),
                    level="ULTRA" if score > 50 else "HIGH" if score > 25 else "LOW"
                ))

        return sorted(points, key=lambda p: p.score, reverse=True)