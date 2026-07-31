import logging
import time
from functools import wraps

logger = logging.getLogger("banderabot")


def log_handler(func):
    @wraps(func)
    async def wrapper(event, *args, **kwargs):
        start = time.perf_counter()

        try:
            result = await func(event, *args, **kwargs)

            elapsed = (time.perf_counter() - start) * 1000

            if hasattr(event, "text"):
                action = event.text
            elif hasattr(event, "data"):
                action = event.data
            else:
                action = "<unknown>"

            user = getattr(event, "from_user", None)

            logger.info(
                "✅ %s | %s (@%s | %s) | %s | %.1f ms",
                func.__name__,
                user.full_name if user else "-",
                user.username if user and user.username else "-",
                user.id if user else "-",
                action,
                elapsed,
            )

            return result

        except Exception:
            logger.exception(
                "❌ Exception in handler %s",
                func.__name__,
            )
            raise

    return wrapper