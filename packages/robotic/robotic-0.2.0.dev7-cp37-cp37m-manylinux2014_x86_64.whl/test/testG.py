import robotic as ry
import sys 
try:
    C = ry.Config()
    C.watchFile("giraffehd.g")
except KeyboardInterrupt:
    sys.exit(1)