#!/usr/bin/env python
import rospy
from trajectory_msgs.msg import JointTrajectory,JointTrajectoryPoint
import cv2
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class Img2joint:
  x = 0
  y = 0

  def __init__(self):
    global control_publisher
    rospy.Subscriber('/camera/rgb/image_raw', Image, self.trackerCallback)
    self.bridge = CvBridge()
    control_publisher = rospy.Publisher('/joint_trajectory_controller/command', JointTrajectory, queue_size=10)
    

  def trackerCallback(self, ros_msg):
    try:
      cv_img = self.bridge.imgmsg_to_cv2(ros_msg, "bgr8")
    except CvBridgeError as e:
      print(e)
      return
    mask_img = self.get_masked_image(cv_img)
    _, contours, hierarchy = cv2.findContours(mask_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # One method of drawing contours
    # index = -1
    # thickness = 2
    # color = (255,0,255)
    # cv2.drawContours(cv_img, contours, index, color, thickness)
    # cv2.imshow("Ball Video", cv_img)
    # cv2.waitKey(3)
    self.draw_ball_contours(cv_img, contours)
    #calculating joint positions
    self.calculateJoints(x,y)

  def get_masked_image(self,rgb_img):
    hsv = cv2.cvtColor(rgb_img,cv2.COLOR_BGR2HSV)
    #mudar aqui cor		
    blueLower = np.array([95,50,50],np.uint8)
    blueUpper = np.array([110,255,255],np.uint8)
    mask = cv2.inRange(hsv,blueLower,blueUpper)
    return mask



  def draw_ball_contours(self, rgb_img, contours):
    black_img = np.zeros(rgb_img.shape, 'uint8')
    for c in contours:
      area = cv2.contourArea(c)
      ((x,y), radius) = cv2.minEnclosingCircle(c)
      if (area > 5000):
        cv2.drawContours(rgb_img, [c], -1, (255,0,255), 2)
        cx, cy = self.get_contour_center(c)
        global x
        global y
        x = cx
        y = cy
        cv2.circle(rgb_img, (cx,cy), (int)(radius), (0,255,255), 3)
        cv2.circle(black_img, (cx,cy), (int)(radius), (0,255,255), 3)
        cv2.circle(black_img, (cx,cy), 5, (150,0,255), -1)
      # print("Area: ", area)

    cv2.imshow("Ball Tracking", rgb_img)
    cv2.imshow("Black Background Tracking", black_img)
    cv2.waitKey(3)

  def get_contour_center(self, contour):
    M = cv2.moments(contour)
    cx = -1
    cy = -1
    if (M['m00'] != 0):
      cx = int(M['m10']/M['m00'])
      cy = int(M['m01']/M['m00'])
    return cx, cy
	
  def calculateJoints(self, x, y):
    #junta 1 maximo range +- 2.7
    #jinta 2 ate 0.8 - 0
    #junta 3 ate 1.7
    #junta 4 0
    #junta 5 0.7 - 0.0 
    #y ->479 x ->639
    j1 = 0
    ponto_zero = 319
    y_total = 479
    x_meio = 319
    passoj1 = 2.7/x_meio
    passoj2 = 0.8/y_total
    passoj3 = 1.7/y_total
    passoj5 = 0.7/y_total
    j1 = (x-ponto_zero)*passoj1
    j2 = 0
    j3 = 0
    j5 = 0
#((y - y_total)*passoj5*-1)
    print("J1 Value",j1)
    self.publish_msg2joint(j1,j2,j3,j5)

  def publish_msg2joint(self,j1,j2,j3,j5):
    global control_publisher
    msg=JointTrajectory()
    msg.header.stamp = rospy.Time.now()
    msg.header.frame_id = ''
    msg.joint_names = ['joint1','joint2','joint3','joint4','joint5', 'joint6']
    point = JointTrajectoryPoint()
    j4 = 0
    j6 = 0
    point.positions = [j1,j2,j3,j4,j5,j6]
    point.velocities = []
    point.accelerations = []
    point.effort = []
    point.time_from_start = rospy.Duration(1)
    msg.points.append(point)
    control_publisher.publish(msg)
    rospy.loginfo(msg)


if __name__ == '__main__':
  try:
    rospy.init_node('melfa_controller_python')
    tracker_obj = Img2joint()
    rospy.spin()
  except rospy.ROSInterruptException:
    rospy.loginfo("Node terminated.")


