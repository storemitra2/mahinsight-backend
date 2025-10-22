import os
import sys
from datetime import datetime, date
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from services.data_service import generate_social_media_samples, generate_sales_data, generate_heatmap_states
from database.database import SessionLocal, engine, Base
from models.user import User
from models.sentiment import Sentiment
from models.sales import Sales
from models.social_buzz import SocialBuzz
from models.executive_chat import ExecutiveChat
from models.topic import Topic

def populate():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Users (idempotent)
        existing_user = db.query(User).filter_by(email='demo@mahindra.com').first()
        if not existing_user:
            u = User(email='demo@mahindra.com', name='Demo User')
            db.add(u)
            db.commit()

        # Sentiments with normalized topics
        social = generate_social_media_samples(2000)
        topic_cache = {}
        for s in social:
            # naive topic extraction from text for demo
            candidate_topics = [w for w in ['design','mileage','service','safety','performance'] if w in s['text'].lower()]
            sent = Sentiment(text=s['text'], sentiment=s['sentiment'], confidence=0.9, summary=None, source='twitter', vehicle_model=s['vehicle_model'])
            db.add(sent)
            db.flush()
            # associate topics
            for tname in (candidate_topics or ['general']):
                t = topic_cache.get(tname)
                if not t:
                    t = db.query(Topic).filter_by(name=tname).first()
                    if not t:
                        t = Topic(name=tname)
                        db.add(t)
                        db.flush()
                    topic_cache[tname] = t
                sent.topics.append(t)


        # Sales
        sales = generate_sales_data(6)
        for s in sales:
            # ensure `date` is a Python date object (SQLite requires date objects)
            d = s.get('date')
            if isinstance(d, str):
                try:
                    d_obj = datetime.fromisoformat(d).date()
                except Exception:
                    # fallback: try parsing common YYYY-MM-DD
                    parts = d.split('-')
                    d_obj = date(int(parts[0]), int(parts[1]), int(parts[2]))
            else:
                d_obj = d
            db.add(Sales(region=s['region'], vehicle_model=s['vehicle_model'], units_sold=s['units_sold'], booking_count=s['booking_count'], delivery_time=s['delivery_time'], dealer_rating=s['dealer_rating'], date=d_obj))

        # Heatmap
        for h in generate_heatmap_states():
            db.add(SocialBuzz(state=h['state'], buzz_intensity=h['buzz_intensity'], trending_model=h['trending_model'], trending_topic=None, mentions=h['mentions']))

        db.commit()
        print('Demo DB populated')
    finally:
        db.close()

if __name__ == '__main__':
    populate()
