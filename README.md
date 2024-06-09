# Computer_Graphics Project02 
### Cow roller coaster
The goal of this project is to understand and generate spline curves, specifically using the Catmull-Rom spline, and apply these concepts to create an animation where a cow model follows a cyclic roller coaster track.
### Developing Environment
The project is implemented using Python and requires the following libraries:
- Python 3
- PIL (Python Imaging Library)
- GLFW (Graphics Library Framework)
- NumPy (Numerical Python)
- PyOpenGL (Python binding to OpenGL)
### Requirements
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

