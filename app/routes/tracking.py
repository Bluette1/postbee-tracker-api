from utils.auth import validate_token

@app.route('/api/track', methods=['POST'])
@validate_token
def track_interaction():
    user_id = request.user.get('user_id') 
    # Rest of your tracking logic