from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy
from datetime import datetime

# Server class to handle client requests
class NoteServer:
    def __init__(self):
        # Initialize the notes database as an empty dictionary
        self.notes = {}

    # Method to add a note to the database
    def add_note(self, topic, text):
        try:
            # Get the current timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Check if the topic already exists in the notes database
            if topic in self.notes:
                # Append the new note to the existing topic
                self.notes[topic].append((timestamp, text))
            else:
                # Create a new topic with the note
                self.notes[topic] = [(timestamp, text)]
            # Return a message indicating the note has been added
            return "Note added."
        except Exception as e:
            # Handle any unexpected errors and return an error message
            return f"Error adding note: {str(e)}"

    # Method to retrieve notes for a given topic from the database
    def get_notes(self, topic):
        try:
            # Check if the topic exists in the notes database
            if topic in self.notes:
                # Return the notes for the given topic
                return self.notes[topic]
            else:
                # Return a message indicating no notes were found for the given topic
                return "No notes found."
        except Exception as e:
            # Handle any unexpected errors and return an error message
            return f"Error retrieving notes: {str(e)}"

# Function to start the server
def server():
    try:
        # Initialize the XML-RPC server instance on localhost at port 8000
        server = SimpleXMLRPCServer(('localhost', 8000))
        # Register the NoteServer instance with the XML-RPC server
        server.register_instance(NoteServer())
        # Print a message indicating the server is running
        print("Server running...")
        # Start serving requests indefinitely
        server.serve_forever()
    except Exception as e:
        # Handle any unexpected errors and print an error message
        print(f"Server error: {str(e)}")

# Client class to interact with the server
class NoteClient:
    def __init__(self):
        try:
            # Create a ServerProxy to connect to the server's XML-RPC endpoint
            self.server = ServerProxy('http://localhost:8000')
        except Exception as e:
            # Handle connection errors and print an error message
            print(f"Connection error: {str(e)}")

    # Method to add a note using the server's add_note method
    def add_note(self, topic, text):
        try:
            # Call the add_note method exposed by the server
            return self.server.add_note(topic, text)
        except Exception as e:
            # Handle RPC call errors and print an error message
            return f"Error adding note: {str(e)}"

    # Method to retrieve notes for a given topic using the server's get_notes method
    def get_notes(self, topic):
        try:
            # Call the get_notes method exposed by the server
            return self.server.get_notes(topic)
        except Exception as e:
            # Handle RPC call errors and print an error message
            return f"Error retrieving notes: {str(e)}"

# Function to handle client actions
def client_menu():
    try:
        # Create a NoteClient instance to interact with the server
        client = NoteClient()

        # Display the client menu and handle user input
        while True:
            print("\nMenu:")
            print("1. Add a note")
            print("2. Get notes by topic")
            print("3. Exit")

            choice = input("Option: ")

            if choice == "1":
                # Prompt the user to enter a topic and text for the new note
                topic = input("Enter topic: ")
                text = input("Enter text: ")
                # Call the add_note method of the client
                response = client.add_note(topic, text)
                print(response)
            elif choice == "2":
                # Prompt the user to enter a topic to retrieve notes for
                topic = input("Enter topic: ")
                # Call the get_notes method of the client
                notes = client.get_notes(topic)
                # Print the retrieved notes or a message if no notes were found
                if isinstance(notes, str):
                    print(notes)
                else:
                    print("Notes for topic '{}':".format(topic))
                    for timestamp, text in notes:
                        print("Timestamp:", timestamp)
                        print("Text:", text)
            elif choice == "3":
                break
            else:
                print("Invalid option. Please try again.")
    except Exception as e:
        # Handle any unexpected errors and print an error message
        print(f"Client error: {str(e)}")

# Main function to start the client or server
if __name__ == "__main__":
    try:
        # Prompt the user to choose the role of the application (server or client)
        role = input("Choose role (server/client): ")
        if role.lower() == "server":
            server()  # Start the server
        elif role.lower() == "client":
            client_menu()   # Run the client menu
        else:
            print("Invalid role. Please choose either 'server' or 'client'.")
    except Exception as e:
        # Handle any unexpected errors and print an error message
        print(f"Main error: {str(e)}")
