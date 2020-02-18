#ifndef COLORSPACETRANSFORM_H
#define COLORSPACETRANSFORM_H

#include <cstdio>
#include <cstdlib> #rand etc
#include <string>
#include <iostream>
#include <climits> #<limits.h>

##define CT_TESTLIMITS

#include "frameworkdummy.h"
#include "preporting.h"

using namespace std

namespace ProtoArmor
 char c255=(char)255
extern float YCToRgb_fMaxY
extern float YCToRgb_fMaxU
extern float YCToRgb_fMaxV
extern float YCToRgb_fMinY
extern float YCToRgb_fMinU
extern float YCToRgb_fMinV
extern float RgbToYC_fMaxY
extern float RgbToYC_fMaxU
extern float RgbToYC_fMaxV
extern float RgbToYC_fMinY
extern float RgbToYC_fMinU
extern float RgbToYC_fMinV
extern float YCToRgb_byMaxR
extern float YCToRgb_byMaxG
extern float YCToRgb_byMaxB
extern float YCToRgb_byMinR
extern float YCToRgb_byMinB
extern float YCToRgb_byMinG
#class CONVERT_FAKESTATIC_CLASS#public:
#	static byte ToByte(float val)
#	static byte ToByte(double val)
#	static char ToChar8(float val)
#	static char ToChar8(double val)
#
def GetCurrentOrPrevFrameFor(self, sAnyFrameFile, iFrame):
def IsDigit(self, val):
#void YUV4xxSubsampledPlanarToYUV444NonPlanar(unsigned char* dest, bAddDestAlpha, char* source, char* source_Stride, int source_J, int source_a, int source_b, int w, int h)
#void RgbToYC(byte &Y, &U, &V, r, g, b)
def RgbToYC(self, char &Y, char &U, char &V, char r, char g, char b):
#void YCToRgb(byte &r, &g, &b, Y, U, V)
def YCToRgb(self, char &r, char &g, char &b, char Y, char U, char V):
def YUV444NonPlanarToRGB(self, char* dest, bDestHasAlphaChannel, bSetDestAlphaTo255_IgnoredIfNoDestAlpha, char* source, int iPixels):
void CopySurface_BitdepthSensitive(unsigned char* dest, int dest_BytesPP, int dest_Stride, char* source, int source_BytesPP, int source_Stride, int w, int h); #	void CopySurface_BitdepthSensitive(unsigned char* dest, int dest_BytesPP, char* source, int source_BytesPP, int iTotalPixels)
def CopyPlaneToNonPlanar(self, char* dest, int DestChannelIndex, int dest_BytesPP, char* source, int source_Stride, int w, int h, bSamplesOnSecondLineOfSource):
def CopyNonPlanarToPlane(self, char* dest, int dest_Stride, bSamplesOnSecondLineOfDest, char* source, int SourceChannelIndex, int source_BytesPP, int w, int h):
def SaveRaw(self, sFile, char* buffer, iBytes):
def Heal_ToNearestPixel(self, char* dest, int dest_BytesPP, int dest_Stride, char* mask, int mask_BytesPP, int mask_Stride, int mask_Channel, int w, int h, rReachMultiplier_UNUSED, rRadialSampleSpacing_UNUSED, rDiffusionMultiplier):
def Heal_WithAveraging_Permutations(self, char* dest0, int dest_BytesPP, int dest_Stride, char* mask0, int mask_BytesPP, int mask_Stride, int mask_Channel, int w, int h, rReachMultiplier, rRadialSampleSpacing, rDiffusionMultiplier, bHorizonalSearch, bVerticalSearch):
def Diffuse(self, char* dest0, int dest_w, int dest_h, int dest_BytesPP, int dest_Stride, at_x, at_y, char* brush0, int brush_w, int brush_y, int brush_BytesPP, int brush_Stride, int brush_Channel, iPixelsRadius, bRandom):
def Heal_WithAveraging_Sequential(self, char* dest, int dest_BytesPP, int dest_Stride, char* mask, int mask_BytesPP, int mask_Stride, int mask_Channel, int w, int h, rReachMultiplier, rRadialSampleSpacing, rDiffusionMultiplier):
}#end namespace
#endif
