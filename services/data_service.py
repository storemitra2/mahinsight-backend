import random
import datetime
from typing import List, Dict, Any
import numpy as np

VEHICLE_MODELS = ["Thar","Scorpio","XUV700","Bolero","ScorpioN"]
STATES = [
    'Maharashtra','Karnataka','Gujarat','Tamil Nadu','Rajasthan','Uttar Pradesh','West Bengal',
    'Andhra Pradesh','Telangana','Kerala','Punjab','Haryana','Bihar','Odisha','Madhya Pradesh'
]

def generate_social_media_samples(n: int = 15000) -> List[Dict[str, Any]]:
    samples = []
    for i in range(n):
        model = random.choices(VEHICLE_MODELS, weights=[0.25,0.2,0.2,0.15,0.2])[0]
        state = random.choices(STATES, weights=[3 if s in ['Maharashtra','Gujarat','Karnataka'] else 1 for s in STATES])[0]
        sentiment = random.choices(['positive','neutral','negative'], weights=[70,20,10])[0]
        text = f"User {i} about {model}: sample opinion ({sentiment})"
        samples.append({
            'id': f's_{i}',
            'text': text,
            'sentiment': sentiment,
            'vehicle_model': model,
            'state': state,
            'timestamp': (datetime.datetime.utcnow() - datetime.timedelta(days=random.randint(0,180))).isoformat()
        })
    return samples

def generate_sales_data(months: int = 6) -> List[Dict[str, Any]]:
    out = []
    start = datetime.date.today() - datetime.timedelta(days=30*months)
    for day in range(months * 30):
        d = start + datetime.timedelta(days=day)
        for region in ['North','South','East','West','Central']:
            for model in VEHICLE_MODELS:
                base = random.randint(10,200)
                # seasonal boost for festival months (assume Oct-Nov)
                if d.month in [10,11]:
                    base = int(base * 1.25)
                out.append({
                    'date': d.isoformat(),
                    'region': region,
                    'vehicle_model': model,
                    'units_sold': base,
                    'booking_count': int(base * random.uniform(1.0,1.5)),
                    'delivery_time': round(random.uniform(5,30),1),
                    'dealer_rating': round(random.uniform(3.5,4.9),2)
                })
    return out

def generate_heatmap_states() -> List[Dict[str, Any]]:
    out = []
    for s in STATES:
        buzz = random.randint(10,100)
        trending = random.choice(VEHICLE_MODELS)
        mentions = random.randint(50,2000)
        sentiment_score = random.randint(40,90)
        weekly_change = random.randint(-20,30)
        out.append({
            'state': s,
            'buzz_intensity': buzz,
            'trending_model': trending,
            'mentions': mentions,
            'sentiment_score': sentiment_score,
            'weekly_change': weekly_change
        })
    return out
