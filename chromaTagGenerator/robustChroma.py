'''
  @Description: 
      Given an input matrix, duplicates and rotates image 180 degrees.
      Thereby enabling the encoding of an image twice for a more robust,
      AprilTag dubed ChromaTag.

  @Author: Austin Walters
  @Creation Date: 9/21/2014
  @Last Modified: 5/08/2015
  @Written in Python 2.7
'''

import sys
import os
from PIL import Image


# TODO: ENSURE COLORS ARE OPTIMAL
# AprilTag - (a, b) - colors

# (1, 1) - (a+, b+) - orange = (241, 125, 42)
# (1, 0) - (a+, b-) - magenta = (248, 140, 149)
# (0, 1) - (a-, b+) - lime = (90, 205, 86)
# (0, 0) - (a-, b-) - teal = (23, 249, 255)


orange = (255,  125, 42)
magenta = (200, 114, 239)
lime = (82, 255, 0)
teal = (25, 255, 255)

black = (0, 0, 0)
white = (255, 255, 255)

colors = [orange, magenta, lime, teal]

'''
Flips and encodes!
Could use http://stackoverflow.com/questions/16265673/rotate-image-by-90-180-or-270-degrees
for OpenCV implementation
'''
def encode(matrix):

    encodedMatrix = []
    
    try:
        height = len(matrix) 
        width = len(matrix[0])
    except:
        return [[]]

    for i in range(height):
        newRow = []
        for j in range(width):
            tup = (matrix[i][j], matrix[height - i - 1][width - j - 1])
            newRow.append(tup)
        encodedMatrix.append(newRow)
    return encodedMatrix

'''
Decodes encoded matrix from image
'''
def image2Matrix(imageMatrix):
    
    matrix = []

    try:
        height = len(imageMatrix)
        width = len(imageMatrix[0])
    except:
        return [[]]

    for i in range(height):
        row = []
        for j in range(width):
            if imageMatrix[i][j] is colors[0]:
                row.append((1, 1))
            elif imageMatrix[i][j] is colors[1]:
                row.append((1, 0))
            elif imageMatrix[i][j] is colors[2]:
                row.append((0, 1))
            elif imageMatrix[i][j] is colors[3]:
                row.append((0, 0))
        matrix.append(row)
    return matrix

'''
Creates an image from a matrix
'''
def generateImage(name, matrix):

    scale = 100
    size = len(matrix) * scale
    img = Image.new("RGB", (size, size), (255, 255, 255))
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            for k in range(scale):
                for t in range(scale):
                    img.putpixel((j*scale + k, i*scale + t), matrix[i][j])
    img.save(name, "PNG")

'''
Creates a black and white image
'''
def generateBWMatrix(matrix):

    imageMatrix = []
    i = 0
    
    for row in matrix:
        imageMatrix.append([])
        for entry in row:
            if entry is 1:
                imageMatrix[i].append(black)
            else:
                imageMatrix[i].append(white)
        i += 1
    return imageMatrix

'''
Converts the tuples into pixel matrix
'''
def generateColorMatrix(matrix):    

    imageMatrix = []
    i = 0

    for row in matrix:
        imageMatrix.append([])
        for entry in row:
            if entry[0] is 0:
                if entry[1] is 0:
                    imageMatrix[i].append(colors[0])
                else:
                    imageMatrix[i].append(colors[1])
            else:
                if entry[1] is 0:
                    imageMatrix[i].append(colors[2])
                else:
                    imageMatrix[i].append(colors[3])
        i += 1
    return imageMatrix


'''
Prints a matrix in a decent format
'''
def printMatrix(matrix):
    for i in range(len(matrix)):
        print '\t[',
        for j in range(len(matrix[i])):
            print matrix[i][j], 
        print ']'

'''
  Simple test, checks to see if input == output
'''
def runTest(name, test):

    if not os.path.exists('output/'):
        os.makedirs('output')
    if not os.path.exists('input/'):
        os.makedirs('input')

    print '\n-- Beginning Test %s! --\n' % (name)
    print 'input matrix:'
    printMatrix(test)
    print 'Genearting Input Image...'
    inputName = 'input/' + name + '-april.png'
    generateImage(inputName, generateBWMatrix(test))
#    print 'tuple matrix:'
#    printMatrix(encode(test))
#    print 'coded matrix:'
#    printMatrix(generateColorMatrix(encode(test)))
#    print 'tuple matrix:'
#    printMatrix(image2Matrix(generateColorMatrix(encode(test))))
#    print 'Generating Output Image...'
    outputName = os.getcwd() + '/output/' + name + '-chroma.png'
    generateImage(outputName, generateColorMatrix(encode(test)))

#    if encode(test) == image2Matrix(generateColorMatrix(encode(test))):
#        print '\nOutput == Input!'
#        print 'Successfully, Completed Test %s!\n\n' % (name)
#    else:
#        print '\nOutput != Input!'
#        print 'Failed Test %s!\n\n' % (name)

'''
  Convert to two-dimensional array
'''
def toTwoDArray(numin, length):
    resMatrix = []
    while numin > 0:
        num = numin & 0b11111
        numin = numin >> length
        line = []
        for i in range(length):
            if num & 0b1:
                line.append(0)
            else:
                line.append(1)
            num = num >> 1
        resMatrix.append(line[::-1])
    if(len(resMatrix) < length):
        resMatrix.extend([[0] * length for row in range(length - len(resMatrix))])
    return resMatrix[::-1]

'''
  Add outliers to the two-dimensional array
'''
def addOutliers(numin):
    resMatrix = []
    length = len(numin)
    # top
    resMatrix.append([0] * (length + 4))
    resMatrix.append([1] * (length + 4))
    resMatrix[1][0] = 0
    resMatrix[1][-1] = 0
    # mid
    for i in range(length):
        line = [0, 1]
        line.extend(numin[i])
        line.extend([1, 0])
        resMatrix.append(line)
    # bottom
    resMatrix.append([1] * (length + 4))
    resMatrix[-1][0] = 0
    resMatrix[-1][-1] = 0        
    resMatrix.append([0] * (length + 4))
    return resMatrix

Tag25h9 = [0x25b7abL,  0x1d2c8faL, 0x1e130d4L, 0x703699L,  0x1776a86L, 0xc91d61L,
           0xb245c4L,  0x16c8317L, 0x1a02a68L, 0xbbbe46L,  0x21d112L,  0x162a467L,
           0x1748cacL, 0x11fa4bL,  0x1c503b1L, 0x1898f2eL, 0x125c0f7L, 0x59d7c2L,
           0x127e50dL, 0x9bf985L,  0xd8722cL,  0x13261b3L, 0x1ae71d9L, 0x15dd109L,
           0x189a1f2L, 0x17b27acL, 0x5edf55L,  0x182b92bL, 0x70ed4eL,  0x11d8ae0L,
           0x13be6dbL, 0xeeab84L,  0x48b4e8L,  0xd40e82L,  0x93503bL,  0x7d53beL]

print '\n---- TESTING Tag25h9 -----\n\n'
# print addOutliers(toTwoDArray(Tag25h9[0], 5))
for i in range(len(Tag25h9)):
    runTest('Tag25h9-' + str(i), addOutliers(toTwoDArray(Tag25h9[i], 5)))

# test = [[1, 0],[0, 1]]
# runTest('#1', test) 

# test2 = [[0, 1, 1], [1, 1, 1], [0, 1, 0]]
# runTest('#2', test2)

# apriltag36_11_12 = [[0,0,0,0,0,0,0,0,0,0],\
#                     [0,1,1,1,1,1,1,1,1,0],\
#                     [0,1,1,1,1,1,0,1,1,0],\
#                     [0,1,1,0,1,0,0,0,1,0],\
#                     [0,1,0,1,1,0,1,1,1,0],\
#                     [0,1,0,0,1,1,0,1,1,0],\
#                     [0,1,1,0,1,0,1,1,1,0],\
#                     [0,1,1,0,1,0,0,1,1,0],\
#                     [0,1,1,1,1,1,1,1,1,0],\
#                     [0,0,0,0,0,0,0,0,0,0]]

# runTest('tag36_11_12', apriltag36_11_12)

# apriltag36_11_13 = [[0,0,0,0,0,0,0,0,0,0],\
#                     [0,1,1,1,1,1,1,1,1,0],\
#                     [0,1,0,1,1,1,0,1,1,0],\
#                     [0,1,1,1,0,1,0,0,1,0],\
#                     [0,1,0,1,0,0,1,0,1,0],\
#                     [0,1,0,0,1,1,1,1,1,0],\
#                     [0,1,0,1,1,1,1,0,1,0],\
#                     [0,1,0,0,0,0,0,1,1,0],\
#                     [0,1,1,1,1,1,1,1,1,0],\
#                     [0,0,0,0,0,0,0,0,0,0]]

# runTest('tag36_11_13', apriltag36_11_13)

# apriltag36_11_14 = [[0,0,0,0,0,0,0,0,0,0],\
#                     [0,1,1,1,1,1,1,1,1,0],\
#                     [0,1,0,0,1,1,0,1,1,0],\
#                     [0,1,0,1,1,0,1,0,1,0],\
#                     [0,1,1,1,0,1,0,0,1,0],\
#                     [0,1,1,1,0,1,1,0,1,0],\
#                     [0,1,0,0,0,0,1,1,1,0],\
#                     [0,1,0,1,1,0,1,0,1,0],\
#                     [0,1,1,1,1,1,1,1,1,0],\
#                     [0,0,0,0,0,0,0,0,0,0]]

# runTest('tag36_11_14', apriltag36_11_14)

# apriltag36_11_80 = [[0,0,0,0,0,0,0,0,0,0],\
#                     [0,1,1,1,1,1,1,1,1,0],\
#                     [0,1,1,0,0,1,0,1,1,0],\
#                     [0,1,0,0,0,0,1,0,1,0],\
#                     [0,1,1,1,1,1,0,1,1,0],\
#                     [0,1,1,0,0,1,1,1,1,0],\
#                     [0,1,0,1,1,1,1,1,1,0],\
#                     [0,1,1,0,1,0,1,1,1,0],\
#                     [0,1,1,1,1,1,1,1,1,0],\
#                     [0,0,0,0,0,0,0,0,0,0]]

# runTest('tag36_11_80', apriltag36_11_80)


# apriltag36_11_544= [[0,0,0,0,0,0,0,0,0,0],\
#                     [0,1,1,1,1,1,1,1,1,0],\
#                     [0,1,0,0,0,0,1,1,1,0],\
#                     [0,1,1,0,1,1,1,0,1,0],\
#                     [0,1,0,0,1,0,0,1,1,0],\
#                     [0,1,0,1,1,0,0,1,1,0],\
#                     [0,1,1,0,0,0,1,1,1,0],\
#                     [0,1,1,1,0,0,1,1,1,0],\
#                     [0,1,1,1,1,1,1,1,1,0],\
#                     [0,0,0,0,0,0,0,0,0,0]]

# runTest('tag36_11_544', apriltag36_11_544)


# test4 = []
# print 'Enter 6 rows, each row MUST contain 6 entries of 1s and 0s ONLY!'
# print 'EXAMPLE: 1 0 1 0 1 0'
# '''
# for i in range(6):
#     row = input('Row #%s: ' % (i))
#     row = row.split()
#     test4.append(row)
# runTest('#4', test4)
# '''
