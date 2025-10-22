import tweepy
from typing import List, Dict, Any
from config import OPENAI_API_KEY
import random
from datetime import datetime, timedelta


class TwitterService:
    def __init__(self, bearer_token: str = None):
        self.client = None
        if bearer_token:
            try:
                self.client = tweepy.Client(bearer_token=bearer_token)
            except Exception:
                self.client = None

    def clean_text(self, t: str) -> str:
        return t.replace('\n', ' ').strip()

    def get_mahindra_tweets(self, max_results: int = 100) -> List[Dict[str, Any]]:
        if self.client:
            try:
                tweets = self.client.search_recent_tweets(
                    query="(Mahindra OR Thar OR Scorpio OR XUV700) -is:retweet",
                    max_results=max_results,
                    tweet_fields=["created_at", "author_id", "text"]
                )
                return [
                    {
                        "text": t.text,
                        "created_at": t.created_at,
                        "author_id": t.author_id,
                        "source": "twitter"
                    }
                    for t in (tweets.data or [])
                ]
            except Exception:
                # fall through to mock
                pass

        return self._generate_mock_tweets(max_results)

    def _generate_mock_tweets(self, count: int) -> List[Dict[str, Any]]:
        positive_templates = [
            "Just bought the new Mahindra {model}! Absolutely loving the {feature} 🔥",
            "Mahindra {model} is a beast on Indian roads! {feature} is amazing 💪",
            "Test drove {model} today - mind blown! Mahindra is killing it 🚀",
            "{model} is worth every penny! The {feature} is exceptional 👌"
        ]

        negative_templates = [
            "Disappointed with Mahindra {model} service. {issue} needs fixing 😞",
            "{model} has some issues with {issue}. Hope Mahindra addresses this soon.",
            "Expected better from Mahindra {model}. The {issue} is problematic."
        ]

        neutral_templates = [
            "Saw the new Mahindra {model} on road today. Looks decent.",
            "Considering buying {model}. Any owners here with experience?",
            "Mahindra {model} vs {competitor} - which one to choose?"
        ]

        models = ["Thar", "Scorpio", "XUV700", "Bolero", "XUV400"]
        features = ["design", "performance", "comfort", "tech features", "off-road capability"]
        issues = ["mileage", "service", "price", "delivery", "quality"]
        competitors = ["Tata Safari", "Hyundai Creta", "MG Hector"]

        tweets = []
        for i in range(count):
            template = random.choice(positive_templates + negative_templates + neutral_templates)
            tweet_text = template.format(
                model=random.choice(models),
                feature=random.choice(features),
                issue=random.choice(issues),
                competitor=random.choice(competitors)
            )

            tweets.append({
                "text": tweet_text,
                "created_at": datetime.now() - timedelta(hours=random.randint(1, 168)),
                "author_id": f"user_{random.randint(10000, 99999)}",
                "source": "twitter_mock"
            })

        return tweets

