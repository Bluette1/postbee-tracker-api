from flask_pymongo import PyMongo
from datetime import datetime
from bson.objectid import ObjectId
from app import mongo  # Import the global mongo instance


class JobInteraction:
    def __init__(
        self,
        user_id,
        job_id,
        is_pinned=False,
        is_saved=False,
        follow_up_data=None,
        has_follow_up=False,
        id=None,  # This will be used for the ObjectId
    ):
        self.id = id or ObjectId()  # Set the ObjectId
        self.user_id = user_id
        self.job_id = job_id
        self.is_pinned = is_pinned
        self.is_saved = is_saved
        self.follow_up_data = follow_up_data
        self.has_follow_up = has_follow_up
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "job_id": self.job_id,
            "is_pinned": self.is_pinned,
            "is_saved": self.is_saved,
            "follow_up_data": self.follow_up_data,
            "has_follow_up": self.has_follow_up,
            "updated_at": self.updated_at.isoformat(),
            "_id": self.id,  # Include _id in the dictionary
        }

    @classmethod
    def from_dict(cls, data):
        """Create a JobInteraction from a dictionary."""
        return cls(
            user_id=data["user_id"],
            job_id=data["job_id"],
            is_pinned=data.get("is_pinned", False),
            is_saved=data.get("is_saved", False),
            follow_up_data=data.get("follow_up_data"),
            has_follow_up=data.get("has_follow_up", False),
            id=data.get("_id"), 
        )

    def save(self):
        try:
            mongo.db.job_interactions.insert_one(self.to_dict())
        except Exception as e:
            print("Error saving JobInteraction:", e)
            raise

    def update(self):
        try:
            mongo.db.job_interactions.update_one(
                {"user_id": self.user_id, "job_id": self.job_id},
                {"$set": self.to_dict()},
            )
        except Exception as e:
            print("Error updating JobInteraction:", e)
            raise

    @classmethod
    def find(cls, user_id, job_id):
        try:
            interaction_data = mongo.db.job_interactions.find_one(
                {"user_id": user_id, "job_id": job_id}
            )
            if interaction_data:
                return cls.from_dict(interaction_data)
            return None
        except Exception as e:
            print("Error finding JobInteraction:", e)
            raise

    @classmethod
    def create_index(cls):
        """Create a unique index on user_id and job_id."""
        try:
            mongo.db.job_interactions.create_index(
                [("user_id", 1), ("job_id", 1)], unique=True
            )
            print("Unique index created on user_id and job_id.")
        except Exception as e:
            print("Error creating index:", e)
            raise
