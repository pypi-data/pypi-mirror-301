import asyncio
import threading


def run_until_complete(coro):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # 在一个新的线程中运行一个单独的事件循环来执行协程
            return run_in_thread(coro)
        else:
            return loop.run_until_complete(coro)
    except RuntimeError:
        # 如果没有事件循环，则创建一个新的事件循环并运行协程
        return asyncio.run(coro)


def run_in_thread(coro):
    result = None
    exception = None

    def target():
        nonlocal result, exception
        try:
            result = asyncio.run(coro)
        except Exception as e:
            exception = e

    thread = threading.Thread(target=target)
    thread.start()
    thread.join()

    if exception:
        raise exception
    return result
