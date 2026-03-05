import os
import sys

print("Python version:", sys.version)
print("Python path:", sys.path)

# Try to import Django
try:
    import django
    print("Django version:", django.get_version())
    
    # Try to configure Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot_project.settings')
    django.setup()
    print("Django setup successful!")
    
    # Try to import models
    from chatbot_app.models import Conversation, Message, UserProfile
    print("Models imported successfully!")
    
    print("All tests passed!")
    
except Exception as e:
    print("Error:", str(e))
    import traceback
    traceback.print_exc()
