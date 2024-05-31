import pygame
import socket
import time

# Define actions for each button and their corresponding integer values
def action_square():
    publish(1)

def action_cross():
    publish(2)

def action_circle():
    publish(3)

def action_triangle():
    publish(4)

def action_l1():
    publish(5)

def action_r1():
    publish(6)

def action_r3():
    publish(7)

def action_l3():
    publish(8)

def action_share():
    publish(9)

def action_options():
    publish(10)

def action_ps():
    publish(11)

def action_left_stick():
    publish(12)

def action_right_stick():
    publish(13)

def action_dpad_up():
    publish(14)

def action_dpad_down():
    publish(15)

def action_dpad_left():
    publish(16)

def action_dpad_right():
    publish(17)

# Map each button index to its corresponding action
button_actions = {
    0: action_cross,      # Cross button
    1: action_circle,     # Circle button
    2: action_square,     # Square button
    3: action_triangle,   # Triangle button
    4: action_share,      # Share button
    5: action_ps,         # PS button
    6: action_options,    # Options button
    7: action_l3,         # Left stick button
    8: action_r3,         # Right stick button
    9: action_l1,         # L1 button
    10: action_r1,        # R1 button
    11: action_dpad_up,   # DPAD Up
    12: action_dpad_down, # DPAD Down
    13: action_dpad_left, # DPAD Left
    14: action_dpad_right,# DPAD Right
}

# Function to publish integer values over a socket
def publish(value):
    client_socket.send(str(value).encode('utf-8'))
    print(f"Sent: {value}")

def action_joystick(joystick_name, direction):
    if joystick_name == "Left":
        if direction == "L_left":
            publish(18)
        elif direction == "L_right":
            publish(19)
        elif direction == "L_up":
            publish(20)
        elif direction == "L_down":
            publish(21)
    elif joystick_name == "Right":
        if direction == "R_left":
            publish(22)
        elif direction == "R_right":
            publish(23)
        elif direction == "R_up":
            publish(24)
        elif direction == "R_down":
            publish(25)

def main():
    # Initialize Pygame
    pygame.init()

    # Initialize the PS4 controller as a joystick
    pygame.joystick.init()
    joystick_count = pygame.joystick.get_count()

    if joystick_count < 1:
        print("No joystick connected.")
        return

    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print("Joystick name:", joystick.get_name())

    # Initialize the clock for controlling event loop frequency
    clock = pygame.time.Clock()

    # Create a socket object
    global client_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Get local machine name
    host = '127.0.0.1'
    port = 12331  # Port number
    
    # Bind to the port
    server_socket.bind((host, port))
    
    # Queue up to 5 requests
    server_socket.listen(5)
    
    print("Server waiting for connection...")
    
    # Establish a connection
    client_socket, addr = server_socket.accept()
    print("Got a connection from %s" % str(addr))
    print("Press R2 button as servo button to Jogg robot.")

    try:
        # Main loop to continuously read input from the controller
        while True:
            # Read axes values
            left_x = joystick.get_axis(0)
            left_y = joystick.get_axis(1)
            right_x = joystick.get_axis(2)
            right_y = joystick.get_axis(3)
            axis_5 = joystick.get_axis(5)  # Read axis 5 value

            if axis_5 > 0.5:  # Check if axis 5 is pressed
                # Determine direction for left joystick
                if left_x < -0.5:
                    action_joystick("Left", "L_left")
                elif left_x > 0.5:
                    action_joystick("Left", "L_right")
                if left_y < -0.5:
                    action_joystick("Left", "L_up")
                elif left_y > 0.5:
                    action_joystick("Left", "L_down")

                # Determine direction for right joystick
                if right_x < -0.5:
                    action_joystick("Right", "R_left")
                elif right_x > 0.5:
                    action_joystick("Right", "R_right")
                if right_y < -0.5:
                    action_joystick("Right", "R_up")
                elif right_y > 0.5:
                    action_joystick("Right", "R_down")

            # Read button events
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button in button_actions and axis_5 > 0.5:
                        print("Value published = ")
                        button_actions[event.button]()

            # Control the event loop frequency
            clock.tick(60)  # Adjust the argument as needed (e.g., 60 FPS)

    except KeyboardInterrupt:
        print("Server stopped.")
    finally:
        # Close the joystick
        joystick.quit()
        client_socket.close()
        server_socket.close()

if __name__ == "__main__":
    main()
