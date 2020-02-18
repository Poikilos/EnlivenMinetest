#ifndef PIMAGE_H
#define PIMAGE_H

#include <string>
#include "preporting.h"
#include "frameworkdummy.h"

using namespace std

namespace ProtoArmor
class PImage
public:
    static bool bPushToNearest_ShowMaskChannelError
    static bool bPushToNearestNondirectional_ShowMaskChannelError
    static bool PushToNearest(double& xStart, yStart, mask, int mask_w, int mask_h, int mask_BytesPP, int mask_Stride, int mask_Channel, mask_Threshold, bGreaterThanThreshold_FalseForLessThan)
    static bool PushToNearest(double& xStart, yStart, rDirection_Deg, mask, int mask_w, int mask_h, int mask_BytesPP, int mask_Stride, int mask_Channel, mask_Threshold, bGreaterThanThreshold_FalseForLessThan)
    static bool Draw(unsigned char* dest0, xDestStart, yDestStart, int dest_w, int dest_h, int dest_BytesPP, int dest_Stride, char* src0, int src_w, int src_h, int src_BytesPP, int src_Stride, char* mask0, int mask_BytesPP, int mask_Stride, int mask_Channel)

}#end namespace

#endif