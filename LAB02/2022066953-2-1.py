import glfw
from OpenGL.GL import *
import numpy as np

# global variable to store the primitive type
current_primitive = GL_LINE_LOOP

def key_callback(window, key, scancode, action, mods):
    global current_primitive
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_1:
            current_primitive = GL_POINTS
        elif key == glfw.KEY_2:
            current_primitive = GL_LINES
        elif key == glfw.KEY_3:
            current_primitive = GL_LINE_STRIP
        elif key == glfw.KEY_4:
            current_primitive = GL_LINE_LOOP
        elif key == glfw.KEY_5:
            current_primitive = GL_TRIANGLES
        elif key == glfw.KEY_6:
            current_primitive = GL_TRIANGLE_STRIP
        elif key == glfw.KEY_7:
            current_primitive = GL_TRIANGLE_FAN
        elif key == glfw.KEY_8:
            current_primitive = GL_QUADS
        elif key == glfw.KEY_9:
            current_primitive = GL_QUAD_STRIP
        elif key == glfw.KEY_0:
            current_primitive = GL_POLYGON

            
def draw_dodecagon():
    
    angles = np.linspace(0, 2*np.pi, 12, endpoint=False)
    
    glBegin(current_primitive)
    for angle in angles:
        x = 1.0 * np.cos(angle)
        y = 1.0 * np.sin(angle)
        glVertex2f(x, y)
    glEnd()

def main():
    # Initialize the library
    if not glfw.init():
        return

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(480, 480, "2022066953-2-1", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)
    
    # Make the window's context current
    glfw.make_context_current(window)

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Poll for and process events
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT)
        
        draw_dodecagon()
        
        # Swap front and back buffers
        glfw.swap_buffers(window)
    
    glfw.terminate()

if __name__ == "__main__":
    main()
