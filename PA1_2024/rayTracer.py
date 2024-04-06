#!/usr/bin/env python3
# -*- coding: utf-8 -*
# sample_python aims to allow seamless integration with lua.
# see examples below

import os
import sys
import pdb  # use pdb.set_trace() for debugging
import code # or use code.interact(local=dict(globals(), **locals()))  for debugging.
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image 

class Color:
    def __init__(self, R, G, B):
        self.color=np.array([R,G,B]).astype(np.float64)

    # Gamma corrects this color.
    # @param gamma the gamma value to use (2.2 is generally used).
    def gammaCorrect(self, gamma):
        inverseGamma = 1.0 / gamma;
        self.color=np.power(self.color, inverseGamma)

    def toUINT8(self):
        return (np.clip(self.color, 0,1)*255).astype(np.uint8)

class Sphere:
    def __init__(self, radius, center, shader):
        self.radius = radius
        self.center = center
        self.shader = shader

class Shader_Lambertian:
    def __init__(self, diffuseColor, name):
        self.diffuseColor = diffuseColor
        self.name = name

class Shader_Phong:
    def __init__(self, diffuseColor, name, specularColor, exponent):
        self.diffuseColor = diffuseColor
        self.name = name
        self.specularColor = specularColor
        self.exponent = exponent
        
class light:
    def __init__(self, position, intensity):
        self.position = position
        self.intensity = intensity

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm

def sphere_intersect(origin, direction, sphere):
    a = np.dot(direction, direction)
    b = 2 * np.dot(origin - sphere.center, direction)
    c = np.dot(origin - sphere.center, origin - sphere.center) - sphere.radius * sphere.radius
    discriminant = b ** 2 - 4 * a * c 
    
    if discriminant < 0: # 판별식이 0보다 작으면 교차 안함
        return None
    
    dist = (-b - np.sqrt(discriminant)) / (2 * a)
    
    if dist < 0:
        return None
    hit = origin + direction * dist
    return {'distance': dist, 'point': hit, 'sphere': sphere}
    #return dist



def ray_tracing(origin, direction, list_of_surface, list_of_light):
    closest = {'distance': np.inf, 'point': None, 'sphere': None}

    for sphere in list_of_surface:
        hit = sphere_intersect(origin, direction, sphere)

        if hit is not None and hit['distance'] < closest['distance']:   #가장 가까운 점 찾기
            closest = hit
    
    if closest['sphere'] is None:   # 교차 안 하면 검정색으로
        return np.array([0, 0, 0])


    hit_point = closest['point']
    normal = normalize(hit_point - closest['sphere'].center)
    view_dir = normalize(origin - hit_point)
    hit_color = np.array([0.0, 0.0, 0.0], dtype=np.float64)

    for light in list_of_light:
        light_dir = normalize(light.position - hit_point)
        shadow_ray_origin = hit_point + normal * 1e-5
        in_shadow = False

        for other_sphere in list_of_surface:
            shadow_hit = sphere_intersect(shadow_ray_origin, light_dir, other_sphere)

            if shadow_hit and shadow_hit['distance'] < np.linalg.norm(light.position - hit_point):
                in_shadow = True
                break

        if not in_shadow:
            shader = closest['sphere'].shader
            
            if isinstance(shader, Shader_Lambertian):
                #print("Lambertian")
                diffuse = max(np.dot(light_dir, normal), 0.0)
                hit_color += shader.diffuseColor * diffuse * light.intensity

            elif isinstance(shader, Shader_Phong):
                #print("Phong")
                diffuse_intensity = max(np.dot(light_dir, normal), 0.0)
                hit_color += shader.diffuseColor * diffuse_intensity * light.intensity
                view_dir = normalize(origin - hit_point)
                h = normalize(light_dir + view_dir) 
                specular_intensity = max(np.dot(normal, h), 0.0) ** shader.exponent
                hit_color += shader.specularColor * specular_intensity * light.intensity



    color = Color(hit_color[0], hit_color[1], hit_color[2])
    color.gammaCorrect(2.2)
    
    return color.toUINT8()   # r, g, b 값 return

def reflect(I, N):
    return I - 2 * np.dot(I, N) * N


def main():


    tree = ET.parse(sys.argv[1])
    root = tree.getroot()

    # set default values
    viewDir = np.array([0,0,-1]).astype(np.float64)
    viewUp = np.array([0,1,0]).astype(np.float64)
    viewProjNormal = -1*viewDir  # you can safely assume this. (no examples will use shifted perspective camera)
    viewWidth = 1.0
    viewHeight = 1.0
    projDistance = 1.0
    intensity = np.array([1,1,1]).astype(np.float64)  # how bright the light is.

    imgSize=np.array(root.findtext('image').split()).astype(np.int64)
    

    for c in root.findall('camera'):
        viewPoint = np.array(c.findtext('viewPoint').split()).astype(np.float64)
        viewDir = np.array(c.findtext('viewDir').split()).astype(np.float64)
        if(c.findtext('projNormal')):
            viewProjNormal = np.array(c.findtext('projNormal').split()).astype(np.float64)
        viewUp = np.array(c.findtext('viewUp').split()).astype(np.float64)
        if(c.findtext('projDistance')):
            projDistance = np.array(c.findtext('projDistance').split()).astype(np.float64)
        viewWidth=np.array(c.findtext('viewWidth').split()).astype(np.float64)
        if(c.findtext('viewHeight')):
            viewHeight = np.array(c.findtext('viewHeight').split()).astype(np.float64)

    list_of_shader = []   
    for c in root.findall('shader'):
        diffuseColor_c = np.array(c.findtext('diffuseColor').split()).astype(np.float64)
        name_c = c.get('name')
        type_of_shader = c.get('type')
        if type_of_shader == 'Lambertian':
            shader_c = Shader_Lambertian(diffuseColor_c, name_c)
        elif type_of_shader == 'Phong':
            specularColor_c = np.array(c.findtext('specularColor').split()).astype(np.float64)
            exponent_c = np.array(c.findtext('exponent').split()).astype(np.float64)
            shader_c = Shader_Phong(diffuseColor_c, name_c, specularColor_c, exponent_c)
        list_of_shader.append(shader_c)
            
        #print('name', c.get('name'))
        

    list_of_surface = []
    for c in root.findall('surface'):
        typeC = c.get('type')
        surfaceC = None
        refC = None

        if typeC == 'Sphere':
            radiusC = np.array(c.findtext('radius')).astype(np.float64)
            centerC = np.array(c.findtext('center').split()).astype(np.float64)
            for shader in list_of_shader:
                shader_tag = c.find('shader')

                if shader_tag is not None:
                    refC = shader_tag.get('ref')
                if shader.name == refC:
                    surfaceC = Sphere(radiusC, centerC, shader)
                    break
        if surfaceC is not None:
            list_of_surface.append(surfaceC)

        #list_of_surface.append(surfaceC)
        #print('diffuseColor', diffuseColor_c)
    #code.interact(local=dict(globals(), **locals()))  
    
    list_of_light = []
    for c in root.findall('light'):
        positionC = np.array(c.findtext('position').split()).astype(np.float64)
        intensityC = np.array(c.findtext('intensity').split()).astype(np.float64)
        lightC = light(positionC, intensityC)
        list_of_light.append(lightC)

    # Create an empty image
    channels=3
    img = np.zeros((imgSize[1], imgSize[0], channels), dtype=np.uint8)
    img[:,:]=0
    
    # replace the code block below!
    """for i in np.arange(imgSize[1]): 
        white=Color(1,1,1)
        red=Color(1,0,0)
        blue=Color(0,0,1)
        img[10][i]=white.toUINT8()
        img[i][i]=red.toUINT8()
        img[i][0]=blue.toUINT8()

    for x in np.arange(imgSize[0]): 
        img[5][x]=[255,255,255]"""
    # unit vectors
    w = viewDir
    w_normalize = normalize(w)

    u = np.cross(w_normalize, viewUp)
    u_normalize = normalize(u)

    v = np.cross(w_normalize, u_normalize)
    v_normalize = normalize(v)

    e = w_normalize * projDistance - v_normalize * viewHeight/imgSize[1]*(imgSize[1]/2 + 0.5) - u_normalize * viewWidth/imgSize[0]*(imgSize[0]/2 + 0.5)


    for x in np.arange(imgSize[0]):
        for y in np.arange(imgSize[1]):
            s = e + (viewWidth/imgSize[0])*x*u_normalize + (viewHeight/imgSize[1])*y*v_normalize
            img[y][x] = ray_tracing(viewPoint, s, list_of_surface, list_of_light)


    rawimg = Image.fromarray(img, 'RGB')
    #rawimg.save('out.png')
    rawimg.save(sys.argv[1]+'.png')
    
if __name__=="__main__":
    main()
