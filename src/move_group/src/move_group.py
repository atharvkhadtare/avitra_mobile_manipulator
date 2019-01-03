#!/usr/bin/env python

import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list

moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('move_group',
                anonymous=True)

robot = moveit_commander.RobotCommander()

scene = moveit_commander.PlanningSceneInterface()

group_name = "arm"
group = moveit_commander.MoveGroupCommander(group_name)

display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',
                                               moveit_msgs.msg.DisplayTrajectory,
                                               queue_size=20)

# We can get the name of the reference frame for this robot:
planning_frame = group.get_planning_frame()
print "============ Reference frame: %s" % planning_frame

# We can also print the name of the end-effector link for this group:
eef_link = group.get_end_effector_link()
print "============ End effector: %s" % eef_link

# We can get a list of all the groups in the robot:
group_names = robot.get_group_names()
print "============ Robot Groups:", robot.get_group_names()

# Sometimes for debugging it is useful to print the entire state of the
# robot:
print "============ Printing group_arm pose"
print group.get_current_pose()
print ""
# print "============ Printing robot state"
# print robot.get_current_state()
# print "====join_ngoal"

# We can get the joint values from the group and adjust some of the values:
joint_goal = group.get_current_joint_values()
joint_goal[0] = 0
joint_goal[1] = 0.0785
joint_goal[2] = 0
# joint_goal[3] = 0
# joint_goal[4] = 0

# The go command can be called with joint values, poses, or without any
# parameters if you have already set the pose or joint target for the group
group.go(joint_goal, wait=False)

# Calling ``stop()`` ensures that there is no residual movement
group.stop()


print "============ Printing group_arm pose"
print group.get_current_pose()
print ""
# print "============ Printing robot state"
# print robot.get_current_state()
# print ""

group_hand = moveit_commander.MoveGroupCommander("hand")
print "============ Printing hand pose"
print group_hand.get_current_pose()
print ""

pose_goal = geometry_msgs.msg.Pose()
pose_goal.orientation.w = 1.0
pose_goal.position.x = 0
pose_goal.position.y = 0.129
pose_goal.position.z = 0.192
group.set_pose_target(pose_goal)
# pose_goal = group.get_random_pose()
plan = group.go(wait=True)
# # Calling `stop()` ensures that there is no residual movement
group.stop()

print "============ Printing group_arm pose"
print group.get_current_pose()
print ""
print "============ Printing robot state"
print robot.get_current_state()
print ""

group_hand = moveit_commander.MoveGroupCommander("hand")
print "============ Printing hand pose"
print group_hand.get_current_pose()
print ""
# # It is always good to clear your targets after planning with poses.
# # Note: there is no equivalent function for clear_joint_value_targets()
group.clear_pose_targets()