
import rclpy
from rclpy.node import Node
import cv2
import numpy as np
from sensor_msgs.msg import Image
from nav2_msgs.msg import ParticleCloud, Particle
from geometry_msgs.msg import Pose
from cv_bridge import CvBridge
from neato_tag.game import CALIBRATION_MATRIX, FOCAL_Y, NOTE_HEIGHT, NEATO_TAG, COLOR_TO_MASK

SHOWVISUALS = True


class CameraDetector(Node):
    def __init__(self):
        super().__init__('camera_detector')
        self.bridge = CvBridge()                  # used to convert ROS messages to OpenCV
        self.camera_subscriber = self.create_subscription(Image, 'camera/image_raw', self.find_neatos, 10)
        self.publisher = self.create_publisher(ParticleCloud, 'neatos_in_camera', 10)
        cv2.namedWindow('frame')
        cv2.namedWindow('mask')
    
    def find_neatos(self, msg):
        cloud = ParticleCloud()
        cloud.header = msg.header

        cv_image = self.bridge.imgmsg_to_cv2(msg)
        if SHOWVISUALS:
            cv2.imshow('frame', cv_image)
            k=cv2.waitKey(10)
            if k==27:
                cv2.destroyAllWindows()
        
        for color in NEATO_TAG.player_colors:
            particle = self.find_neatos_from_mask(cv_image, *COLOR_TO_MASK[color], color.lower())
            if particle is not None:
                cloud.particles.append(particle)
        self.publisher.publish(cloud)

    def find_neatos_from_mask(self, cv_image, lower_mask, upper_mask, color):
        mask = cv2.inRange(cv_image, lower_mask, upper_mask)

        if SHOWVISUALS:
            cv2.imshow(f'{color} mask',mask)
            k=cv2.waitKey(10)
            if k==27:
                cv2.destroyAllWindows()
        
        blobs, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(blobs) == 0:
            return None
        big_blob = max(blobs, key=lambda b: b.shape[0]).reshape((-1, 2))
        blob_center_pix = np.mean(big_blob, axis=0)+0.5 #.5 added to account for pixel center
        blob_max_y = np.max(big_blob[:, 1])
        blob_min_y = np.min(big_blob[:, 1])
        blob_height_pix = blob_max_y - blob_min_y
        # print(blob_center_pix, blob_height_pix)

        z_distance = FOCAL_Y*NOTE_HEIGHT/blob_height_pix
        center_homogenous = np.array([blob_center_pix[0], blob_center_pix[1], 1])
        dir_3d = np.linalg.inv(CALIBRATION_MATRIX) @ center_homogenous
        point_in_3D = z_distance * dir_3d / dir_3d[2]
        
        pose = Pose()
        # print(point_in_3D)
        pose.position.x = point_in_3D[0]
        pose.position.y = point_in_3D[2]
        return Particle(pose=pose, weight=1.0)

def main(args=None):
    rclpy.init()
    n = CameraDetector()
    rclpy.spin(n)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
