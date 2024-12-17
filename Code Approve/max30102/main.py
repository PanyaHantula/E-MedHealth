from heartrate_monitor import HeartRateMonitor
import time

print('sensor starting...')
#hrm = HeartRateMonitor(print_raw=args.raw, print_result=(not args.raw))
hrm = HeartRateMonitor()
hrm.run_sensor()
