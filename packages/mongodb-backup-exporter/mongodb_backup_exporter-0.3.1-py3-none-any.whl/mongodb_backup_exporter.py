import os
import json
import subprocess
from pymongo import MongoClient

class MongoDBBackupExporter:

    def __init__(self, username, password, hostname, db_name, mongoexport_path, output_format=None, json_list=False, pretty_json=False, output_dir=None, collections_to_export=None):
        """
        Initializes the MongoDBBackupExporter with the necessary connection details and output format.

        Args:
            username (str): The username for authenticating with the MongoDB database.
            password (str): The password for authenticating with the MongoDB database.
            hostname (str): The hostname or IP address of the MongoDB server.
            db_name (str): The name of the database to be exported.
            mongoexport_path (str): The file path to the mongoexport executable used for exporting data.
            output_format (str, optional): The format of the output files. Accepts 'json' or 'csv'. Defaults to 'json' if not specified.
            json_list (bool, optional): If True, each JSON object will be written on a new line, creating a list format. Defaults to False.
            pretty_json (bool, optional): If True, the JSON output will be formatted with indentation for better readability. Defaults to False.
            output_dir (str, optional): The directory where output files will be saved. If None, defaults to a directory named after the database in the current working directory.
            collections_to_export (list, optional): A list of collection names to be exported. If None, all collections in the database will be exported.

        Attributes:
            username (str): Stores the username for MongoDB.
            password (str): Stores the password for MongoDB.
            hostname (str): Stores the hostname of the MongoDB server.
            db_name (str): Stores the name of the database.
            output_format (str): Stores the output format ('json' or 'csv').
            json_list (bool): Determines if the output should be in list format for JSON.
            pretty_json (bool): Determines if the JSON output should be prettified.
            mongoexport_path (str): Stores the path to the mongoexport executable.
            output_dir (str): Stores the directory for saving exported files.
            collections_to_export (list): Stores the list of collections to be exported.
        """
        self.username = username
        self.password = password
        self.hostname = hostname
        self.db_name = db_name
        self.output_format = str(output_format).lower() if str(output_format).lower() in ['json', 'csv'] else 'json'
        self.json_list = json_list
        self.pretty_json = pretty_json
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

 
    def write_json_file(self, json_data, output_file):
        """
        Writes JSON data to a file, either in a pretty format or as a list of JSON objects.

        Args:
            json_data (list): List of JSON objects to write to the file.
            output_file (str): Path to the output file.
        """
        with open(output_file, 'w', encoding='utf-8') as file:
            if self.pretty_json:
                json.dump(json_data, file, indent=4)  # Pretty print with indentation
                print(f"Pretty JSON output saved to {output_file}")
            else:
                # Write each JSON object on a new line in a list format
                with open(output_file, 'w', encoding='utf-8') as file:
                                file.write('[\n')
                                for idx, doc in enumerate(json_data):
                                    json.dump(doc, file)
                                    if idx < len(json_data) - 1:
                                        file.write(',\n')  # Add a comma between objects
                                    else:
                                        file.write('\n')
                                file.write(']\n')
                print(f"Regular JSON List output saved to {output_file}")


    def export_collection(self, collection_name):
        """
        Exports a specified collection from MongoDB to a file in the specified format.
        
        Args:
            collection_name (str): The name of the collection to export.
            
        This function builds the mongoexport command based on the specified output format.
        If the output format is 'csv', it retrieves the field names from the first document
        in the collection and adds them to the command. The exported file is saved in the
        specified output directory with the collection name and appropriate file extension.
        If the output format is 'json' and json_list is set to True, it processes each line
        of the output as a separate JSON object.
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

            if self.output_format == "json" and self.json_list:
                with open(output_file, 'r', encoding='utf-8') as file:
                    json_data = [json.loads(line) for line in file]  # Read each line as JSON

                # Call the function to write the JSON data to the file
                self.write_json_file(json_data, output_file)

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