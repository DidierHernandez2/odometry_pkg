import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/darhf/Manchester/Week10/odometry/install/odometry_pkg'
