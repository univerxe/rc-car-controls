import cv2
import serial # serial.Serial ser
import numpy as np
import time

def connect_to_arduino(port, baud_rate=9600, simulate=False): 
    if simulate:
        return None
    try:
        return serial.Serial(port, baud_rate)
    except serial.SerialException as e:
        print(f"Failed to connect on {port}: {e}")
        exit(1)
        
def send_command(ser, command):
    if ser is None:
        print(f"Simulated command: {command}")  # simulation 
        return
    try:
        ser.write((command + '\n').encode())  # arduino 
        print(f"Sent '{command}' to Arduino")
    except serial.SerialException as e:
        print(f"Error sending data: {e}")
        exit(1)  

def draw_centroid_and_edges(ser, frame, target_color, tolerance, prev_area=0, area_change_threshold=200):
    # Convert the frame BGR to HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 
    
    # Define the lower and upper bounds for the target color in HSV space (0-255)
    lower_color = (target_color[0] - tolerance, 100, 100) #100
    upper_color = (target_color[0] + tolerance, 255, 255) #255
    
    # Create a mask that isolates the target color
    mask = cv2.inRange(hsv_frame, lower_color, upper_color)
    
    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter the contours to find squares (4-sided polygons)
    squares = [cnt for cnt in contours if cv2.approxPolyDP(cnt, 0.04 * cv2.arcLength(cnt, True), True).shape[0] == 4]
    
    if squares:
        # Find the largest square based on contour area
        largest_square = max(squares, key=cv2.contourArea)
        current_area = cv2.contourArea(largest_square)
        
        # Calculate the moments of the largest square
        M = cv2.moments(largest_square)
        
        if M["m00"] != 0:
            # Calculate the centroid of the square
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            
            # Draw a circle at the centroid on the frame
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

            # Determine the frame width and margins for left and right commands
            frame_width = frame.shape[1]
            left_margin = frame_width * 0.20  # 20% of frame width
            right_margin = frame_width * 0.80  # 80% of frame width

            # Control logic based on area and centroid position
            if current_area < 25000:
                send_command(ser, "forward")  
            else:
                send_command(ser, "stop")  

            # Send "left" or "right" commands based on the centroid's x-coordinate
            if cx <= left_margin:
                send_command(ser, "left") 
            elif cx >= right_margin:
                send_command(ser, "right")  
                
        return frame, current_area  
    return frame, prev_area  

def track_and_control(port='COM11', simulate=False):
    ser = connect_to_arduino(port, simulate=simulate)
    cap = cv2.VideoCapture(0)  
    width = 640
    height = 480
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    fps = 5
    frame_delay = 1 / fps
    
    # Define the HSV color range for tracking
    target_color = (30, 255, 255)  # HSV color for yellow
    tolerance = 30  # Tolerance for color detection

    prev_area = 0  # Initialize previous area to 0
    area_change_threshold = 100  # Define your threshold here for stopping condition

    while True:
        start_time = time.time()
    
        ret, frame = cap.read()
        if not ret:
            print("Error: Cannot receive frame (stream end?). Exiting...")
            break

        # Correctly pass all the required arguments including 'ser'
        frame, prev_area = draw_centroid_and_edges(ser, frame, target_color, tolerance, prev_area, area_change_threshold)
        cv2.imshow('Object Tracking', frame)

        # Calculate the time taken to process the frame and add delay to match the desired FPS
        elapsed_time = time.time() - start_time
        delay = max(0, frame_delay - elapsed_time)
        time.sleep(delay)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    if not simulate:
        ser.close()

if __name__ == "__main__":
    track_and_control(simulate=True)  #simulation (False == Arduino)