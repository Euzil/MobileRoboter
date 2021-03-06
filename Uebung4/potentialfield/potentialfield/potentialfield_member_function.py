import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
from sensor_msgs.msg import LaserScan
from rclpy.qos import qos_profile_sensor_data
import numpy as np

class PotentialField(Node):
    x_vel =0.0
    y_vel =0.0
    z_angular_vel = 0.0 
    def __init__(self):
        super().__init__('potential_field')
        # TODO: create publisher and subscriber 
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.sensor = self.create_subscription(LaserScan,"scan",self.callback, qos_profile=qos_profile_sensor_data)
        timer_period = 0.2  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = Twist()
        msg.linear = Vector3(x=self.x_vel, y=0.0, z=0.0)
        msg.angular = Vector3(x=0.0, y=0.0, z=self.z_angular_vel)
        self.publisher_.publish(msg)
        #self.get_logger().info('Publishing: linear: {} angular: {}'.format(msg.linear, msg.angular))
        self.i += 1

    def callback(self,msg): 
        x = 0
        y = 0
        for idx, i in enumerate(msg.ranges):
            if i != float("inf") and i < 1.0:
                #print("idx: {} i: {} x: {} y: {}".format(idx, i, -math.cos(idx), -math.sin(idx)))
                x += -math.cos(math.radians(idx)) *(1/i)
                y += -math.sin(math.radians(idx)) *(1/i)

        x += 250
        y += 0
        vec_len = math.sqrt(x**2+y**2)

        #print("x: {} y: {}".format(x, y))
        if vec_len != 0:
            x = x / vec_len     
            y = y / vec_len
        
        #print("x: {} y: {}".format(x, y))

        angularZ = math.acos(((x*1)+(y*0))/(math.sqrt(x**2+y**2)))
        print(math.degrees(angularZ))
        if angularZ > math.radians(90):
            xVel = 0.0
            if y > 0:
                self.z_angular_vel = 0.99
                print(angularZ)
                print("left1")
            else: 
                self.z_angular_vel = -1
                print(angularZ)
                print("right1")
        elif angularZ > math.radians(70):
            xVel = 0.0
            if y > 0:
                self.z_angular_vel = 0.8
                print(angularZ)
                print("left1")
            else: 
                self.z_angular_vel = -0.8
                print(angularZ)
                print("right1")
        elif angularZ > math.radians(55):
            if y > 0:
                self.z_angular_vel = 0.5
                xVel = msg.ranges[0]*0.07
                print(angularZ)
                print("left2")
            else: 
                self.z_angular_vel = -0.5
                xVel = msg.ranges[0]*0.07
                print(angularZ)
                print("right2")
        elif angularZ > math.radians(45):
            if y > 0:
                self.z_angular_vel = 0.3
                xVel = msg.ranges[0]*0.07
                print(angularZ)
                print("left3")
            else: 
                self.z_angular_vel = -0.3
                xVel = msg.ranges[0]*0.07
                print(angularZ)
                print("right3")
    
        else:
            #xVel = msg.ranges[0]*0.087-0.0435
            xVel = msg.ranges[0]*0.07

            self.z_angular_vel =0.0
            print(angularZ)
            print("slow down")
        if xVel > 0.26: 
           
            print(xVel)
            self.x_vel = 0.5
            print("straight")
            print(x,angularZ)
            print("---------------")
        else:
            self.x_vel = xVel
            
            print("straight2")
            print(x,angularZ)
            print("---------------")

       
                
        
      

        #print("direction x: {} y: {} x_Vel: {} angZ: {}".format(x,y, self.x_vel, self.z_angular_vel))
        #self.x_vel = 0.0
        #self.z_angular_vel = 0.0
        # TODO: implement repulsive and attractice potential field  
        #self.get_logger().info("I sensor: {} avr:".format( msg.ranges[90] ))
        
        
        
    
    def destroy_node(self):
        # stop robot on shutdown 
        self.publisher_.publish(Twist()) 
        super().destroy_node()

def main(args=None): 
    rclpy.init(args=args)
    potentialfield = PotentialField()
    try:
        rclpy.spin(potentialfield)
    except KeyboardInterrupt:
        print("\nShutdown Potentialfield Node")
    finally:
        potentialfield.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

