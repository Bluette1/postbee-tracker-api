from datetime import datetime

from bson.objectid import ObjectId
from flask import current_app

from webapp import mongo


class JobInteraction:
    def __init__(
        self,
        user_id,
        job_id,
        is_pinned=False,
        is_saved=False,
        follow_up_data=None,
        has_follow_up=False,
        id=None,
    ):
        self.id = id or ObjectId()
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
            "_id": self.id,
        }

    @classmethod
    def from_dict(cls, data):
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
        """Save the JobInteraction to the database."""
        try:
            mongo.db.job_interactions.insert_one(self.to_dict())
            self._log_info(
                "JobInteraction saved successfully for user_id: %s, job_id: %s",
                self.user_id,
                self.job_id,
            )
        except Exception as e:
            self._log_error("Error saving JobInteraction: %s", e)
            raise

    def update(self):
        """Update the JobInteraction in the database."""
        try:
            mongo.db.job_interactions.update_one(
                {"user_id": self.user_id, "job_id": self.job_id},
                {"$set": self.to_dict()},
            )
            self._log_info(
                "JobInteraction updated successfully for user_id: %s, job_id: %s",
                self.user_id,
                self.job_id,
            )
        except Exception as e:
            self._log_error("Error updating JobInteraction: %s", e)
            raise

    @classmethod
    def find(cls, user_id, job_id):
        """Find a JobInteraction by user_id and job_id."""
        try:
            interaction_data = mongo.db.job_interactions.find_one(
                {"user_id": user_id, "job_id": job_id}
            )
            if interaction_data:
                cls._log_info(
                    "JobInteraction found for user_id: %s, job_id: %s", user_id, job_id
                )
                return cls.from_dict(interaction_data)
            cls._log_info(
                "No JobInteraction found for user_id: %s, job_id: %s", user_id, job_id
            )
            return None
        except Exception as e:
            cls._log_error("Error finding JobInteraction: %s", e)
            raise

    @classmethod
    def create_index(cls):
        """Create a unique index on user_id and job_id."""
        try:
            mongo.db.job_interactions.create_index(
                [("user_id", 1), ("job_id", 1)], unique=True
            )
            cls._log_info("Unique index created on user_id and job_id.")
        except Exception as e:
            cls._log_error("Error creating index: %s", e)
            raise

    @classmethod
    def _log_info(cls, message, *args):
        """Log an info message."""
        logger = current_app.logger
        logger.info(message, *args)

    @classmethod
    def _log_error(cls, message, *args):
        """Log an error message."""
        logger = current_app.logger
        logger.error(message, *args)  # Correctly pass message and args to logger
