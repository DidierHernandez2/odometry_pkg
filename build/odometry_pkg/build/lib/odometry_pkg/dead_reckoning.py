import rclpy
import transforms3d
import numpy as np
import signal

from rclpy.node import Node
from std_msgs.msg import Float32
from nav_msgs.msg import Odometry
from rclpy.qos import qos_profile_sensor_data

def normalize_angle(angle):
    return np.arctan2(np.sin(angle), np.cos(angle))

class DeadReckoning(Node):
    def __init__(self):
        super().__init__('dead_reckoning')
        self.X = self.Y = self.Th = 0.0
        self._l, self._r = 0.18, 0.05
        self._sample_time = 0.01
        self.rate = 200.0
        self.first = True
        self.last_time = None
        self.v_r = self.v_l = 0.0
        self.odom_msg = Odometry()

        self.create_subscription(Float32, 'VelocityEncR', self.encR_callback, qos_profile_sensor_data)
        self.create_subscription(Float32, 'VelocityEncL', self.encL_callback, qos_profile_sensor_data)
        self.odom_pub = self.create_publisher(Odometry, 'odom', qos_profile_sensor_data)
        self.create_timer(1.0/self.rate, self.run)
        self.get_logger().info("DeadReckoning node iniciado.")

    def encR_callback(self, msg):
        self.v_r = msg.data * self._r

    def encL_callback(self, msg):
        self.v_l = msg.data * self._r

    def run(self):
        now = self.get_clock().now()
        if self.first:
            self.last_time = now
            self.first = False
            return
        dt = (now - self.last_time).nanoseconds * 1e-9
        if dt < self._sample_time:
            return
        V     = 0.5 * (self.v_r + self.v_l)
        Omega = (self.v_r - self.v_l) / self._l
        self.X  += V * np.cos(self.Th) * dt
        self.Y  += V * np.sin(self.Th) * dt
        self.Th = normalize_angle(self.Th + Omega * dt)
        self.last_time = now
        self.publish_odometry(V, Omega)

    def publish_odometry(self, V, Omega):
        q = transforms3d.euler.euler2quat(0, 0, self.Th)
        self.odom_msg.header.stamp            = self.get_clock().now().to_msg()
        self.odom_msg.header.frame_id         = 'odom'
        self.odom_msg.child_frame_id          = 'base_footprint'
        self.odom_msg.pose.pose.position.x    = self.X
        self.odom_msg.pose.pose.position.y    = self.Y
        self.odom_msg.pose.pose.orientation.x = q[1]
        self.odom_msg.pose.pose.orientation.y = q[2]
        self.odom_msg.pose.pose.orientation.z = q[3]
        self.odom_msg.pose.pose.orientation.w = q[0]
        self.odom_msg.twist.twist.linear.x    = V
        self.odom_msg.twist.twist.angular.z   = Omega
        self.odom_pub.publish(self.odom_msg)

    def stop_handler(self, signum, frame):
        self.get_logger().info("SIGINT recibido, cerrando...")
        raise SystemExit

def main(args=None):
    rclpy.init(args=args)
    node = DeadReckoning()
    signal.signal(signal.SIGINT, node.stop_handler)
    try:
        rclpy.spin(node)
    except SystemExit:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()