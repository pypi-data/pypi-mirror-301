import subprocess

system_message = """You respond only with Applescript code to achieve the users goal. You reply with NOTHING else— you just immediatly start writing Applescript code."""

class Siri:
    def __init__(self, computer):
        self.computer = computer

    def query(self, query):
        query = f"I need Applescript that does this: {query}"
        while True:
            applescript_code = self.computer.ai.chat(query, system_message=system_message, model_size="medium")
            
            # Remove leading and trailing backticks if present
            if applescript_code.startswith("```"):
                applescript_code = applescript_code.split("\n", 1)[1]
            if applescript_code.endswith("```"):
                applescript_code = applescript_code.rsplit("\n", 1)[0]
            applescript_code = applescript_code.strip()
        
            try:
                result = subprocess.run(['osascript', '-e', applescript_code], capture_output=True, text=True, check=True)
                return result.stdout.strip()
            except subprocess.CalledProcessError as e:
                query += f"\n\nI wrote this AppleScript code:\n\n{applescript_code}\n\nBut I got this error:\n{e.stderr.strip()}\n\nPlease write new Applescript to help me achieve my goal."
                continue