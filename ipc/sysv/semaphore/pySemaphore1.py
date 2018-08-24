#!/usr/bin/env python3

import sysv_ipc
import os
import random
import signal
import sys
import time

SEM_KEY = 1024
semaphore = None


def signal_handler(signum, frame):
	global semaphore
	print('File ', __file__, ': Signal handler called with signal', signum)
	if semaphore:
		semaphore.remove()
	sys.exit(0)


def main():
	global semaphore
	print('Python: ', __file__, ' PID: ', os.getpid())

	signal.signal(signal.SIGINT, signal_handler)
	signal.signal(signal.SIGUSR1, signal_handler)

	semaphore = sysv_ipc.Semaphore(SEM_KEY, sysv_ipc.IPC_CREX, initial_value=1)

	while True:
		semaphore.acquire()
		
		print('')
		print('Lock ', __file__, '...')

		sec_sleep = random.randint(1, 5)
		print('Sleep: ', sec_sleep)
		time.sleep(sec_sleep)

		semaphore.release()
		print('Unock ', __file__, '...')
		print('')


if __name__ == '__main__':
	main()
