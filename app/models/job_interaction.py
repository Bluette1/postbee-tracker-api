from flask_pymongo import PyMongo
from datetime import datetime

mongo = PyMongo()

class JobInteraction:
    def __init__(
        self,
        user_id,
        job_id,
        is_pinned=False,
        is_saved=False,
        follow_up_data=None,
        has_follow_up=False,
        view_count=0,
        last_viewed=None,
    ):
        self.user_id = user_id
        self.job_id = job_id
        self.is_pinned = is_pinned
        self.is_saved = is_saved
        self.follow_up_data = follow_up_data
        self.has_follow_up = has_follow_up
        self.view_count = view_count
        self.last_viewed = last_viewed
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "job_id": self.job_id,
            "is_pinned": self.is_pinned,
            "is_saved": self.is_saved,
            "follow_up_data": self.follow_up_data,
            "has_follow_up": self.has_follow_up,
            "view_count": self.view_count,
            "last_viewed": self.last_viewed.isoformat() if self.last_viewed else None,
            "updated_at": self.updated_at.isoformat(),
        }

    def save(self):
        """Save the current instance to the database."""
        mongo.db.job_interactions.insert_one(self.to_dict())

    def update(self):
        """Update the existing interaction in the database."""
        mongo.db.job_interactions.update_one(
            {"user_id": self.user_id, "job_id": self.job_id},
            {"$set": self.to_dict()}
        )

    @classmethod
    def find(cls, user_id, job_id):
        """Find a specific interaction."""
        interaction_data = mongo.db.job_interactions.find_one({"user_id": user_id, "job_id": job_id})
        if interaction_data:
            return cls(**interaction_data)
        return None