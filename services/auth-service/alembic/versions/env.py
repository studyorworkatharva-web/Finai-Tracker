# ... alembic env.py template ...
# Add this line near other imports
from app.db.models.user import User
# Add this line in run_migrations_offline() and run_migrations_online()
# target_metadata = None
target_metadata = Base.metadata