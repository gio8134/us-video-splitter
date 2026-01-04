import threading
from CoreThread import CoreThread

# Create thread objects
t1 = CoreThread("t1", "ori.mp4")

# Start threads
t1.start()

# Wait for threads to complete
t1.join()

print("All threads finished")