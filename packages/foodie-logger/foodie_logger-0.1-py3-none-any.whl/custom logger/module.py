from logger import get_logger

logger = get_logger(__name__)

def some_function():
    logger.info("Starting function.")
    
    try:
        # Your logic here
        logger.debug("Function logic running.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        logger.info("Function completed.")

some_function()