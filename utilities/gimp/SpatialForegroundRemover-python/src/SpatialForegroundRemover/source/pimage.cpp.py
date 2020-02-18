#ifndef PIMAGE_CPP
#define PIMAGE_CPP

#include "pimage.h"
#include "pmath.h"

namespace ProtoArmor
bool PImage.bPushToNearest_ShowMaskChannelError=True
bool PImage.bPushToNearestNondirectional_ShowMaskChannelError=True
#/<summary>
#/Returns nearest pixel where channel mask_Channel is outside mask_Threshold
#/xStart, should normally be a pixel center (will be rounded to find pixel location)
#/(nondirectional overload)
#/</summary>
#/<param name="xStart"></param>
#/<param name="yStart"></param>
#/<return>returns False if edge was found before a near pixel was found</return>
def PushToNearest(self, xStart, yStart, mask, int mask_w, int mask_h, int mask_BytesPP, int mask_Stride, int mask_Channel, mask_Threshold, bGreaterThanThreshold_FalseForLessThan):
    bool bFound=False
    if mask_Channel>=mask_BytesPP:
        if bPushToNearestNondirectional_ShowMaskChannelError:
            Console.Error.WriteLine("PushToNearest [nondirectional version] error: channel index "+Convert.ToString(mask_Channel)+" (starting from 0) does not exist in "+Convert.ToString(mask_BytesPP*8)+"-bit ("+Convert.ToString(mask_BytesPP)+" bytes per pixel) image--last channel will be used.  This message will only be shown once")
            bPushToNearestNondirectional_ShowMaskChannelError=False

        mask_Channel=mask_BytesPP-1

    #double closest_Dist=DBL_MAX
    #double closest_X=-1
    #double closest_Y=-1
    double mask_rH=(double)mask_h
    double mask_rW=(double)mask_w
    double pointNow_Dist=-1.0
    #unsigned int uiLoc
    #unsigned int uiLineLoc=mask_Channel
    double rRadNow=0.0
    double rRadMax=0.0
    double dAbsNow;#just for caching Abs method result
    #NOTE: Since checks distance to all corners,
    #  still works if xStart, is outside of image.
    dAbsNow=PMath.Dist(xStart,yStart,0.0,0.0)
    if (dAbsNow>rRadMax) rRadMax=dAbsNow
    dAbsNow=PMath.Dist(xStart,yStart,0.0,mask_rH)
    if (dAbsNow>rRadMax) rRadMax=dAbsNow
    dAbsNow=PMath.Dist(xStart,yStart,mask_rW,0.0)
    if (dAbsNow>rRadMax) rRadMax=dAbsNow
    dAbsNow=PMath.Dist(xStart,yStart,mask_rW,mask_rH)
    if (dAbsNow>rRadMax) rRadMax=dAbsNow
    double rDegPerPix
    double rAngleNow
    double xNow=xStart
    double yNow=yStart
    unsigned int xRound=(unsigned int)(xNow+.5)
    unsigned int yRound=(unsigned int)(yNow+.5)
    if not (xRound<0orxRound>=mask_woryRound<0oryRound>=mask_h):
        if ( bGreaterThanThreshold_FalseForLessThan
                ? (mask[yRound*mask_Stride+xRound*mask_BytesPP+mask_Channel]>mask_Threshold)
                : (mask[yRound*mask_Stride+xRound*mask_BytesPP+mask_Channel]<mask_Threshold) )
            xStart=(double)xRound
            yStart=(double)yRound
            bFound=True


    double rRadAdd=.5
    if ( ((double)xRound!=xStart) or ((double)yRound!=yStart) ) rRadAdd=.25; #in case start is on border
    #unsigned int xRoundPrev=0
    #unsigned int yRoundPrev=-1
    if not bFound:
        for (rRadNow=rRadAdd; rRadNow<=rRadMax; rRadNow+=rRadAdd)
            rDegPerPix=PMath.DegreesPerPixelAt(rRadNow)
            if rDegPerPix>0.0:
                for (rAngleNow=0.0; rAngleNow<360.0; rAngleNow+=rDegPerPix)
                    xNow=xStart+PMath.XOfRThetaDeg(rRadNow,rAngleNow)
                    yNow=yStart+PMath.YOfRThetaDeg(rRadNow,rAngleNow)
                    xRound=(unsigned int)(xNow+.5)
                    yRound=(unsigned int)(yNow+.5)
                    if not (xRound<0orxRound>=mask_woryRound<0oryRound>=mask_h):
                        if ( bGreaterThanThreshold_FalseForLessThan
                                ? (mask[yRound*mask_Stride+xRound*mask_BytesPP+mask_Channel]>mask_Threshold)
                                : (mask[yRound*mask_Stride+xRound*mask_BytesPP+mask_Channel]<mask_Threshold) )
                            xStart=(double)xRound
                            yStart=(double)yRound
                            bFound=True
                            break
                        }#end if match (outside threshold)
                    }#end if in range
                }#end for rAngleNow
            }#end if rDegPerPix>0.0
            else:
                if PReporting.getIsMegaDebug()) Console.Error.WriteLine("PushToClosest error: rDegPerPix too small {rDegPerPix"+Convert.ToString(rDegPerPix)+"}":

            if (bFound) break
        }#end for rRadNow
    }#end if not matched (i.e. if not already on the pixel)
    '''
    for (double y=0; y<mask_rH; y+=1.0)    	uiLoc=uiLineLoc
    	for (double x=0; x<mask_rW; x+=1.0)    		if ( bGreaterThanThreshold_FalseForLessThan
    				? (mask[uiLoc]>mask_Threshold)
    				: (mask[uiLoc]<mask_Threshold) )    			pointNow_Dist=PMath.Dist(x,y,xStart,yStart)
    			if pointNow_Dist<closest_Dist:    				closest_Dist=pointNow_Dist
    				closest_X=x
    				closest_X=y
    				bFound=True

    		}#end if outside threshold color
    		uiLoc+=mask_BytesPP
    	}#end for x
    	uiLineLoc+=mask_Stride
    }#end for y
    if bFound:    	xStart=closest_X
    	yStart=closest_Y

    '''
    return bFound
}#end PushToNearest nondirectional version
#/<summary>
#/Returns nearest pixel where channel mask_Channel is outside mask_Threshold,
#only looking at pixels on the line at the given angle rDirection_Deg
#/xStart, should normally be a pixel center (will be rounded to find pixel location)
#/; directional overload; does not work with out-of-range starting point (checked after rounding)
#/</summary>
#/<param name="xStart"></param>
#/<param name="yStart"></param>
#/<return>returns False if edge was found before a near pixel was found</return>
def PushToNearest(self, xStart, yStart, rDirection_Deg, mask, int mask_w, int mask_h, int mask_BytesPP, int mask_Stride, int mask_Channel, mask_Threshold, bGreaterThanThreshold_FalseForLessThan):
    bool bFound=False
    if mask_Channel>=mask_BytesPP:
        if bPushToNearest_ShowMaskChannelError:
            Console.Error.WriteLine("PushToNearest(...,direction,...): error, index "+Convert.ToString(mask_Channel)+" (starting from 0) does not exist in "+Convert.ToString(mask_BytesPP*8)+"-bit ("+Convert.ToString(mask_BytesPP)+" bytes per pixel) image--last channel will be used.  This message will only be shown once")
            bPushToNearest_ShowMaskChannelError=False

        mask_Channel=mask_BytesPP-1

    #double xStart, yStart, rDirection_Deg
    #byte* mask
    #uint mask_w, mask_h
    #uint mask_BytesPP
    #uint mask_Stride
    #uint mask_Channel
    #byte mask_Threshold #mask_Needlean
    double dSubsampleSpacing=.125;#not 1 since could be intersecting pixels at any point (.125 is 8x subsampling)
    #use int to avoid out-of-range starting point
    int ixStart
    int iyStart
    unsigned int uiLoc
    int mask_iW=(int)mask_w
    int mask_iH=(int)mask_h
    do
        ixStart=(int)(xStart+.5); #+.5 for rounding
        iyStart=(int)(yStart+.5); #+.5 for rounding
        if (ixStart<0 or ixStart>=mask_iW or iyStart<0 or iyStart>=mask_iH) break
        #if ixStart>=0 and ixStart<mask_iW and iyStart>=0 and iyStart<mask_iH:        uiLoc=iyStart*mask_Stride+ixStart*mask_BytesPP+mask_Channel
        if ( bGreaterThanThreshold_FalseForLessThan
                ?(mask[uiLoc]>mask_Threshold)
                :(mask[uiLoc]<mask_Threshold) )
            bFound=True
            break

        #
        #else break
        PMath.Travel2d(xStart,yStart,rDirection_Deg,dSubsampleSpacing)

    while (not bFound)
    return bFound
}#end PushToNearest
#/<summary>
#/Draws to src0 to dest0 at (xDestStart,yDestStart) using mask0 as alpha for source
#--alpha is neither modified on dest0 nor used from src0
#/</summary>
#/<param name="mask0">must be same size as source</param>
def Draw(self, char* dest0, xDestStart, yDestStart, int dest_w, int dest_h, int dest_BytesPP, int dest_Stride, char* src0, int src_w, int src_h, int src_BytesPP, int src_Stride, char* mask0, int mask_BytesPP, int mask_Stride, int mask_Channel):
    bool bGood=True
    try
        if (PReporting.getIsMegaDebug()) cerr<<"Draw(dest,...,src,...,mask,...)..."<<flush
        unsigned int xSrcStart=0
        unsigned int ySrcStart=0
        if xDestStart<0:
            xSrcStart=0-xDestStart
            xDestStart=0

        if yDestStart<0:
            ySrcStart=0-yDestStart
            yDestStart=0

        unsigned int xSrc=xSrcStart
        unsigned int ySrc=ySrcStart
        unsigned int xDest=xDestStart
        unsigned int yDest=yDestStart
        float rCookedAlpha
        unsigned int iSrcChan
        unsigned int iDestChan
        #unsigned int Debug_PixelsDone=0;#debug only
        if dest0!=null:
            if src0!=null:
                if mask0!=null:
                    if (xDestStart>=0 and xDestStart<dest_w and yDestStart>=0 and yDestStart<dest_h
                            and xSrc>=0 and xSrc<src_w and ySrc>=0 and ySrc<src_w)
                        unsigned char* destLineLoc=&dest0[yDestStart*dest_Stride+xDestStart*dest_BytesPP]
                        unsigned char* srcLineLoc=&src0[ySrc*src_Stride+xSrc*src_BytesPP]
                        unsigned char* maskLineLoc=&mask0[mask_Channel+ySrc*mask_Stride+xSrc*mask_BytesPP]
                        unsigned char* destLoc
                        unsigned char* srcLoc
                        unsigned char* maskLoc
                        for (yDest=yDestStart; yDest<dest_h and ySrc<src_h; yDest++)
                            destLoc=destLineLoc
                            srcLoc=srcLineLoc
                            maskLoc=maskLineLoc
                            xSrc=xSrcStart
                            for (xDest=xDestStart; xDest<dest_w and xSrc<src_w; xDest++)
                                rCookedAlpha=(float)*maskLoc/255.0f
                                float rCookedInverseAlpha=1.0f-rCookedAlpha
                                iSrcChan=0
                                for (iDestChan=0; iDestChan<dest_BytesPP; iDestChan++)
                                    #alpha formula: (src-dest)*alpharatio+dest
                                    #for each channel of dest (<3 excludes alpha)
                                    if iDestChan<3:
                                        *destLoc=PMath.ByRound(  (float)( (float)(*srcLoc-*destLoc)*rCookedAlpha + (float)*destLoc )  )
                                        #*destLoc=PMath.ByRound(  (float)( rCookedInverseAlpha*(float)*destLoc + rCookedAlpha*(float)*srcLoc )  )

                                    if iSrcChan<src_BytesPP:
                                        iSrcChan++
                                        srcLoc++

                                    destLoc++

                                while (iSrcChan<src_BytesPP)
                                    iSrcChan++
                                    srcLoc++

                                maskLoc+=mask_BytesPP; #does NOT need to be incremented during pixel above since only 1 channel is needed
                                xSrc++
                                #Debug_PixelsDone++
                            }#end for xDest while xDest&sSrc both in range
                            destLineLoc+=dest_Stride
                            srcLineLoc+=src_Stride
                            maskLineLoc+=mask_Stride
                            ySrc++
                        }#end for yDest while yDest*ySrc both in range
                        if (PReporting.getIsMegaDebug()) Console.Error.WriteLine((string)"OK ("
                                    #+"Debug_PixelsDone:"+Convert.ToString(Debug_PixelsDone)
                                    +"; xDestStart:"+Convert.ToString(xDestStart)
                                    +"; yDestStart:"+Convert.ToString(yDestStart)
                                    +"; xDest:"+Convert.ToString(xDest)
                                    +"; yDest:"+Convert.ToString(yDest)
                                    +"; dest_w:"+Convert.ToString(dest_w)
                                    +"; dest_h:"+Convert.ToString(dest_h)
                                    +"; xSrcStart:"+Convert.ToString(xSrcStart)
                                    +"; ySrcStart:"+Convert.ToString(ySrcStart)
                                    +"; xSrc:"+Convert.ToString(xSrc)
                                    +"; ySrc:"+Convert.ToString(ySrc)
                                    +"; src_w:"+Convert.ToString(src_w)
                                    +"; src_h:"+Convert.ToString(src_h)
                                    +(string)")")
                    }#end if any pixels within range
                    else:
                        if PReporting.getIsMegaDebug():
                            Console.Error.WriteLine("Draw(dest,...,src,...,mask,...): no pixels within range")



                else Console.Error.WriteLine("Draw using mask buffer Error: null mask for source")

            else Console.Error.WriteLine("Draw using mask buffer Error: null source")

        else Console.Error.WriteLine("Draw using mask buffer Error: null destination")

    catch (exception& exn)
        bGood=False
        PReporting.ShowExn(exn,"drawing using mask buffer","PImage.Draw")

    return bGood
}#end Draw using mask buffer
}#end namespace

#endif