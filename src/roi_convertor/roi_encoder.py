import roi_convertor.roi_decoder as dec
import struct

def RGB_encoder(fA,fR,fG,fB):
    bA = (fA).to_bytes(1, 'big') #ALPHA 0-255
    bR = (fR).to_bytes(1, 'big') #RED  0-255
    bG = (fG).to_bytes(1, 'big') #GREEN  0-255
    bB = (fB).to_bytes(1, 'big') #BLUE  0-255
    return int.from_bytes(bA+bR+bG+bB, byteorder='big')

def encode_ij_freehand_roi(roi_name, slice_id, x_coords, y_coords):
    HEADER_SIZE = 64
    HEADER2_SIZE = 64
    VERSION = 227 # v1.50d (point counters)
    TYPES = {'polygon':0,'rect':1,'oval':2,'line':3,'freeline':4,'polyline':5,
             'noROI':6,'freehand':7,'traced':8,'angle':9,'point':10}

    def write(roi_name, slice_id, x_coords, y_coords):
        def putShort(loc,num):
            dt = (num).to_bytes(2, 'big')
            data[loc:loc+2] = dt
        def putChar(loc,num):
            dt = struct.pack('!c', num)
            data[loc:loc+1] = dt
        def putByte(loc,num):
            dt = (num).to_bytes(1, 'big')
            data[loc:loc+1] = dt
        def putInt(loc,num):
            dt = (num).to_bytes(4, 'big')
            data[loc:loc+4] = dt
        def putFloat(loc,num):
            dt = struct.pack('!f', num)
            data[loc:loc+4] = dt
        def putName(roiName,hdr2Offset):
            offset = hdr2Offset+HEADER2_SIZE
            nameLength = roiName.__len__()
            putInt(hdr2Offset+dec.NAME_OFFSET, offset)
            putInt(hdr2Offset+dec.NAME_LENGTH, nameLength)
            for i in range(0, nameLength):
                putShort(offset+i*2, ord(roiName[i]))

        def putHeader2(roi_name, slice_id, hdr2Offset):
            putInt(dec.HEADER2_OFFSET,hdr2Offset)
            putInt(hdr2Offset+dec.C_POSITION, 0)
            putInt(hdr2Offset+dec.Z_POSITION, slice_id)
            putInt(hdr2Offset+dec.T_POSITION, 0)
            if roiNameSize >0:
                putName(roi_name, hdr2Offset)
            putFloat(hdr2Offset+dec.FLOAT_STROKE_WIDTH, 0.0)


        roiType = TYPES['freehand']

        if roi_name != None:
            roiNameSize = roi_name.__len__()*2
        else:
            roiNameSize = 0

        roiPropsSize = 0

        n = len(x_coords)
        options = 0
        floatSize = 0
        countersSize = 0

        # Python 3
        data = bytearray(HEADER_SIZE+HEADER2_SIZE+(n*4)+floatSize+roiNameSize+roiPropsSize+countersSize)
        data[0]=73; data[1]=111; data[2]=117; data[3]=116; # "Iout"

        putShort(dec.VERSION_OFFSET,VERSION)
        putByte(dec.TYPE,roiType)
        top = min(y_coords)
        putShort(dec.TOP, top)
        left = min(x_coords)
        putShort(dec.LEFT, left)
        putShort(dec.BOTTOM, max(y_coords))
        putShort(dec.RIGHT, max(x_coords))


        putShort(dec.N_COORDINATES, n)
        putInt(dec.POSITION,1)

        putHeader2(roi_name, slice_id, HEADER_SIZE+n*4+floatSize)

        if n>0:
            base1 = 64
            base2 = base1+2*n
            for i in range(0,n):
                putShort(base1+i*2, x_coords[i]-left)
                putShort(base2+i*2, y_coords[i]-top)

        return data

    return write(roi_name, slice_id, x_coords, y_coords)