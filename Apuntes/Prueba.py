goal = 9
goal1 = goal / 5
goal1 = int(goal1)
print(goal1)


def make_bricks(small, big, goal):
  goal1 = goal / 5
  goal1 = int(goal1)
  big1 = big - goal1
  big1 = big1 *5
  small1 = goal - big1
  print(small1)
  if small1 > small:
    return False 


print(make_bricks(3,2,9))
