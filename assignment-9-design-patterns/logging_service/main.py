import os
import sys
import time
import threading
import random
from typing import List
from service.logger_factory import get_logger, LoggerFactory
from core.log_level import LogLevel

def simulate_user_activity(user_id: int, actions: List[str], duration: int = 10):
    logger = get_logger(f"user.{user_id}")
    start_time = time.time()
    logger.info(f"User {user_id} session started", user_id=user_id)
    
    try:
        while time.time() - start_time < duration:
            action = random.choice(actions)
            
            if action == "view":
                logger.debug(f"User {user_id} viewed a page", action=action, page_id=random.randint(1, 100))
            elif action == "click":
                logger.info(f"User {user_id} clicked on element", action=action, element_id=f"btn-{random.randint(1, 20)}")
            elif action == "purchase":
                logger.info(f"User {user_id} made a purchase", 
                           action=action, 
                           amount=round(random.uniform(10.0, 500.0), 2),
                           item_id=random.randint(1000, 9999))
            elif action == "error":
                try:
                    if random.random() < 0.3:
                        raise ValueError("Simulated validation error")
                    else:
                        raise KeyError("Simulated key not found")
                except Exception as e:
                    logger.error(f"Error during {action} for user {user_id}: {str(e)}", 
                                exc_info=True, 
                                action=action,
                                error_type=type(e).__name__)
            
            time.sleep(random.uniform(0.1, 0.5))
            
        logger.info(f"User {user_id} session ended", user_id=user_id, duration=round(time.time() - start_time, 2))

    except Exception as e:
        logger.exception(f"Unexpected error in user {user_id} simulation: {str(e)}")

def simulate_system_monitoring(duration: int = 15):
    logger = get_logger("system.monitor")
    logger.info("System monitoring started")
    start_time = time.time()
    iteration = 0
    
    try:
        while time.time() - start_time < duration:
            iteration += 1
            
            cpu_usage = random.uniform(10.0, 95.0)
            memory_usage = random.uniform(20.0, 85.0)
            disk_space = random.uniform(40.0, 95.0)
            
            logger.debug(f"System metrics - Iteration {iteration}", 
                        cpu=round(cpu_usage, 1), 
                        memory=round(memory_usage, 1), 
                        disk=round(disk_space, 1))
            
            if cpu_usage > 80:
                logger.warning(f"High CPU usage detected: {round(cpu_usage, 1)}%", 
                              metric="cpu", 
                              value=round(cpu_usage, 1),
                              threshold=80)
                
            if memory_usage > 75:
                logger.warning(f"High memory usage detected: {round(memory_usage, 1)}%", 
                              metric="memory", 
                              value=round(memory_usage, 1),
                              threshold=75)
                
            if disk_space > 90:
                logger.critical(f"Critical disk space usage: {round(disk_space, 1)}%", 
                               metric="disk", 
                               value=round(disk_space, 1),
                               threshold=90)
            
            time.sleep(1)
            
        logger.info("System monitoring completed", 
                   duration=round(time.time() - start_time, 2),
                   iterations=iteration)
                   
    except Exception as e:
        logger.exception(f"Error in system monitoring: {str(e)}")

def demonstrate_trace_logging():
    logger = get_logger("demo.trace")
    logger.set_level(LogLevel.TRACE)
    logger.trace("This is a trace message with very detailed information")
    logger.trace("Trace message with context data", 
               operation="initialization", 
               memory_address=hex(id(logger)),
               thread_id=threading.get_ident())

def demonstrate_context_logging():
    logger = get_logger("demo.context")
    request_id = f"req-{random.randint(10000, 99999)}"
    
    logger.info("Processing request started", 
               request_id=request_id, 
               client_ip="192.168.1.105",
               endpoint="/api/v1/users")
               
    start_time = time.time()
    time.sleep(0.3) 
    processing_time = time.time() - start_time
    
    logger.info("Request processed successfully", 
               request_id=request_id,
               duration_ms=round(processing_time * 1000, 2),
               status_code=200)


def main():
    root_logger = get_logger()
    root_logger.info("Application started")
    
    root_logger.debug("This is a debug message")
    root_logger.info("This is an info message")
    root_logger.warning("This is a warning message")
    root_logger.error("This is an error message")
    root_logger.critical("This is a critical message")
    
    try:
        numerator = 10
        denominator = 0
        result = numerator / denominator
    except Exception as e:
        root_logger.exception(f"An exception occurred: {str(e)}")
    
    demonstrate_trace_logging()
    
    demonstrate_context_logging()
    
    user_actions = ["view", "click", "purchase", "error"]
    user_threads = []
    for user_id in range(1, 4):
        thread = threading.Thread(
            target=simulate_user_activity,
            args=(user_id, user_actions, 5),
            name=f"UserThread-{user_id}"
        )
        user_threads.append(thread)
        thread.start()
    
    monitor_thread = threading.Thread(
        target=simulate_system_monitoring,
        args=(8,),
        name="MonitorThread"
    )
    monitor_thread.start()
    
    for thread in user_threads:
        thread.join()
    monitor_thread.join()
    
    root_logger.info("Application shutting down")
    
    LoggerFactory.shutdown_all()

if __name__ == "__main__":
    main()