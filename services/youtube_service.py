import random
from typing import List, Dict, Any

def mock_comments(video_id: str, count: int = 50) -> List[Dict[str, Any]]:
    sample_models = ["Thar","Scorpio","XUV700","Bolero","ScorpioN"]
    out = []
    for i in range(count):
        m = random.choice(sample_models)
        sentiment = random.choices(['positive','neutral','negative'], weights=[65,25,10])[0]
        out.append({
            'id': f'c_{video_id}_{i}',
            'text': f"This is a comment about {m} - sentiment {sentiment}",
            'author': f'user_{random.randint(1,1000)}',
            'like_count': random.randint(0,200)
        })
    return out
