import datetime
import copy

class SimpleVCS:
    """
    A simplified Version Control System (VCS) to demonstrate core concepts
    like committing changes, viewing history, and reverting to previous versions.
    """
    def __init__(self, project_name="My Project"):
        self.project_name = project_name
        self.working_copy = [] # Represents the current state of our "file" or project content
        self.history = []    # Stores committed versions (snapshots)
        self.commit_id_counter = 0

    def _get_current_state_snapshot(self):
        """Returns a deep copy of the current working copy to store in history."""
        return copy.deepcopy(self.working_copy)

    def add_line(self, line):
        """Adds a line to the current working copy, simulating a change to a file."""
        self.working_copy.append(line)
        print(f"[Working Copy] Added: '{line}'")

    def commit(self, message, author="Anonymous"):
        """Saves the current state of the working copy to history, like `git commit`."""
        self.commit_id_counter += 1
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_data = {
            "id": self.commit_id_counter,
            "author": author,
            "timestamp": timestamp,
            "message": message,
            "snapshot": self._get_current_state_snapshot() # Store a snapshot of the file
        }
        self.history.append(commit_data)
        print(f"\n--- Commit {self.commit_id_counter} by {author} ---")
        print(f"Message: '{message}'")
        print(f"Timestamp: {timestamp}")
        print("Current state committed.")
        self.show_current_state()

    def log(self):
        """Displays the commit history, similar to `git log`."""
        print(f"\n--- Commit History for {self.project_name} ---")
        if not self.history:
            print("No commits yet.")
            return

        for commit in self.history:
            print(f"Commit ID: {commit['id']}")
            print(f"Author: {commit['author']}")
            print(f"Date: {commit['timestamp']}")
            print(f"Message: '{commit['message']}'")
            print("--------------------")

    def revert(self, commit_id):
        """Reverts the working copy to a state of a specific commit ID, like `git revert` or `git reset`."""
        for commit in self.history:
            if commit['id'] == commit_id:
                self.working_copy = copy.deepcopy(commit['snapshot']) # Restore working copy
                print(f"\n--- Reverted to Commit ID: {commit_id} ---")
                print(f"Message: '{commit['message']}'")
                print("Working copy restored to this state.")
                self.show_current_state()
                return
        print(f"\nError: Commit ID {commit_id} not found.")

    def show_current_state(self):
        """Displays the current content of the working copy."""
        print(f"\n--- Current Working Copy for {self.project_name} ---")
        if not self.working_copy:
            print("[Empty]")
        else:
            for i, line in enumerate(self.working_copy):
                print(f"{i+1}: {line}")
        print("------------------------------------")

# --- Example Usage ---
if __name__ == "__main__":
    vcs = SimpleVCS("My First Git-like Project")

    # Initial work and commit
    vcs.add_line("Merhaba dünya!")
    vcs.add_line("Bu benim ilk satırım.")
    vcs.commit("Initial commit", "Alice") # Simulates `git commit -m "Initial commit"`

    # More work and another commit
    vcs.add_line("Yeni bir özellik ekliyorum.")
    vcs.commit("Added new feature", "Bob") # Another commit by a different author

    # Alice makes a change
    vcs.add_line("Alice'in yaptığı önemli bir değişiklik.")
    vcs.commit("Alice's important change", "Alice")

    # Bob makes a mistake or wants to add something else
    vcs.add_line("Yanlışlıkla eklenen bir satır.")
    vcs.show_current_state()

    # View the history
    vcs.log() # Simulates `git log`

    # Bob realizes the mistake and wants to go back to Alice's last commit (Commit ID 3)
    vcs.revert(3) # Simulates `git revert` or `git reset --hard` (simplified)

    # Now Bob adds the correct line
    vcs.add_line("Bob'un düzeltilmiş yeni satırı.")
    vcs.commit("Bob's corrected addition", "Bob")

    vcs.log()
    vcs.show_current_state()

    # Revert to the very first commit to see the project's initial state
    vcs.revert(1)
    vcs.show_current_state()
