import PIL
import matplotlib.pyplot as plt # single use of plt is commented out
import os.path
import PIL.ImageDraw

def round_corners(original_image, percent_of_side):
    '''
    Rounds the corner of a PIL.Image
    original_image must be a PIL.Image
    Returns a new PIL.Image with rounded corners, where
    0 < percent_of_side < 1
    is the corner radius as a portion of the shorter dimension of original_image
    '''

    #set the radius of the rounded corners
    width, height = original_image.size
    radius = int(percent_of_side * min(width, height)) # radius in pixels
    
    ###
    #create a mask
    ###
    
    #start with transparent mask
    rounded_mask = PIL.Image.new('RGBA', (width, height), (127,0,127,0))
    drawing_layer = PIL.ImageDraw.Draw(rounded_mask)
    # Overwrite the RGBA values with A=255.
    # The 127 for RGB values was used merely for visualizing the mask
    #make the mask of the new eclipse shape
    drawing_layer.ellipse((0,0,width, height),
                            fill=(0,127,127,255)) #top left
    # Uncomment the following line to show the mask
    #plt.imshow(frame)
    # Make the new image, starting with all transparent
    result = PIL.Image.new('RGBA', original_image.size, (0,0,0,0))
    result.paste(original_image, (0,0), mask=rounded_mask)
    #result.paste(result, (0,0), mask=frame)
    frame_mask = PIL.Image.new('RGBA', (width, height), (0, 0, 0, 0))
    drawing_layerF = PIL.ImageDraw.Draw(frame_mask)
    # Draw hollow eclipse frame
    drawing_layerF.ellipse((0,0,width, height),
                            fill=(240,240,30,255))
    drawing_layerF.ellipse((20,20,width-20, height-20),
                                    fill=(0,127,127,0))
    result.paste(frame_mask,(0,0),mask=frame_mask)
    return result
    
def get_images(directory=None):
    """ Returns PIL.Image objects for all the images in directory.
    If directory is not specified, uses current directory.
    Returns a 2-tuple containing
    a list with a PIL.Image object for each image file in root_directory, and
    a list with a string filename for each image file in root_directory    
    """
 
    if directory == None:
        directory =  os.getcwd() ##os.getcwd() # Use working directory if unspecified
       
    image_list = [] # Initialize aggregaotrs
    file_list = []
       
    directory_list = os.listdir(directory) # Get list of files
    for entry in directory_list:
        absolute_filename = os.path.join(directory, entry)
        try:
            image = PIL.Image.open(absolute_filename)
            file_list += [entry]
            image_list += [image]
        except IOError:
            pass # do nothing with errors tying to open non-images
    return image_list, file_list

def round_corners_of_all_images(directory=None):
    """ Saves a modfied version of each image in directory.
    Uses current directory if no directory is specified.
    Places images in subdirectory 'modified', creating it if it does not exist.
    New image files are of type PNG and have transparent rounded corners.
    """

    if directory == None:
        directory =  os.getcwd() ##os.getcwd() # Use working directory if unspecified
    print directory

    # Create a new directory 'modified'
    new_directory = os.path.join(directory, 'modified2')
    try:
        os.mkdir(new_directory)
    except OSError:
        pass # if the directory already exists, proceed

    #load all the images
    image_list, file_list = get_images(directory)

    #go through the images and save modified versions
    for n in range(len(image_list)):

    # Parse the filename
        filename, filetype = file_list[n].split('.')
    # Round the corners with radius = 30% of short side
        new_image = round_corners(image_list[n],.30)
#save the altered image, suing PNG to retain transparency
        new_image_filename = os.path.join(new_directory, filename + '.png')
        new_image.save(new_image_filename)    