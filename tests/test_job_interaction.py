from unittest import TestCase
from unittest.mock import patch, MagicMock
from webapp import create_app
from webapp.models.job_interaction import JobInteraction

class JobInteractionTestCase(TestCase):
    def setUp(self):
        self.app, self.celery = create_app()  # Unpack the app and celery
        self.app.config['TESTING'] = True  # Set testing mode 

        self.app_context = self.app.app_context()  # Create application context
        self.app_context.push()  # Push the app context

        self.user_id = "test_user"
        self.job_id = "test_job"
        self.interaction = JobInteraction(user_id=self.user_id, job_id=self.job_id)

    def tearDown(self):
        self.app_context.pop()  # Pop the app context after tests

    @patch('webapp.models.job_interaction.mongo')
    def test_save(self, mock_mongo):
        mock_mongo.db.job_interactions.insert_one.return_value = MagicMock()
        self.interaction.save()
        mock_mongo.db.job_interactions.insert_one.assert_called_once_with(self.interaction.to_dict())

    @patch('webapp.models.job_interaction.mongo')
    def test_update(self, mock_mongo):
        mock_mongo.db.job_interactions.update_one.return_value = MagicMock()
        self.interaction.update()
        mock_mongo.db.job_interactions.update_one.assert_called_once()

    @patch('webapp.models.job_interaction.mongo')
    def test_find(self, mock_mongo):
        mock_interaction_data = self.interaction.to_dict()
        mock_mongo.db.job_interactions.find_one.return_value = mock_interaction_data
        
        found_interaction = JobInteraction.find(self.user_id, self.job_id)
        self.assertEqual(found_interaction.user_id, self.user_id)
        self.assertEqual(found_interaction.job_id, self.job_id)

    @patch('webapp.models.job_interaction.mongo')
    def test_create_index(self, mock_mongo):
        mock_mongo.db.job_interactions.create_index.return_value = MagicMock()
        JobInteraction.create_index()
        mock_mongo.db.job_interactions.create_index.assert_called_once()

# Add more tests as necessary...