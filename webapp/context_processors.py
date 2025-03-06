import pickle
import os

def theme_processor(request):
    if request.user.is_authenticated:
        user_prefs_file = f"user_data/{request.user.username}_prefs.pickle"
        if os.path.exists(user_prefs_file):
            with open(user_prefs_file, "rb") as f:
                preferences = pickle.load(f)
        else:
            preferences = {"theme": "light"}
    else:
        preferences = {"theme": "light"}

    return {"preferences": preferences}
