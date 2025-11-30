import psutil
import time

def monitor_cpu(threshold=80):
    """Continuously monitor CPU usage and alert if threshold is exceeded."""
    print("Monitoring CPU usage...")

    try:
        while True:
            cpu_usage = psutil.cpu_percent(interval=1)  # checks usage every 1 second
            
            if cpu_usage > threshold:
                print(f"Alert! CPU usage exceeds threshold: {cpu_usage}%")

    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")

    except Exception as e:
        print(f"An error occurred while monitoring CPU: {e}")


# ----------- Main Program Execution ------------- #

monitor_cpu(threshold=80)