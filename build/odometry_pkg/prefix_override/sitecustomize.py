import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
<<<<<<< HEAD
    sys.prefix = sys.exec_prefix = '/home/darhf/Manchester/Week10/odometry/install/odometry_pkg'
=======
    sys.prefix = sys.exec_prefix = '/home/darhf/Manchester/Week10/odometry_pkg/install/odometry_pkg'
>>>>>>> d34c3ea (Cambio de paquete)
