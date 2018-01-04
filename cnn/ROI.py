import numpy as np
import shutil, time

from cntk_helpers import makeDirectory, getFilesInDirectory, imread, imWidth, imHeight, imWidthHeight,\
                         getSelectiveSearchRois, imArrayWidthHeight, getGridRois, filterRois, imArrayWidth,\
                         imArrayHeight, getCntkInputPaths, getCntkRoiCoordsLine, getCntkRoiLabelsLine  

####################################
# Parameters
####################################
boSaveDebugImg = True

# ROI generation
roi_minDimRel = 0.01      # minium relative width/height of a ROI
roi_maxDimRel = 1.0       # maximum relative width/height of a ROI
roi_minNrPixelsRel = 0    # minium relative area covered by ROI
roi_maxNrPixelsRel = 1.0  # maximm relative area covered by ROI
roi_maxAspectRatio = 4.0  # maximum aspect Ratio of a ROI vertically and horizontally
roi_maxImgDim = 200       # image size used for ROI generation
ss_scale = 100            # selective search ROIS: parameter controlling cluster size for segmentation
ss_sigma = 1.2            # selective search ROIs: width of gaussian kernal for segmentation
ss_minSize = 20           # selective search ROIs: minimum component size for segmentation
grid_nrScales = 7         # uniform grid ROIs: number of iterations from largest possible ROI to smaller ROIs
grid_aspectRatios = [1.0, 2.0, 0.5]    # uniform grid ROIs: aspect ratio of ROIs

def generate_input_rois(imgOrig, testing=False):
     # init
    roi_minDim = roi_minDimRel * roi_maxImgDim
    roi_maxDim = roi_maxDimRel * roi_maxImgDim
    roi_minNrPixels = roi_minNrPixelsRel * roi_maxImgDim*roi_maxImgDim
    roi_maxNrPixels = roi_maxNrPixelsRel * roi_maxImgDim*roi_maxImgDim

    # get rois
    rects, img, scale = getSelectiveSearchRois(imgOrig, ss_scale, ss_sigma, ss_minSize, roi_maxImgDim) 
    print ("   Number of rois detected using selective search: " + str(len(rects)))

    imgWidth, imgHeight = imArrayWidthHeight(img)

                # add grid rois
    rectsGrid = getGridRois(imgWidth, imgHeight, grid_nrScales, grid_aspectRatios)
    rects += rectsGrid
                # run filter
    rois = filterRois(rects, imgWidth, imgHeight, roi_minNrPixels, roi_maxNrPixels, 
                      roi_minDim, roi_maxDim, roi_maxAspectRatio)
    if len(rois) == 0: #make sure at least one roi returned per image
        rois = [[5, 5, imgWidth-5, imgHeight-5]]
    print ("   Number of rectangles after filtering  = " + str(len(rois)))
                # scale up to original size and save to disk
                # note: each rectangle is in original image format with [x,y,x2,y2]
    rois = np.int32(np.array(rois) / scale)
    assert (np.min(rois) >= 0)
    assert (np.max(rois[:, [0,2]]) < imArrayWidth(imgOrig))
    assert (np.max(rois[:, [1,3]]) < imArrayHeight(imgOrig))
    return rois
