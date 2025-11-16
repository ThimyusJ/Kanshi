from commands import basic_commands

def route(intent: str):
    command_to_run = basic_commands.handle_intent(intent)
    if callable(command_to_run):
        #Run the command
        return command_to_run()
    return None