# Computer_Graphics Project02 
This README file explains project02 of the 3rd-year Computer Graphics course (Professor Tae-Soo Kwon) in the Department of Computer Software Engineering at Hanyang University.
## Cow roller coaster
The goal of this project is to understand and generate spline curves, specifically using the Catmull-Rom spline, and apply these concepts to create an animation where a cow model follows a cyclic roller coaster track.

## Developing Environment
The project is implemented using Python and requires the following libraries:
- Python 3
- PIL (Python Imaging Library)
- GLFW (Graphics Library Framework)
- NumPy (Numerical Python)
- PyOpenGL (Python binding to OpenGL)

## Requirements
Start from the Skeleton Code:

1. The code requires reading the cow.obj file.
   - Understand the basic structure of the skeleton code.
   - Change the viewpoint by typing 'space'.
   - Identify parts of the source code that need modification (look for "TODO" comments).
   - Implement Control Point Specification:

2. Pick the cow by left-clicking on it.
   - Specify six control points for the cow’s trajectory by clicking on the random locations.
   - Duplicate the cow at each control point.
   - Use left-dragging to adjust the cow’s height.
   - After specifying all control points, the cow moves along a cyclic Catmull-Rom spline curve connecting these points, repeating the motion three times.

3. Animation Features:
   - The cow should face forward (yaw orientation).
   - The cow should face upward when going up (pitch orientation).
   - Ensure that when dragging, the pick-location on the cow’s bounding box aligns with the cursor.

## Usage Instructions
1. Run the main script to start the animation.
2. Left-click to pick and place control points for the cow's path.
3. Adjust the cow's height by left-dragging.
4. Press 'space' to change the camera viewpoint.
  
## Changed Code
#### 1. onMouseDrag
The onMouseDrag function handles vertical and horizontal dragging of the cow model by converting screen coordinates to a ray, determining intersections with defined planes, and updating the cow's transformation matrix accordingly. It also checks for intersections with the cow's bounding box to initiate dragging.
- Improved handling of vertical and horizontal dragging.
- Implemented correct intersection logic with the dragging plane.

      def onMouseButton(window,button, state, mods):
          global isDrag, V_DRAG, H_DRAG, count, positions, cow2wld, hasDragged
          GLFW_DOWN=1;
          GLFW_UP=0;
          x, y=glfw.get_cursor_pos(window)
          if button == glfw.MOUSE_BUTTON_LEFT and cursorOnCowBoundingBox:
              if state == GLFW_DOWN:
                  isDrag = V_DRAG
                  print( "Left mouse down-click at %d %d\n" % (x,y))
                  # start vertical dragging
              elif state == GLFW_UP and isDrag != 0:
                  isDrag = H_DRAG
                  hasDragged += 1
                  if hasDragged > 0:
                      if count < 6:
                          print("count: ",count)
                          positions[count%6] = cow2wld.copy()
                          
                          count += 1
                  print( "Left mouse up\n");
                  # start horizontal dragging using mouse-move events.
          elif button == glfw.MOUSE_BUTTON_RIGHT:
              if state == GLFW_DOWN:
                  print( "Right mouse click at (%d, %d)\n"%(x,y) );

#### 2. display
The display function clears the screen, sets the viewing transformation, and renders the scene, including the floor and cow models. It updates the cow's position and orientation along the Catmull-Rom spline for animation and handles rendering of control points and animated movement.
- Updated to handle cow animation along the Catmull-Rom spline curve.
- Added logic to render the cow at specified control points and animate the cow's movement.

      if count < 6:
              drawCow(cow2wld, cursorOnCowBoundingBox)
              for i in range(count):
                  drawCow(positions[i], False)  # Draw duplicated cows without bounding box
          elif count == 6:
              if not AnimationStarted:
                  startTime = glfw.get_time()
                  AnimationStarted = True
                  cowPosition = positions[0].copy()
              animTime = glfw.get_time() - startTime
      
              t = animTime % 6
              if animTime < 18.0:
                  for i in range(6):
                      if i <= t < i + 1:
                          t %= 1
                          spline = catmullRomSpline(t, positions[(5 + i) % 6], positions[i % 6], positions[(i + 1) % 6], positions[(i + 2) % 6])
                          cowDirection(t, positions[(5 + i) % 6], positions[i % 6], positions[(i + 1) % 6], positions[(i + 2) % 6])
                          break
              else:
                  resetAnimation()
                  return
      
              setTranslation(cowPosition, getTranslation(spline))
              drawCow(cowPosition, False)  # Draw animated cow without bounding box
      
          if count != 6:
              drawCow(cow2wld, cursorOnCowBoundingBox)
          glFlush()

#### 3. catmullRomSpline
The catmullRomSpline function calculates the interpolated position on a Catmull-Rom spline curve given a parameter t and four control points, ensuring smooth transitions between points.
- Implemented the Catmull-Rom spline curve calculation for smooth animation.
  
      def catmullRomSpline(t, p0, p1, p2, p3):
          t2 = t * t
          t3 = t2 * t
          return 0.5 * (2*p1 + (-p0 + p2)*t + (2*p0 - 5*p1 + 4*p2 - p3)*t2 + (-p0 + 3*p1 - 3*p2 + p3)*t3)

#### 4. cowDirection
The cowDirection function calculates and applies the cow's orientation (yaw and pitch) along the Catmull-Rom spline curve based on the current parameter t and four control points, ensuring the cow faces forward and adjusts its pitch when moving up or down.
- Calculated and applied the correct orientation (yaw and pitch) of the cow during the animation.

      def cowDirection(t, p0, p1, p2, p3):
          t2 = t * t
          direction = 0.5 * ((-p0 + p2) + 2 * (2*p0 - 5*p1 + 4*p2 - p3)*t + 3*(-p0 + 3*p1 - 3*p2 + p3)*t2)
          direction = normalize(getTranslation(direction))
      
          pitch = math.atan2(direction[1], np.sqrt(direction[0]**2 + direction[2]**2))
          yaw = math.atan2(direction[2], direction[0])
          
          Rx = np.array([[1., 0., 0.],
                          [0., np.cos(pitch), -np.sin(pitch)],
                          [0., np.sin(pitch), np.cos(pitch)]])
          Ry = np.array([[np.cos(yaw), 0., np.sin(yaw)], 
                          [0., 1., 0.], 
                          [-np.sin(yaw), 0., np.cos(yaw)]])
          
          cowPosition[0:3, 0:3] =  (Ry @ Rx).T


#### 5. resetAnimation
The resetAnimation function resets the animation state, including the count, cow's transformation matrix, control points, and other related variables, preparing the system for a new set of control points and animation cycle.

      def resetAnimation():
          global count, cow2wld, positions, AnimationStarted, isDrag, hasDragged
          count = -1
          positions = [positions[0] for _ in range(6)]
          cow2wld = positions[0].copy()
          AnimationStarted = False
          isDrag = 0
          hasDragged = 0

#### 6. onMouseButton
The onMouseButton function handles mouse button events to initiate and finalize dragging of the cow model. It updates the drag state, stores control points, and duplicates the cow model at specified positions when the left mouse button is clicked and released.
- Tracks the number of control points, ensuring there are six points to form a complete trajectory.
- Print when needed.

   def onMouseDrag(window, x, y):
       global isDrag, cursorOnCowBoundingBox, pickInfo, cow2wld
       if isDrag:
           print("in drag mode %d\n" % isDrag)
           ray = screenCoordToRay(window, x, y)
           pp = pickInfo
   
           if isDrag == V_DRAG:
               # Vertical dragging
               if cursorOnCowBoundingBox:
                   plane_normal = np.array((0, 0, 1))  # Vertical plane
                   cow_translation = getTranslation(cow2wld)
                   p = Plane(plane_normal, cow_translation)
                   intersect_result = ray.intersectsPlane(p)
   
                   if intersect_result[0]:  # Check for intersection
                       intersection_point = ray.getPoint(intersect_result[1])
                       intersection_point[0] = cow_translation[0]  # Fix X coordinate
   
                       translation_vector = intersection_point - cow_translation
                       translation_matrix = np.eye(4)
                       setTranslation(translation_matrix, translation_vector)
                       cow2wld = translation_matrix @ cow2wld
   
           else:
               # Horizontal dragging
               if cursorOnCowBoundingBox:
                   plane_normal = np.array((0, 1, 0))  # Horizontal plane
                   cow_translation = getTranslation(cow2wld)
                   p = Plane(plane_normal, cow_translation)
                   intersect_result = ray.intersectsPlane(p)
   
                   if intersect_result[0]:  # Check for intersection
                       intersection_point = ray.getPoint(intersect_result[1])
   
                       translation_vector = intersection_point - cow_translation
                       translation_matrix = np.eye(4)
                       setTranslation(translation_matrix, translation_vector)
                       cow2wld = translation_matrix @ cow2wld
       else:
           ray = screenCoordToRay(window, x, y)
   
           planes = []
           cow = cowModel
           bbmin = cow.bbmin
           bbmax = cow.bbmax
   
           planes.append(makePlane(bbmin, bbmax, vector3(0, 1, 0)))
           planes.append(makePlane(bbmin, bbmax, vector3(0, -1, 0)))
           planes.append(makePlane(bbmin, bbmax, vector3(1, 0, 0)))
           planes.append(makePlane(bbmin, bbmax, vector3(-1, 0, 0)))
           planes.append(makePlane(bbmin, bbmax, vector3(0, 0, 1)))
           planes.append(makePlane(bbmin, bbmax, vector3(0, 0, -1)))
   
           o = ray.intersectsPlanes(planes)
           cursorOnCowBoundingBox = o[0]
           cowPickPosition = ray.getPoint(o[1])
           cowPickLocalPos = transform(np.linalg.inv(cow2wld), cowPickPosition)
           pickInfo = PickInfo(o[1], cowPickPosition, cow2wld, cowPickLocalPos)
