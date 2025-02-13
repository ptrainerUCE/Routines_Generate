class RoutinesRepository:
    """
    Repository for routines stored in CouchDB.
    """

    def __init__(self, server):
        """
        Initializes the repository with a CouchDB server.

        :param server: The CouchDB server instance.
        """
        self.server = server
        self.db_name = "ptrainer_user_routine"  # Name of the database for routines
        self._ensure_database_exists()

    def _ensure_database_exists(self):
        """
        Ensures the database exists in CouchDB.
        """
        if self.db_name not in self.server:
            self.server.create(self.db_name)

    def save_routine(self, user_id: int, routine_data: dict):
        """
        Save or update a routine for a specific user in CouchDB.

        :param user_id: The ID of the user owning the routine.
        :param routine_data: A dictionary representing the routine data.
        :return: A tuple (id, rev) with the CouchDB document ID and revision.
        """
        db = self.server[self.db_name]
        routine_data["_id"] = str(user_id)  # Use the user ID as the document ID
        try:
            # Check if the document already exists (handle updates)
            if str(user_id) in db:
                existing_doc = db[str(user_id)]
                routine_data["_rev"] = existing_doc["_rev"]  # Add revision for update

            # Save document (insert new or update existing) and return the response
            response = db.put(routine_data)
            print(f"Routine saved successfully for user {user_id}: {response}")  # Debugging
            return response  # This should return a tuple (id, rev)
        except Exception as e:
            print(f"Error saving routine for user {user_id}: {e}")  # Log the actual error
            raise e  # Re-raise the exception to surface it properly
