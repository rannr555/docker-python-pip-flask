import unittest
from multiprocessing import Queue, Process

def wrapper(q, fn, args):
    try:
        q.put(fn(*args))
    except BaseException as ex:
        q.put(ex)

def run_one_test(fn, should_block=False, args=(), timeout=1):
    q = Queue()
    p = Process(target=wrapper, args=(q, fn, args))
    p.start()
    p.join(timeout)
    msg = [q.get()] if not q.empty() else []
    if should_block and not p.is_alive():
        msg.append('Expected to block, but did not')
    elif not should_block and p.is_alive():
        msg.append('Blocked, but should have finished in under {} seconds'.format(timeout))
    if p.is_alive(): p.kill()
    return msg[0] if msg else None

class TodoTestCase(unittest.TestCase):
    def test_blocking(self):
        print("❌ test_blocking is running")
        self.assertEqual(1, 0)  # force fail

def case_blocking():
    from wallet import Wallet
    w = Wallet()
    w.change('deficit', 5)
    w.change('deficit', -7)
    return "this should fail"

if __name__ == "__main__":
    print("✅ Running tests via __main__")
    unittest.main()

