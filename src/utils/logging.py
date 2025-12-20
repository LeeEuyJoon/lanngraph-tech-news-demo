import functools
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)-8s] %(message)s [%(filename)s]",
    datefmt="%H:%M:%S",
)

logging.getLogger().setLevel(logging.INFO)

logger = logging.getLogger("node_logger")


def log_node_execution(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        node_name = func.__name__
        logger.info(f"[NODE START] {node_name}")

        start_time = time.perf_counter()
        try:
            result = func(*args, **kwargs)

            end_time = time.perf_counter()
            duration = end_time - start_time

            logger.info(f"[NODE END] {node_name} (소요 시간: {duration:.4f}s)")
            return result

        except Exception as e:
            logger.error(f"[NODE ERROR] {node_name} - {e}")
            raise e

    return wrapper
