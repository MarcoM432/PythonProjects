def in1to10(n, outside_mode):
  if outside_mode == False:
    if 1 <= n <= 10:
      return True 
  if outside_mode == True:
    if 1 >= n or n >= 10:
      return True
  else:
    return False
  
  
  in1to10(10,True)