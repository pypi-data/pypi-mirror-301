import os
import subprocess
from pymongo import MongoClient

class MongoDBBackupExporter:
    def __init__(self, username, password, hostname, db_name, mongoexport_path, output_format=None, output_dir=None, collections_to_export=None):
        """
        Initializes the MongoDBBackupExporter with the necessary connection details and output format.

        Args:
            username (str): The username for the MongoDB database.
            password (str): The password for the MongoDB database.
            hostname (str): The cluster address for the MongoDB connection.
            db_name (str): The name of the database.
            mongoexport_path (str): The path to the mongoexport executable.
            output_format (str, optional): The format of the output files (either 'json' or 'csv'). Defaults to 'json'.
            output_dir (str, optional): The directory where output files will be saved. 
                                         If None, defaults to current working directory.
            collections_to_export (list, optional): A list of collection names to export. 
                                                    If None, all collections will be exported.
        """
        self.username = username
        self.password = password
        self.hostname = hostname
        self.db_name = db_name
        self.output_format = str(output_format).lower() if str(output_format).lower() in ['json','csv'] else 'json'
        self.mongoexport_path = mongoexport_path
        self.output_dir = output_dir or os.path.join(os.getcwd(), db_name)  # Use provided dir or default
        self.collections_to_export = collections_to_export

    def build_mongo_uri(self):
        """
        Builds the MongoDB connection URI.

        Returns:
            str: The complete MongoDB connection URI.
        """
        return f"mongodb+srv://{self.username}:{self.password}@{self.hostname}/{self.db_name}"

    def create_output_directory(self):
        """
        Creates the output directory for storing files if it doesn't already exist.
        """
        os.makedirs(self.output_dir, exist_ok=True)
        print(f"Output directory created or already exists: {self.output_dir}")

    def get_mongo_client(self):
        """
        Returns a MongoDB client connected to the specified URI.

        Returns:
            MongoClient: An instance of the MongoClient connected to the database.
        """
        return MongoClient(self.build_mongo_uri())

    def list_collections(self):
        """
        Lists all collections in the specified database.

        Returns:
            list: A list of collection names.
        """
        client = self.get_mongo_client()
        collections = client[self.db_name].list_collection_names()
        client.close()
        return collections

    def export_collection(self, collection_name):
        """
        Exports a specified collection from MongoDB to a file in the specified format.
        
        Args:
            collection_name (str): The name of the collection to export.
            
        The function builds the mongoexport command based on the specified output format.
        If the output format is 'csv', it retrieves the field names from the first document
        in the collection and adds them to the command. The exported file is saved in the
        specified output directory with the collection name and appropriate file extension.
        """
        output_file = os.path.join(self.output_dir, f"{collection_name}.{self.output_format}")
        
        # Initialize the MongoDB client
        client = MongoClient(self.build_mongo_uri())
        db = client[self.db_name]
        collection = db[collection_name]
        
        # Build the base command for mongoexport
        command = [
            self.mongoexport_path,
            "--uri", self.build_mongo_uri(),
            "--collection", collection_name,
            "--out", output_file,
            "--type", self.output_format
        ]

        # If the format is CSV, retrieve the fields
        if self.output_format == "csv":
            # Retrieve field names from the first document
            fields = collection.find_one().keys()
            fields_list = ','.join(fields)  # Create a comma-separated string of fields
            
            command += ["--fields", fields_list]

        try:
            subprocess.run(command, check=True)
            print(f"Export of collection '{collection_name}' completed: {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error exporting collection '{collection_name}': {e}")
        finally:
            client.close()  # Ensure the connection is closed


    def export_all_collections(self):
        """
        Exports all specified collections to files in the specified format.
        If no collections are specified, it exports all collections in the database.
        Additionally, it prints the total number of documents and size in MB for each collection.
        """
        self.create_output_directory()
        client = self.get_mongo_client()
        
        collections = self.collections_to_export or self.list_collections()  # Use provided collections or list all
        
        # Inform about the collections to be exported
        print(f"Collections to export: {collections}")

        for collection in collections:
            # Get stats for the collection
            stats = client[self.db_name].command("collStats", collection)
            size_in_mb = stats['size'] / (1024 * 1024)  # Size in MB
            total_documents = stats['count']  # Total number of documents

            # Print the collection details
            print(f"Collection: {collection}, Total documents: {total_documents}, Size: {size_in_mb:.2f} MB")

            # Export the collection
            self.export_collection(collection)

        client.close()


    def execute_export(self):
        """
        Executes the export process for all collections if none are provided,
        or for the specified collections.
        """
        if self.collections_to_export is None:
            print("No collections specified; exporting all collections.")
        else:
            print(f"Exporting specified collections: {self.collections_to_export}")
        
        self.export_all_collections()
