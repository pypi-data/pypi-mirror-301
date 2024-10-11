import random
from .fun_facts import fun_facts
from .jokes import jokes

# Initialize a toggle variable to track the state
message_toggle = True


def get_random_message():
    global message_toggle
    if message_toggle:
        # Print a joke
        message = random.choice(jokes)
        message_toggle = False
    else:
        # Print a fun fact
        message = random.choice(fun_facts)
        message_toggle = True
    return message  # Return the message
