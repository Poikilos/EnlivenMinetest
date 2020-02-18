#ifndef COLORSPACETRANSFORM_CPP
#define COLORSPACETRANSFORM_CPP

#include "colorspacetransform.h"
#include "pstring.h"
#include "pmath.h"
#include "pimage.h"
#include <climits>
##define WIN32_LEAN_AND_MEAN
#include <windows.h>

namespace ProtoArmor
extern  char c255
float YCToRgb_fMaxY=-256.0f
float YCToRgb_fMaxU=-256.0f
float YCToRgb_fMaxV=-256.0f
float YCToRgb_fMinY=256.0f
float YCToRgb_fMinU=256.0f
float YCToRgb_fMinV=256.0f
float RgbToYC_fMaxY=-256.0f
float RgbToYC_fMaxU=-256.0f
float RgbToYC_fMaxV=-256.0f
float RgbToYC_fMinY=256.0f
float RgbToYC_fMinU=256.0f
float RgbToYC_fMinV=256.0f
float YCToRgb_byMaxR=-255
float YCToRgb_byMaxG=-255
float YCToRgb_byMaxB=-255
float YCToRgb_byMinR=255
float YCToRgb_byMinG=255
float YCToRgb_byMinB=255

def GetCurrentOrPrevFrameFor(self, sAnyFrameFile, iFrameCurrent):
    #NOTE: VirtualDub uses sint32 for current frame of source, dest, sequence
    string sReturn=sAnyFrameFile
    int iDesiredFrame=0
    int iSequenceDigits=0
    size_t stLastDot=sAnyFrameFile.find_last_of(".")
    if stLastDot!=string.npos:
         char* carrsAnyFrameFile=sAnyFrameFile.c_str()
        if  ((stLastDot-1)>=0) and IsDigit(carrsAnyFrameFile[stLastDot-1]) :
             int iLastDigit=stLastDot-1
            int iFirstDigit=iLastDigit
            int iChar=iFirstDigit
            while (iChar>=0)
                if  ((iFirstDigit-1)>=0) and IsDigit(carrsAnyFrameFile[iFirstDigit-1]) :
                    iFirstDigit--

                else:
                    break

                iChar--

            #OK to continue processing number since found at least one digit:
            iSequenceDigits=iLastDigit-iFirstDigit+1
            string sDotThenExt=sAnyFrameFile.substr(stLastDot)
            string sFileBaseName=sAnyFrameFile.substr(0,iFirstDigit)
            #cerr<<"looking for frame "<<iFrameCurrent<<" using name \""
            #cerr<<sFileBaseName
            #for (int iSeqDig=0; iSeqDig<iSequenceDigits; iSeqDig++)            #	cerr<<"?"
            #
            #cerr<<sDotThenExt<<"\" e.g. "<<(sFileBaseName+PString.SequenceDigits(iFrameCurrent,iSequenceDigits)+sDotThenExt)<<endl
            for (int iFrame=iFrameCurrent; iFrame>=0; iFrame--)
                string sFileTheoretical=sFileBaseName+PString.SequenceDigits(iFrame,iSequenceDigits)+sDotThenExt
                if  File.Exists(sFileTheoretical) :
                    sReturn=sFileTheoretical
                    #cerr<<"GetCurrentOrPrevFrameFor: "<<sReturn<<" FOUND"<<endl
                    break

                #else cerr<<"GetCurrentOrPrevFrameFor: "<<sFileTheoretical<<" NOT FOUND"<<endl

        }#if any digits found before last dot
    }#end if any extension for
    return sReturn
}#end GetCurrentOrPrevFrameFor

def IsDigit(self, val):
    bool bReturn=False
    for (int i=0; i<=9; i++)
        if val==PString.carrDigit[i]:
            bReturn=True
            break


    return bReturn
}#end IsDigit

def CopyPlaneToNonPlanar(self, char* dest, int DestChannelIndex, int dest_BytesPP, char* source, int source_Stride, int w, int h, bSamplesOnSecondLineOfSource):
    #assumes dest stride
    unsigned char* lpDestLineNow=dest
    lpDestLineNow+=DestChannelIndex
    unsigned char* lpSourceLineNow=source
    unsigned char* lpDestNow
    unsigned char* lpSourceNow
    unsigned int half_h=h/2
    if dest!=NULL:
        if source!=NULL:
            if w>0:
                unsigned int PixelsPerSourceSubsample=(int)((double)w/(double)source_Stride+.5); #+.5 to round since stride may be a little wide (e.g. extra 8 bytes can occurnot )
                #Console.Error.WriteLine("CopyPlaneToNonPlanar {PixelsPerSourceSubsample:"+Convert.ToString(PixelsPerSourceSubsample)+"; source_w: "+Convert.ToString(w)+"; source_Stride:"+Convert.ToString(source_Stride)+"; bSamplesOnSecondLineOfSource:"+Convert.ToString(bSamplesOnSecondLineOfSource)+";}");#debug only
                unsigned int iBuildUp=0
                #double source_PixelOffset=(double)source_Stride/(double)w;#unsigned int source_BytesPP=source_Stride/w; #can be less than 1 if subsampled; 1 or less since planar
                unsigned int dest_Stride=w*dest_BytesPP
                for (unsigned int y=0; y<half_h; y++)
                    lpDestNow=lpDestLineNow
                    lpSourceNow=lpSourceLineNow
                    for (unsigned int x=0; x<w; x++)
                        *lpDestNow=*lpSourceNow
                        lpDestNow+=dest_BytesPP
                        iBuildUp++
                        if iBuildUp>=PixelsPerSourceSubsample:
                            lpSourceNow++
                            iBuildUp=0

                    }#end for x
                    if (bSamplesOnSecondLineOfSource) lpSourceLineNow+=source_Stride
                    lpDestLineNow+=dest_Stride

                    lpDestNow=lpDestLineNow
                    lpSourceNow=lpSourceLineNow
                    for (unsigned int x=0; x<w; x++)
                        *lpDestNow=*lpSourceNow
                        lpDestNow+=dest_BytesPP
                        iBuildUp++
                        if iBuildUp>=PixelsPerSourceSubsample:
                            lpSourceNow++
                            iBuildUp=0

                    }#end for x
                    lpSourceLineNow+=source_Stride
                    lpDestLineNow+=dest_Stride
                }#end for y

            else cerr<<"CopyPlaneToNonPlanar Error: width 'w' was "<<w<<endl

        else cerr<<"CopyPlaneToNonPlanar Error: source was NULL"<<endl

    else cerr<<"CopyPlaneToNonPlanar Error: dest was NULL"<<endl
}#end CopyPlaneToNonPlanar

def CopyNonPlanarToPlane(self, char* dest, int dest_Stride, bSamplesOnSecondLineOfDest, char* source, int SourceChannelIndex, int source_BytesPP, int w, int h):
    #assumes dest stride
    unsigned char* lpSourceLineNow=source
    lpSourceLineNow+=SourceChannelIndex
    unsigned char* lpDestLineNow=dest
    unsigned char* lpSourceNow
    unsigned char* lpDestNow
    if dest!=NULL:
        if source!=NULL:
            if w>0:
                unsigned int PixelsPerDestSubsample=w/dest_Stride
                unsigned int iBuildUp=0
                #double source_PixelOffset=(double)source_Stride/(double)w;#unsigned int source_BytesPP=source_Stride/w; #can be less than 1 if subsampled; 1 or less since planar
                unsigned int dest_BytesPP=dest_Stride/w; #normally 1 if planar
                unsigned int source_Stride=w*source_BytesPP
                unsigned int half_h=h/2
                for (unsigned int y=0; y<half_h; y++)
                    lpSourceNow=lpSourceLineNow
                    lpDestNow=lpDestLineNow
                    for (unsigned int x=0; x<w; x++)
                        *lpDestNow=*lpSourceNow
                        lpSourceNow+=source_BytesPP
                        iBuildUp++
                        if iBuildUp>=PixelsPerDestSubsample:
                            lpDestNow+=dest_BytesPP
                            iBuildUp=0

                    }#end for x
                    if (bSamplesOnSecondLineOfDest) lpDestLineNow+=dest_Stride
                    lpSourceLineNow+=source_Stride

                    lpSourceNow=lpSourceLineNow
                    lpDestNow=lpDestLineNow
                    for (unsigned int x=0; x<w; x++)
                        *lpDestNow=*lpSourceNow
                        lpSourceNow+=source_BytesPP
                        iBuildUp++
                        if iBuildUp>=PixelsPerDestSubsample:
                            lpDestNow+=dest_BytesPP
                            iBuildUp=0

                    }#end for x
                    lpDestLineNow+=dest_Stride
                    lpSourceLineNow+=source_Stride
                }#end for y

            else cerr<<"CopyNonPlanarToPlane Error: width 'w' was "<<w<<endl

        else cerr<<"CopyNonPlanarToPlane Error: source was NULL"<<endl

    else cerr<<"CopyNonPlanarToPlane Error: dest was NULL"<<endl
}#end CopyNonPlanarToPlane

'''	void YUV4xxSubsampledPlanarToYUV444NonPlanar(unsigned char* dest, bAddDestAlpha, char* source, char* source_Stride, int source_J, int source_a, int source_b, int w, int h)		unsigned char* lpDestLineNow=dest
		unsigned char* lpSourceLineNow=source
		unsigned char* lpDestNow
		unsigned char* lpSourceNow
		for (yDest=0; yDest<h; yDest++)			lpDestNow=lpDestLineNow
			lpSourceNow=lpSourceLineNow
			for (int xDest=0; xDest<w; xDest++)				*lpDestNow=*lpSourceNow
				lpDestNow+=3
				lpSourceNow++
			}#end for xDest
			lpDestLineNow+=dest_Stride
			lpSourceLineNow+=w;#using w as stride assumes planar Y
		}#end for yDest
		#unsigned char* lpSourcePlaneNow=lpSourceNow
		unsigned int iBuildUp=0
		unsigned int source_chromaplane_stride=w*a/J; #e.g. 2/4 of w for 4:2:0 and 4:2:2, 1/4 for 4:1:0 and 4:1:1
		for (int chroma_plane=1; chroma_plane<=2; chroma_plane++)			lpDestNow=dest
			lpDestNow+=chroma_plane;#skip to V then U
			lpDestLineNow=lpDestNow
			#lpSourceLineNow is not reset since planar not intermingled channels
			for (int yDest=0; yDest<half_h; yDest++)				lpDestNow=lpDestLineNow
				lpSourceNow=lpSourceLineNow
				for (int xDest=0; xDest<w; xDest++)					*lpDestNow=*lpSourceNow
					lpDestNow+=3
					iBuildUp++
					if iBuildUp>=source_a:						lpSourceNow++
						iBuildUp=0

				}#end for xDest
				lpDestLineNow+=dest_Stride
				if (source_b>0) lpSourceLineNow+=source_chromaplane_stride; #assumes b is equal to a when b>0
				#else goes back to beginning of line and re-uses chroma line (starting at lpSourceNow=lpSourceLineNow below)

				lpDestNow=lpDestLineNow
				lpSourceNow=lpSourceLineNow
				for (int xDest=0; xDest<w; xDest++)					*lpDestNow=*lpSourceNow
					lpDestNow+=3
					iBuildUp++
					if iBuildUp>=source_a:						lpSourceNow++
						iBuildUp=0

				}#end for xDest
				lpDestLineNow+=dest_Stride
				lpSourceLineNow+=source_chromaplane_stride
			}#end for yDest
		}#end for chroma_plane
	}#end YUV4xxSubsampledToYUV444
'''
void RgbToYC(unsigned char &Y, char &U, char &V, char R, char G, char B)   #aka RGBToYUV
    #UNSIGNED TO PREVENT CASTING TO NEGATIVE

    #float declarations avoid redundant typecasts
    #--AND allow for writing back to exact same 3 bytes without interfering with U and V calculation


    #<http:#msdn.microsoft.com/en-us/library/ms893078.aspx> accessed 2010-03-03
    #Y = Convert.ToByte(  ( (  66 * R + 129 * G +  25 * B + 128) >> 8) +  16  )
    #U = Convert.ToByte(  ( ( -38 * R -  74 * G + 112 * B + 128) >> 8) + 128  )
    #V = Convert.ToByte(  ( ( 112 * R -  94 * G -  18 * B + 128) >> 8) + 128  )
    #These formulas produce 8-bit results using coefficients that require no more than 8 bits of (unsigned) precision. Intermediate results require up to 16 bits of precision.

    #VirtualDub author's formula (see TransformRGB32 function in sample plugin code):
    #r = R / 255.0f
    #g = G / 255.0f
    #b = B / 255.0f
    #y = 0.299f*r + 0.587f*g + 0.114f*b
    #u = 0.5f*(b - y)
    #v = 0.5f*(r - y)
    Y = Convert.ToByte(  (0.299*R + 0.587*G + 0.114*B) * 219.0/255.0 + 16.0  )
    U = Convert.ToByte(  (0.564*(B-Y)) * 224.0/255.0 + 128.0  );#Cb
    V = Convert.ToByte(  (0.713*(R-Y)) * 224.0/255.0 + 128.0  );#Cr

    #<http:#www.webkinesia.com/games/vcompress2.php> accessed 2010-03-03
    '''
    int r=R
    int g=G
    int b=B
    ##coefs summed to 65536 ( 1 << 16 ), Y is always within [0, 255]
    Y = Convert.ToByte( (19595*r + 38470*g + 7471*b ) >> 16)
    U = Convert.ToByte( ( 36962*(b-Y) ) >> 16 );#Cb
    V = Convert.ToByte( ( 46727*(r-Y) ) >> 16 );#Cr
    '''

    '''
    float fB=(float)b
    float fG=(float)g
    float fR=(float)r
    float fY=.299f*fR + .587f*fG + .114f*fB 
    float fU=-.16874f*fR - .33126f*fG + .5f*fB
    float fV=.5f*fR - .41869f*fG - .08131f*fB
    Y  = Convert.ToChar8( fY+.5 ); #+.5 for rounding
    U = Convert.ToChar8( fU+.5 ); #+.5 for rounding
    V = Convert.ToChar8( fV+.5 ); #+.5 for rounding
    '''
#ifdef CT_TESTLIMITS
    if (fY<RgbToYC_fMinY) RgbToYC_fMinY=fY
    if (fU<RgbToYC_fMinU) RgbToYC_fMinU=fU
    if (fV<RgbToYC_fMinV) RgbToYC_fMinV=fV
    if (fY>RgbToYC_fMaxY) RgbToYC_fMaxY=fY
    if (fU>RgbToYC_fMaxU) RgbToYC_fMaxU=fU
    if (fV>RgbToYC_fMaxV) RgbToYC_fMaxV=fV
#endif
}#end RgbToYC
void YCToRgb(unsigned char &R, char &G, char &B, char Y, char U, char V)   #aka YUVToRGB
    #UNSIGNED TO PREVENT CASTING TO NEGATIVE
    #-otherwise range becomes -128to127 (tested)
    #	if (Y<YCToRgb_fMinY) YCToRgb_fMinY=Y
    #	if (U<YCToRgb_fMinU) YCToRgb_fMinU=U
    #	if (V<YCToRgb_fMinV) YCToRgb_fMinV=V
    #	if (Y>YCToRgb_fMaxY) YCToRgb_fMaxY=Y
    #	if (U>YCToRgb_fMaxU) YCToRgb_fMaxU=U
    #	if (V>YCToRgb_fMaxV) YCToRgb_fMaxV=V

    #float declarations avoid redundant typecasts
    #--AND allow for writing back to exact same 3 bytes without interfering with g and b calculation

    #<http:#msdn.microsoft.com/en-us/library/ms893078.aspx> accessed 2010-03-03
    #C = (int)Y - 16
    #D = (int)U - 128
    #E = (int)V - 128
    #R = Convert.ToByte(( 298 * C           + 409 * E + 128) >> 8)
    #G = Convert.ToByte(( 298 * C - 100 * D - 208 * E + 128) >> 8)
    #B = Convert.ToByte(( 298 * C + 516 * D           + 128) >> 8)
    #(Convert.ToByte acts as clip)
    #Note   All units range from 0 (zero) to 1.0 (one). In DirectDraw, range from 0 to 255. Overflow and underflow can (and does) occur, the results must be saturated.

    #VirtualDub author's formula (see TransformRGB32 function in sample plugin code):
    float fY=(float)Y
    float fU=(float)U
    float fV=(float)V
    #the resulting tga using these has no perceivable difference from virtualdub screenshot:
    R = Convert.ToByte( 1.164*(fY-16.0f) + 1.596*(fV-128.0f) )
    G = Convert.ToByte( 1.164*(fY-16.0f) - 0.813*(fV-128.0f) - 0.391*(fU-128.0f) )
    B = Convert.ToByte( 1.164*(fY-16.0f) + 2.018*(fU-128.0f) )
    #	if Convert.ToByte(R)<YCToRgb_byMinR) YCToRgb_byMinR=Convert.ToByte(R:
    #	if Convert.ToByte(R)>YCToRgb_byMaxR) YCToRgb_byMaxR=Convert.ToByte(R:
    #	if Convert.ToByte(G)<YCToRgb_byMinG) YCToRgb_byMinG=Convert.ToByte(G:
    #	if Convert.ToByte(G)>YCToRgb_byMaxG) YCToRgb_byMaxG=Convert.ToByte(G:
    #	if Convert.ToByte(B)<YCToRgb_byMinB) YCToRgb_byMinB=Convert.ToByte(B:
    #	if Convert.ToByte(B)>YCToRgb_byMaxB) YCToRgb_byMaxB=Convert.ToByte(B:
    #y = (float)Y/255.0f
    #u = (float)U/255.0f
    #v = (float)V/255.0f
    #r = y + 1.402f*v
    #g = y - 0.714f*v - 0.344f*u
    #b = y + 1.772f*u
    #ir = (int)(0.5f + r*255.0f)
    #ig = (int)(0.5f + g*255.0f)
    #ib = (int)(0.5f + b*255.0f)
    #ir &= ~(ir >> 31)
    #ir |= (255 - ir) >> 31
    #ig &= ~(ig >> 31)
    #ig |= (255 - ig) >> 31
    #ib &= ~(ib >> 31)
    #ib |= (255 - ib) >> 31
    #B = Convert.ToByte(ib)
    #G = Convert.ToByte(ig)
    #R = Convert.ToByte(ir)
    #if (ir<YCToRgb_byMinR) YCToRgb_byMinR=ir
    #if (ir>YCToRgb_byMaxR) YCToRgb_byMaxR=ir
    #if (ig<YCToRgb_byMinG) YCToRgb_byMinG=ig
    #if (ig>YCToRgb_byMaxG) YCToRgb_byMaxG=ig
    #if (ib<YCToRgb_byMinB) YCToRgb_byMinB=ib
    #if (ib>YCToRgb_byMaxB) YCToRgb_byMaxB=ib



    #<http:#www.webkinesia.com/games/vcompress2.php> accessed 2010-03-03
    '''
    y = ( int ) Y << 16;	#same as multiply 65536
    int r=( y             + (int)91881 * V ) >> 16
    int g=( y  - (int)22544 * U - (int)46793 * V ) >> 16
    int b=( y  + (int) 116129 * U ) >> 16
    R = Convert.ToByte( ( y             + (int)91881 * V ) >> 16 )
    G = Convert.ToByte( ( y  - (int)22544 * U - (int)46793 * V ) >> 16 )
    B = Convert.ToByte( ( y  + (int) 116129 * U ) >> 16 )
    if ((float)Y<YCToRgb_fMinY) YCToRgb_fMinY=(float)Y
    if ((float)Y>YCToRgb_fMaxY) YCToRgb_fMaxY=(float)Y
    if ((float)U<YCToRgb_fMinU) YCToRgb_fMinU=(float)U
    if ((float)U>YCToRgb_fMaxU) YCToRgb_fMaxU=(float)U
    if ((float)V<YCToRgb_fMinV) YCToRgb_fMinV=(float)V
    if ((float)V>YCToRgb_fMaxV) YCToRgb_fMaxV=(float)V
    if (r<YCToRgb_byMinR) YCToRgb_byMinR=r
    if (r>YCToRgb_byMaxR) YCToRgb_byMaxR=r
    if (g<YCToRgb_byMinG) YCToRgb_byMinG=g
    if (g>YCToRgb_byMaxG) YCToRgb_byMaxG=g
    if (b<YCToRgb_byMinB) YCToRgb_byMinB=b
    if (b>YCToRgb_byMaxB) YCToRgb_byMaxB=b
    '''


    '''
    float fY=(float)Y
    float fU=(float)U
    float fV=(float)V
    r = Convert.ToChar8( fY + 1.402f*fV +.5); #+.5 for rounding
    g = Convert.ToChar8( fY - 0.34414f*fU - .71414f*fV +.5); #+.5 for rounding
    b = Convert.ToChar8( fY + 1.772f*fU +.5); #+.5 for rounding

    if (fY<YCToRgb_fMinY) YCToRgb_fMinY=fY
    if (fU<YCToRgb_fMinU) YCToRgb_fMinU=fU
    if (fV<YCToRgb_fMinV) YCToRgb_fMinV=fV
    if (fY>YCToRgb_fMaxY) YCToRgb_fMaxY=fY
    if (fU>YCToRgb_fMaxU) YCToRgb_fMaxU=fU
    if (fV>YCToRgb_fMaxV) YCToRgb_fMaxV=fV
    if (r<YCToRgb_byMinR) YCToRgb_byMinR=r
    if (g<YCToRgb_byMinG) YCToRgb_byMinG=g
    if (b<YCToRgb_byMinB) YCToRgb_byMinB=b
    if (r>YCToRgb_byMaxR) YCToRgb_byMaxR=r
    if (g>YCToRgb_byMaxG) YCToRgb_byMaxG=g
    if (b>YCToRgb_byMaxB) YCToRgb_byMaxB=b
    '''
}#end YCToRgb

void CopySurface_BitdepthSensitive(unsigned char* dest, int dest_BytesPP, int dest_Stride, char* source, int source_BytesPP, int source_Stride, int w, int h)   #formerly ChanToChan
    unsigned char* lpDestLoc
    unsigned char* lpDestLineLoc=dest
    unsigned char* lpSourceLoc
    unsigned char* lpSourceLineLoc=source
    unsigned int iSrcChan

    if source!=NULL:
        if dest!=NULL:
            for (unsigned int iLine=0; iLine<h; iLine++)
                lpSourceLoc=lpSourceLineLoc
                lpDestLoc=lpDestLineLoc
                for (unsigned int x=0; x<w; x++)
                    iSrcChan=0
                    for (unsigned int iDestChan=0; iDestChan<dest_BytesPP; iDestChan++)
                        *lpDestLoc=*lpSourceLoc
                        lpDestLoc++
                        if iSrcChan<source_BytesPP:
                            lpSourceLoc++
                            iSrcChan++


                    while (iSrcChan<source_BytesPP)
                        lpSourceLoc++
                        iSrcChan++

                }#end for x
                lpSourceLineLoc+=source_Stride
                lpDestLineLoc+=dest_Stride
            }#end for iLine

        else cerr<<"CopySurface_BitdepthSensitive Error: dest is NULL"<<endl

    else cerr<<"CopySurface_BitdepthSensitive Error: source is NULL"<<endl
    ''' #THE FOLLOWING is NOT pitch-sensitive
    unsigned char* lpDestNow=dest
    unsigned char* lpSourceNow=source
    unsigned int iSrcChan
    if source!=NULL:    	if dest!=NULL:    		for (unsigned int iPixel=0; iPixel<iTotalPixels; iPixel++)    			iSrcChan=0
    			for (unsigned int iDestChan=0; iDestChan<dest_BytesPP; iDestChan++)    				*lpDestNow=*lpSourceNow
    				if iSrcChan<source_BytesPP:    					lpSourceNow++
    					iSrcChan++


    			while (iSrcChan<source_BytesPP)    				lpSourceNow++
    				iSrcChan++



    	else cerr<<"CopySurface_BitdepthSensitive Error: dest is NULL"<<endl

    else cerr<<"CopySurface_BitdepthSensitive Error: source is NULL"<<endl
    '''
}#end CopySurface_BitdepthSensitive

def YUV444NonPlanarToRGB(self, char* dest, bDestHasAlphaChannel, bSetDestAlphaTo255_IgnoredIfNoDestAlpha, char* source, int iPixels):
    unsigned int chanY=0
    unsigned int chanU=1
    unsigned int chanV=2

    unsigned int chanB=0
    unsigned int chanG=1
    unsigned int chanR=2

    unsigned int dest_iBytesPP=bDestHasAlphaChannel?4:3
    unsigned char* lpDestNow=dest
    unsigned char* lpSourceNow=source
    for (unsigned int iPixel=0; iPixel<iPixels; iPixel++)
        YCToRgb(lpDestNow[chanR],lpDestNow[chanG],lpDestNow[chanB],lpSourceNow[chanY],lpSourceNow[chanU],lpSourceNow[chanV])
        lpSourceNow+=3
        lpDestNow+=3
        if bDestHasAlphaChannel:
            if (bSetDestAlphaTo255_IgnoredIfNoDestAlpha) *lpDestNow=c255
            lpDestNow++


}#end YUV444NonPlanarToRGB

def SaveRaw(self, sFile, char* buffer, iBytes):
    BinaryWriter streamOut( File.Open(sFile,FileMode.OpenWrite), True)
    streamOut.Write(buffer,0,iBytes)
    streamOut.Close()


def Heal_ToNearestPixel(self, char* dest0, int dest_BytesPP, int dest_Stride, char* mask0, int mask_BytesPP, int mask_Stride, int mask_Channel, int w, int h, rReachMultiplier_UNUSED, rRadialSampleSpacing_UNUSED, rDiffusionMultiplier):
    int chanB=0
    int chanG=(dest_BytesPP>1)?1:0;#if not grayscale set to next channel
    int chanR=(dest_BytesPP>1)?2:0;#if not grayscale set to next channel
    int chanA=(dest_BytesPP>=4)?3:0

    int dest_VisibleChannels=dest_BytesPP
    if (dest_VisibleChannels==4) dest_VisibleChannels=3
    int uiChan

    if dest0!=null:
        #if dest_BytesPP<4:        if mask0!=null:
            byte* lpDestLine=dest0
            #if (mask_BytesPP==4) lpMaskLine+=3;#move to alpha if alpha exists
            byte* lpDest
            byte* lpMaskLine=&mask0[mask_Channel]
            byte* lpMask
            double rNear_X;#near pixel that is nonzero in mask
            double rNear_Y;#near pixel that is nonzero in mask
            unsigned int Near_X;#near pixel that is nonzero in mask
            unsigned int Near_Y;#near pixel that is nonzero in mask
            #double fxFar;#far pixel to use as heal source (diffusable)
            #double fyFar;#far pixel to use as heal source (diffusable)
            bool bUsable=True
            int iHealed=0
            byte* lpSrcNow=dest0;#unsigned int dwSrc=0
            float fAlphaCooked
            float fAlphaCookedInverse
            for (unsigned int y=0; y<h; y++)
                lpMask=lpMaskLine
                lpDest=lpDestLine
                for (unsigned int x=0; x<w; x++)
                    if *lpMask>0)   #non-black pixel (to heal:
                        rNear_X=(double)x
                        rNear_Y=(double)y
                        if PImage.PushToNearest(rNear_X,rNear_Y,mask0,w,h,mask_BytesPP,mask_Stride,mask_Channel,1,False):
                            Near_X=(unsigned int)(rNear_X+.5f)
                            Near_Y=(unsigned int)(rNear_Y+.5f)
                            #if PReporting.getIsUltraDebug():                            #cerr<<"healing:("<<x<<","<<y<<"); found:("<<Near_X<<","<<Near_Y<<")"<<endl
                            #
                            lpSrcNow=&dest0[Near_Y*dest_Stride+Near_X*dest_BytesPP]
                            #if dest_BytesPP==4:
                            fAlphaCooked=(float)*lpMask/255.0f
                            #else fAlphaCooked=1.0f;#255.0f
                            fAlphaCookedInverse=1.0f-fAlphaCooked
                            for (uiChan=0; uiChan<dest_VisibleChannels; uiChan++)
                                #alpha formula: (src-dest)*alpharatio+dest
                                *lpDest = Convert.ToByte( ((float)lpSrcNow[uiChan]*fAlphaCookedInverse + (float)lpDest[uiChan]*fAlphaCooked) ); #*lpDest = Convert.ToByte( ((float)lpSrcNow[uiChan]-(float)lpDest[uiChan])*fAlphaCooked + (float)lpDest[uiChan] ); #memcpy(lpDest, &dest0[Near_Y*dest_Stride+Near_X*dest_BytesPP], dest_BytesPP); #memcpy(&dest0[y*dest_Stride+x*dest_BytesPP], &dest0[Near_Y*dest_Stride+Near_X*dest_BytesPP], dest_BytesPP)

                            iHealed++

                        else:
                            Console.Error.WriteLine("Heal error: no black pixels for color source")
                            bUsable=False
                            break

                    }#end if non-black pixel (to heal)
                    lpMask+=mask_BytesPP
                    lpDest+=dest_BytesPP
                }#end for x
                if (not bUsable) break
                lpMaskLine+=mask_Stride
                lpDestLine+=dest_Stride
            }#end for y
            if PReporting.getIsMegaDebug()) Console.Error.WriteLine("Finished Heal {iHealed:"+Convert.ToString(iHealed)+"; TotalPixels:"+Convert.ToString(w*h)+"; bUsable-background:"+Convert.ToString(bUsable)+"}":

        else Console.Error.WriteLine("Error in Heal: null mask")
        #}#end if dest_BytesPP<4

    else Console.Error.WriteLine("Error in Heal: null dest")
}#end Heal_ToNearestPixel

#int HealWithAvCache_X[2073600];#NOTE: 1920x1080=2073600
#int HealWithAvCache_Y[2073600];#NOTE: 1920x1080=2073600
#int HealWithAvCache_Count
# int HealWithAvCache_Max=2073600
bool bShowNegativeSpreadError=True
bool bShowAbsentBlackAreaInMaskError=True

#/<summary>
#/Gets a certain number of nearby background pixels where number is (rReachMultiplier*8.0+.5)+1.0).
#/rRadialSampleSpacing is ignored (self checks all nearest pixels limited to number determined as per formula above).
#/rDiffusionMultiplier is pixel radius for diffusion, is multiplied by 3
#/</summary>
def Heal_WithAveraging_Permutations(self, char* dest0, int dest_BytesPP, int dest_Stride, char* mask0, int mask_BytesPP, int mask_Stride, int mask_Channel, int w, int h, rReachMultiplier, rRadialSampleSpacing, rDiffusionMultiplier, bHorizonalSearch, bVerticalSearch):
    int chanB=0
    int chanG=(dest_BytesPP>1)?1:0;#if not grayscale set to next channel
    int chanR=(dest_BytesPP>1)?2:0;#if not grayscale set to next channel
    int chanA=(dest_BytesPP>=4)?3:0
    int iHealedTotal=0

    if PReporting.getIsMegaDebug) Console.Error.Write("Heal_WithAveraging_Permutations...":
    try
        unsigned int x
        unsigned int y
        PReporting.setParticiple("running heal")
        PMath.ResizePixelInfoCache(w*h,False)
        PMath.ResizeDistanceCache(w,h)
        PMath.ResizePointInfoCache((w>h)?w:h, bHorizonalSearch, bVerticalSearch)
        #PMath.ResizePointInfoCache((w>h)?w:h, bHorizonalSearch, bVerticalSearch);#ResizePointInfoCache(int iRadius)
        # (cutoff of cache is determined manually below by quantity of background pixels found,
        # so self program doesn't need a radius-based cutoff anywhere).
        #PMath.ppxiCache_Used=0
        #pfDistCache[x][y]
        #PMath.ppxiCache[PMath.ppxiCache_Used]
        unsigned int uiMaskLine=mask_Channel
        unsigned int uiMaskLoc
        unsigned int uiDestLine=0
        unsigned int uiDestLoc
        bool bLineOnly=( not bHorizonalSearch or not bVerticalSearch )
        unsigned int uiPixelsToGet=bLineOnly ? (4) : ( (unsigned int)( (rReachMultiplier*8.0+.5) + 1.0 ) )
        PReporting.setParticiple("finished setting uiPixelsToGet (for getting average background color) to "+Convert.ToString(uiPixelsToGet-1)+"(+1)")
        unsigned int iPointInfoNow
        POINTINFO* lppiNow=NULL
        float rNearestBGDist=FLT_MAX
        float rFarthestBGDist=0
        float fWeightNow
        unsigned int uiChan
        int iW=(int)w
        int iH=(int)h
        #uiMaskLoc=0
        #uiDestLoc=0
        float rCookedAlpha
        float rInverseAlpha
        float rDestTemp
        unsigned int iMatchNow
        float farrHeavyPixel[4]
        float fTotalWeight;#needed since e.g. if ther are two background pixels, red channels are 255 are 255 ends up being 255+0 where 0 is farthest pixel (since multiplied by weight of 0 since farthest)--total weight would be 1.0, in 255/1, is 255
        PReporting.setParticiple("processing destination")
        for (y=0; y<h; y++)
            #TODO: debug performance--use pointers and remove uiMaskLoc AND uiDestLoc
            uiMaskLoc=uiMaskLine
            uiDestLoc=uiDestLine
            if PReporting.getIsUltraDebug():
                Console.Write("y "+Convert.ToString(y)+":")
                Console.Out.Flush()

            for (x=0; x<w; x++)
                if PReporting.getIsUltraDebug():
                    Console.Write("("+Convert.ToString(x)+")")
                    Console.Out.Flush()

                if mask0[uiMaskLoc]>0:
                    PMath.ppxiCache_Used=0
                    iPointInfoNow=0;#ptcachebydistanceNow.Seek(0)
                    for (iPointInfoNow=0; iPointInfoNow<PMath.ppiCache_Used; iPointInfoNow++)  #while (not ptcachebydistanceNow.getFinished())                        #NOTE: no distance cutoff is needed since self method is capped by #of background pixels collected!
                        lppiNow=&PMath.ppiCache[iPointInfoNow];#ptcachebydistanceNow.NextPointInfo()
                        if lppiNow!=NULL:
                            #use the point cache to find surrounding pixels, sign to get all reflections:
                            #--the point info cache should already only contain pixels in the search area (bHorizonalSearch, bVerticalSearch, both)
                            for (int ySign=-1; bVerticalSearch?(ySign<=1):(ySign==-1); ySign+=2)   #==-1 ok since if bVerticalSearch, should already always be 0 in pointinfocache
                                for (int xSign=-1; bHorizonalSearch?(xSign<=1):(xSign==-1); xSign+=2)
                                    #int xOffset=lppiNow.x*xSign
                                    #int yOffset=lppiNow.y*ySign
                                    int xPointTheoretical=(int)x+lppiNow.x*xSign
                                    int yPointTheoretical=(int)y+lppiNow.y*ySign
                                    if (		xPointTheoretical<iW
                                                and yPointTheoretical<iH
                                                and xPointTheoretical>=0
                                                and yPointTheoretical>=0 )
                                        int mask_indexTheoretical=yPointTheoretical*mask_Stride+xPointTheoretical*mask_BytesPP+mask_Channel
                                        if (mask0[mask_indexTheoretical]==0)  #IS background at theoretical location
                                            int dest_indexTheoretical=yPointTheoretical*dest_Stride+xPointTheoretical*dest_BytesPP
                                            memcpy(PMath.ppxiCache[PMath.ppxiCache_Used].data, &dest0[dest_indexTheoretical], dest_BytesPP); #for (int uiChan=0; uiChan<dest_BytesPP; uiChan++) {	PMath.ppxiCache[PMath.ppxiCache_Used].data[uiChan]=dest_indexTheoretical;
                                            PMath.ppxiCache[PMath.ppxiCache_Used].distance=lppiNow.fDist
                                            if (PMath.ppxiCache[PMath.ppxiCache_Used].distance>rFarthestBGDist) rFarthestBGDist=PMath.ppxiCache[PMath.ppxiCache_Used].distance
                                            if (PMath.ppxiCache[PMath.ppxiCache_Used].distance<rNearestBGDist) rNearestBGDist=PMath.ppxiCache[PMath.ppxiCache_Used].distance
                                            PMath.ppxiCache_Used++


                                    if (PMath.ppxiCache_Used>=uiPixelsToGet) break

                                if (PMath.ppxiCache_Used>=uiPixelsToGet) break

                            if (PMath.ppxiCache_Used>=uiPixelsToGet) break
                        }#end if lppiNow!=NULL
                        else:
                            Console.Error.WriteLine("Error: NULL pointinfo in cachenot ")
                            break

                    }#end while there are permutatable points in ptcachebydistanceNow using the given range
                    if (PMath.ppxiCache_Used>=2)  #both a min and max location are needed since weight of far pixel is zero!
                        float rSpreadBGDistance=rFarthestBGDist-rNearestBGDist
                        if rSpreadBGDistance>0:
                            fTotalWeight=0.0f;#needed since e.g. if ther are two background pixels, red channels are 255 are 255 ends up being 255+0 where 0 is farthest pixel (since multiplied by weight of 0 since farthest)--total weight would be 1.0, in 255/1, is 255
                            for (uiChan=0; uiChan<dest_BytesPP; uiChan++)
                                farrHeavyPixel[uiChan]=0.0f

                            for (iMatchNow=0; iMatchNow<PMath.ppxiCache_Used; iMatchNow++)
                                #fWeightNow should approach 1 as background pixel's distance approaches that of the nearest one
                                fWeightNow=(  '''PMath.ppxiCache[iMatchNow].weight='''1.0f  -  ( (PMath.ppxiCache[iMatchNow].distance-rNearestBGDist) / rSpreadBGDistance )  )
                                fTotalWeight+=fWeightNow
                                for (uiChan=0; uiChan<dest_BytesPP; uiChan++)
                                    farrHeavyPixel[uiChan]+=(float)PMath.ppxiCache[iMatchNow].data[uiChan]*fWeightNow


                            rCookedAlpha=(float)mask0[uiMaskLoc]/255.0f
                            rInverseAlpha=1.0f-rCookedAlpha
                            for (uiChan=0; uiChan<dest_BytesPP; uiChan++)
                                rDestTemp=(float)dest0[uiDestLoc+uiChan]
                                dest0[uiDestLoc+uiChan]=PMath.ByRound( rDestTemp*rInverseAlpha + (farrHeavyPixel[uiChan]/fTotalWeight)*rCookedAlpha )
                                #source is (unsigned char)(farrHeavyPixel[uiChan]/(fTotalWeight)+.5f);#+.5 for rounding

                            iHealedTotal++

                        else:
                            string sMsg="  ("+Convert.ToString(x)+","+Convert.ToString(y)+"): NO background for healing pixel (negative spread of "+Convert.ToString(rSpreadBGDistance)+")not  {sources:"+Convert.ToString(PMath.ppiCache_Used)+"}"
                            Console.Error.WriteLine(sMsg)
                            if bShowNegativeSpreadError:
                                #int iResult=
                                MessageBox(NULL'''hWnd''',sMsg.c_str(),"SpatialForegroundRemover.Heal",NULL);#MB_OK)
                                #DialogResult dlgresult=MessageBox.Show(sMsg)
                                bShowNegativeSpreadError=False



                    else:
                        string sMsg="only "+Convert.ToString(PMath.ppxiCache_Used)+" (NOT ENOUGH) pixels for heal (no black pixels in mask specifying background in dest; "+Convert.ToString(PMath.ppiCache_Used)+" cached points; searched starting from "+Convert.ToString(x)+","+Convert.ToString(y)+")not "
                        Console.Error.WriteLine(sMsg)
                        if bShowAbsentBlackAreaInMaskError:
                            #int iResult=
                            MessageBox(NULL'''hWnd''',sMsg.c_str(),"SpatialForegroundRemover.Heal",NULL);#MB_OK)
                            #DialogResult dlgresult=MessageBox.Show(sMsg)
                            bShowAbsentBlackAreaInMaskError=False


                }#end if nonzero at self point in mask, fix using nearby pixels where mask is zero
                uiMaskLoc+=mask_BytesPP
                uiDestLoc+=dest_BytesPP
            }#end for x
            if PReporting.getIsUltraDebug()) Console.WriteLine(:
            Console.WriteLine()
            uiMaskLine+=mask_Stride
            uiDestLine+=dest_Stride
        }#end for y
        if PReporting.getIsMegaDebug()) Console.Error.WriteLine("done. {iHealedTotal:"+Convert.ToString(iHealedTotal)+"}":

    catch (exception& exn)
        PReporting.ShowExn(exn)

    catch (...)
        PReporting.ShowUnknownExn("Heal_WithAveraging_Permutations")

    PMath.ppxiCache_Used=0
    bool bRandom=False
    int iDiffusionRadius=(int)( (rDiffusionMultiplier*3.0+.5) )
    #if rDiffusionMultiplier==0.0:
    #	iDiffusionRadius=0
    Console.Error.WriteLine("rDiffusionMultiplier:"+Convert.ToString(rDiffusionMultiplier))
    Console.Error.WriteLine("iDiffusionRadius:"+Convert.ToString(iDiffusionRadius))
    PReporting.setParticiple("finished Heal")
    if iDiffusionRadius>0) Diffuse(dest0, w, h, dest_BytesPP, dest_Stride, 0, 0, mask0, w, h, mask_BytesPP, mask_Stride, mask_Channel, iDiffusionRadius, bRandom:
}#end Heal_WithAveraging_Permutations
def Diffuse(self, char* dest0, int dest_w, int dest_h, int dest_BytesPP, int dest_Stride, to_Left, to_Top, char* brush0, int brush_w, int brush_h, int brush_BytesPP, int brush_Stride, int brush_Channel, iRadius, bRandom):
    if PReporting.getIsMegaDebug():
        Console.Error.WriteLine("Starting diffuse...")
        Console.Out.Flush()

    unsigned int uiDestLine
    unsigned int uiDestLoc
    unsigned int uiBrushLine
    unsigned int uiBrushLoc
    unsigned int xDest
    unsigned int yDest=to_Top
    double rPixelRadius=(double)iRadius
    int xBrushStart
    if (to_Left<0) xBrushStart=to_Left*-1
    else xBrushStart=0
    int yBrushStart
    if (to_Top<0) yBrushStart=to_Top*-1
    else yBrushStart=0
    PReporting.setParticiple("diffusing using brush")
    byte byarrColor[4]
    #for (int i=0; i<4; i++)    #	byarrColor[i]=0
    #
    int iFibboLimit=INT_MAX/2
    int iFibboTemp
    int iFibboPrev=0
    int iFibbo=1
    int iFibboStart=377;#go past 360 to make angles seem more random after modulus 360
    int iFibboStartPrev=233
    #fibbonocci set begins with: 0,1,1,2,3,5,8,13,21,34,55,89,144,233,377
    iFibboStartPrev=iFibboStartPrev;#0
    iFibbo=iFibboStart;#1
    #while (iFibbo<240) { #go past 240 to make angles seem more random after modulus 360
    #	iFibboTemp=iFibbo
    #	iFibbo=iFibbo+iFibboPrev
    #	if iFibbo<iFibboLimit:    #		iFibboPrev=iFibboTemp
    #
    #	else:
    #		iFibbo=1
    #		iFibboPrev=0
    #
    #
    #int iDiameterInclusive=iRadius*2+1;#inclusive diameter e.g. radius 1 makes a 3-pixel-wide square range
    int iPixelsRadiusEx=iRadius+1;#exclusive so can be used for modulus operations
    float rDistDiffused
    float rAngleDiffused
    int xDiffused
    int yDiffused
    int iChan
    byte* lpDestDiffusedBrushColor
    byte* lpDestNow
    float rCookedAlpha
    float rInverseAlpha
    try
        uiDestLine=to_Left*dest_Stride
        uiBrushLine=yBrushStart*brush_Stride+xBrushStart*brush_BytesPP+brush_Channel
        for (int yBrush=yBrushStart; yBrush<brush_h; yBrush++)  #do not stop at bounds, fibbo will be non-deterministic near edges
            if yBrush>=0 and yDest>=0 and yDest<dest_h:
                uiDestLoc=uiDestLine
                uiBrushLoc=uiBrushLine
                xDest=to_Left
                for (int xBrush=xBrushStart; xBrush<brush_w; xBrush++)  #do not stop at bounds, fibbo will be non-deterministic near edges
                    if xBrush>=0 and xDest>=0 and xDest<dest_w and brush0[uiBrushLoc]>0:
                        #subtracting PixelRadius makes probability sets like {0,1,2} into {-1,0,1
                        if not bRandom:
                            rDistDiffused=(float)(iFibbo%iPixelsRadiusEx)
                            rAngleDiffused=(float)(iFibbo%360)
                            xDiffused=xDest+(int)(PMath.XOfRThetaDeg(rDistDiffused,rAngleDiffused)+.5f); #xDiffused=x+(iFibbo%iDiameterInclusive-iRadius)
                            yDiffused=yDest+(int)(PMath.YOfRThetaDeg(rDistDiffused,rAngleDiffused)+.5f); #yDiffused=y+(iFibboPrev%iDiameterInclusive-iRadius)

                        else:
                            rDistDiffused=(float)(rand()%iPixelsRadiusEx)
                            rAngleDiffused=(float)(rand()%360)
                            xDiffused=xDest+(int)(PMath.XOfRThetaDeg(rDistDiffused,rAngleDiffused)+.5f); #xDiffused=x+(rand()%iDiameterInclusive-iRadius)
                            yDiffused=yDest+(int)(PMath.YOfRThetaDeg(rDistDiffused,rAngleDiffused)+.5f); #yDiffused=y+(rand()%iDiameterInclusive-iRadius)

                        if (xDiffused<0) xDiffused=0
                        elif (xDiffused>=dest_w) xDiffused=dest_w-1
                        if (yDiffused<0) yDiffused=0
                        elif (yDiffused>=dest_h) yDiffused=dest_h-1

                        #uiDiffusedDestLoc=yDiffused*w+xDiffused
                        lpDestNow=&dest0[yDiffused*dest_Stride+xDiffused*dest_BytesPP]
                        lpDestDiffusedBrushColor=&dest0[uiDestLoc]
                        #alpha is brush0[uiBrushLoc]
                        rCookedAlpha=(float)brush0[uiBrushLoc]/255.0f
                        rInverseAlpha=1.0f-rCookedAlpha
                        for (iChan=0; iChan<dest_BytesPP; iChan++)
                            *lpDestNow=(unsigned char)( (float)*lpDestNow*rInverseAlpha + (float)*lpDestDiffusedBrushColor*rCookedAlpha + .5f )
                            lpDestNow++
                            lpDestDiffusedBrushColor++

                    }#end if within bounds
                    if not bRandom:
                        iFibboTemp=iFibbo
                        iFibbo=iFibbo+iFibboPrev
                        if iFibbo<iFibboLimit:
                            iFibboPrev=iFibboTemp

                        else:
                            iFibbo=iFibboStart
                            iFibboPrev=iFibboStartPrev


                    uiBrushLoc+=brush_BytesPP
                    uiDestLoc+=dest_BytesPP
                    xDest++
                }#end for xBrush
            }#end if line is in bounds
            else:
                #preserve non-random behavior even if line is skipped
                if not bRandom:
                    for (int xBrush=xBrushStart; xBrush<brush_w; xBrush++)
                        iFibboTemp=iFibbo
                        iFibbo=iFibbo+iFibboPrev
                        if iFibbo<iFibboLimit:
                            iFibboPrev=iFibboTemp

                        else:
                            iFibbo=iFibboStart
                            iFibboPrev=iFibboStartPrev



            }#end else line is out of bounds
            uiDestLine+=dest_Stride
            uiBrushLine+=brush_Stride
            yDest++
        }#end for yBrush
        Console.Error.WriteLine("OK (Diffuse)")

    catch (exception& exn)
        PReporting.ShowExn(exn)

    catch (...)
        PReporting.ShowUnknownExn("Heal_WithAveraging_Permutations")

}#end Diffuse
def Heal_WithAveraging_Sequential(self, char* dest0, int dest_BytesPP, int dest_Stride, char* mask0, int mask_BytesPP, int mask_Stride, int mask_Channel, int w, int h, rReachMultiplier, rRadialSampleSpacing, rDiffusionMultiplier):
    #TODO: return False if there are no zero mask pixels (which correspond usable background pixels in dest)
    int chanB=0
    int chanG=(dest_BytesPP>1)?1:0;#if not grayscale set to next channel
    int chanR=(dest_BytesPP>1)?2:0;#if not grayscale set to next channel
    int chanA=(dest_BytesPP>=4)?3:0;#if
    #NOTE: mask is always used as alpha so dest0 does NOT need to be dest_BytesPP==4
    if rRadialSampleSpacing<=0.0) rRadialSampleSpacing=1.0/360.0; #1/360.0=~0.00278 (repeating 7:
    elif (rRadialSampleSpacing>360.0) rRadialSampleSpacing=360.0
    unsigned int uiRadialSamples=(unsigned int)(360.0/rRadialSampleSpacing)
    if ((double)uiRadialSamples*rRadialSampleSpacing==360.0) uiRadialSamples--; #prevents 360 from repeating location of 0 degrees
    if (uiRadialSamples<1) uiRadialSamples=1
    if (PReporting.getIsMegaDebug()) cerr<<"Heal...w:"<<w<<"...h:"<<h<<"...uiRadialSamples:"<<uiRadialSamples<<"..."<<flush
    unsigned int unfiltered_Used;#unsigned int unfiltered_angleq_Used
    #unsigned int unfiltered_angleq_Max=uiRadialSamples
    double* unfiltered_angleq=null
    unfiltered_angleq=(double*)malloc(sizeof(double)*uiRadialSamples)
    #unsigned int unfiltered_nonreached_distanceq_Used
    #unsigned int unfiltered_nonreached_distanceq_Max=0
    double* unfiltered_nonreached_distanceq=null
    unfiltered_nonreached_distanceq=(double*)malloc(sizeof(double)*uiRadialSamples)
    #unsigned int unfiltered_reached_Used
    #unsigned int unfiltered_reached_Max=0
    double* unfiltered_reached_pointq_rqX=null
    unfiltered_reached_pointq_rqX=(double*)malloc(sizeof(double)*uiRadialSamples)
    double* unfiltered_reached_pointq_rqY=null
    unfiltered_reached_pointq_rqY=(double*)malloc(sizeof(double)*uiRadialSamples)
    #nearpointq is the point before reach and diffusion is applied--exists to avoid redundant points
    #unsigned int unfiltered_nonreached_pointqUsed
    #unsigned int unfiltered_nonreached_pointqMax=0
    unsigned int* unfiltered_nonreached_pointq_rqX=null
    unfiltered_nonreached_pointq_rqX=(unsigned int*)malloc(sizeof(unsigned int)*uiRadialSamples)
    unsigned int* unfiltered_nonreached_pointq_rqY=null
    unfiltered_nonreached_pointq_rqY=(unsigned int*)malloc(sizeof(unsigned int)*uiRadialSamples)
    double* unfiltered_reached_distq=null
    unfiltered_reached_distq=(double*)malloc(sizeof(double)*uiRadialSamples)

    unsigned int filtered_Used
    unsigned int* filtered_indexq=null
    filtered_indexq=(unsigned int*)malloc(sizeof(unsigned int)*uiRadialSamples)
    #unsigned int unfiltered_byqUsed
    double* unfiltered_Weight=null
    unfiltered_Weight=(double*)malloc(sizeof(double)*uiRadialSamples)
    byte* unfiltered_byqB=null
    unfiltered_byqB=(byte*)malloc(uiRadialSamples)
    byte* unfiltered_byqG=null
    unfiltered_byqG=(byte*)malloc(uiRadialSamples)
    byte* unfiltered_byqR=null
    unfiltered_byqR=(byte*)malloc(uiRadialSamples)
    byte* unfiltered_byqA=null
    unfiltered_byqA=(byte*)malloc(uiRadialSamples)

    double unfiltered_rCumulativeDistance=0.0

    #double ClosestEvenIfOutlier_Dist=DBL_MAX
    #byte ClosestEvenIfOutlier_B=0
    #byte ClosestEvenIfOutlier_G=0
    #byte ClosestEvenIfOutlier_R=0
    #byte ClosestEvenIfOutlier_A=0

    if dest0!=null:
        #if dest_BytesPP<4:        if mask0!=null:
            byte* lpDestLine=dest0
            #if (mask_BytesPP==4) lpMaskLine+=3;#move to alpha if alpha exists
            byte* lpDest
            byte* lpMaskLine=&mask0[mask_Channel]
            byte* lpMask
            double rNear_X;#near pixel that is nonzero in mask
            double rNear_Y;#near pixel that is nonzero in mask
            #double fxFar;#far pixel to use as heal source (diffusable)
            #double fyFar;#far pixel to use as heal source (diffusable)
            for (unsigned int y=0; y<h; y++)
                lpMask=lpMaskLine
                lpDest=lpDestLine
                for (unsigned int x=0; x<w; x++)
                    if *lpMask!=0)   #non-black pixel (to heal:
                        if (PReporting.getIsMegaDebug()) cerr<<endl<<"  heal:"<<x<<","<<y<<"..."<<flush
                        double rAngleNow=0.0
                        #unsigned int iPrev_X=-1
                        #unsigned int iPrev_Y=-1
                        unfiltered_Used=0
                        filtered_Used=0
                        #unfiltered_angleq_Used=0
                        #unfiltered_nonreached_distanceq_Used=0
                        #unfiltered_reached_Used=0
                        #unfiltered_nonreached_pointqUsed=0
                        #filtered_indexq_Used=0
                        #unfiltered_byqUsed=0
                        for (unsigned int uiRadialSampleNow=0; uiRadialSampleNow<uiRadialSamples; uiRadialSampleNow++)
                            #for each radial sample
                            #queue vars:
                            #unfiltered_angleq_Used, unfiltered_angleq_Y, unfiltered_angleq_Y
                            #unfiltered_nonreached_distanceq_Used, unfiltered_nonreached_distanceq_Y, unfiltered_nonreached_distanceq_Y
                            #unfiltered_reached_Used, unfiltered_reached_pointq_rqY, unfiltered_reached_pointq_rqY
                            #unfiltered_nonreached_pointqUsed, unfiltered_nonreached_pointq_rqY, unfiltered_nonreached_pointq_rqY
                            #unfiltered_byqB, unfiltered_byqG, unfiltered_byqR, unfiltered_byqA
                            #methods:
                            #HavePoint(haystack_X, haystack_Y, haystack_Count, xNeedle, yNeedle)
                            rNear_X=x
                            rNear_Y=y
                            #Find nearest zero pixel in mask channel mask_Channel (usable background pixel)
                            #--intentionally edit near pixel
                            #PushToNearest(double& xStart, yStart, rDirection_Deg, mask, int mask_w, int mask_h, int mask_BytesPP, int mask_Stride, int mask_Channel, mask_Threshold, bGreaterThanThreshold_FalseForLessThan)
                            bool bFoundZeroBeforeEdge=PImage.PushToNearest(rNear_X,rNear_Y,rAngleNow,mask0,w,h,mask_BytesPP,mask_Stride,mask_Channel,1,False)
                            #use PMath.HavePoint to avoid duplication of first and last#bool bRoundsToSamePixAsPrev=((unsigned int)(rNear_X+.5)==iPrev_X)and((unsigned int)(rNear_Y+.5)==iPrev_Y)

                            #iPrev_X=(unsigned int)(rNear_X+.5)
                            #iPrev_Y=(unsigned int)(rNear_Y+.5)
                            if (bFoundZeroBeforeEdge
                                    and not PMath.HavePoint(unfiltered_nonreached_pointq_rqX,unfiltered_nonreached_pointq_rqY,unfiltered_Used,rNear_X,rNear_Y) )  #PMath.HavePoint(unfiltered_nonreached_pointq_rqX, unfiltered_nonreached_pointq_rqY, unfiltered_nonreached_pointqUsed, rNear_X, rNear_Y))                                unfiltered_nonreached_pointq_rqX[unfiltered_Used]=rNear_X
                                unfiltered_nonreached_pointq_rqY[unfiltered_Used]=rNear_Y
                                #NOTE: already fixed location above (rNear_X,rNear_Y)
                                #unfiltered_nonreached_pointqUsed++;#do ONCE for pair of x, coordinates above
                                unfiltered_nonreached_distanceq[unfiltered_Used]=PMath.Dist(x,y,rNear_X,rNear_Y)
                                unfiltered_rCumulativeDistance=unfiltered_nonreached_distanceq[unfiltered_Used]
                                #unfiltered_nonreached_distanceq_Used++
                                #Set far to CENTER then move far by reach factor then move back to nearest zero pixel if necessary
                                #fxFar=x;#center
                                #fyFar=y;#center
                                #CAN'T DO REACH YET because average is needed#PMath.Approach(fxFar, fyFar, rNear_X, rNear_Y, rReachMultiplier+1.0);#ok since starts at x,y; +1.0 to start at rNear_X, but use distance of (x,y) to (rNear_X,rNear_Y)
                                #unfiltered_reached_pointq_rqX[unfiltered_Used]=fxFar
                                #unfiltered_reached_pointq_rqY[unfiltered_Used]=fyFar
                                #unfiltered_reached_Used++
                                unfiltered_angleq[unfiltered_Used]=rAngleNow
                                unfiltered_Used++;#unfiltered_angleq_Used++
                            }#end if do not already have self starting radial pixel location
                            rAngleNow+=rRadialSampleSpacing
                        }#end for iAngle in unfiltered_angleq
                        if (PReporting.getIsMegaDebug()) cerr<<"unfiltered_Used:"<<unfiltered_Used<<"..."<<flush

                        #3. get average distance using count and cumulative distance found
                        double unfiltered_rAvgDist=unfiltered_rCumulativeDistance/(double)unfiltered_Used
                        if (PReporting.getIsMegaDebug()) cerr<<"unfiltered_rAvgDist:"<<unfiltered_rAvgDist<<"..."<<flush

                        #4. collect near pixels that are at or below average distance
                        for (unsigned int unfiltered_index=0; unfiltered_index<unfiltered_Used; unfiltered_index++)
                            if unfiltered_nonreached_distanceq[unfiltered_index]<=unfiltered_rAvgDist:
                                filtered_indexq[filtered_Used]=unfiltered_index
                                filtered_Used++
                            }#if pixel is close enough
                        }#end for all pixels, by distance
                        if (PReporting.getIsMegaDebug()) cerr<<"filtered_Used:"<<filtered_Used<<"..."<<flush
                        #--if there are fewer than one, the nearest one
                        if filtered_Used<=0)  #unfiltered_nonreached_pointqUsed<=0:                            if (PReporting.getIsMegaDebug()) cerr<<"0 so getting nearest out of "<<unfiltered_Used<<"..."<<flush
                            double unfiltered_closest_Dist=DBL_MAX
                            int unfiltered_closest_index=-1
                            for (unsigned int unfiltered_index=0; unfiltered_index<unfiltered_Used; unfiltered_index++)
                                if unfiltered_nonreached_distanceq[unfiltered_index]<unfiltered_closest_Dist:
                                    unfiltered_closest_Dist=unfiltered_nonreached_distanceq[unfiltered_index]
                                    unfiltered_closest_index=(int)unfiltered_index


                            if unfiltered_closest_index>=0:
                                filtered_indexq[filtered_Used]=unfiltered_closest_index
                                if (PReporting.getIsMegaDebug()) cerr<<"closest:("<<unfiltered_nonreached_pointq_rqX[unfiltered_closest_index]<<","<<unfiltered_nonreached_pointq_rqY[unfiltered_closest_index]<<")..."<<flush
                                filtered_Used++

                            if (PReporting.getIsMegaDebug()) cerr<<"now have filtered_Used:"<<filtered_Used<<"; unfiltered_closest_Dist:"<<unfiltered_closest_Dist<<"..."<<flush

                        #--randomize corresponding far location by diffusion factor then move back to nearest zero pixel if necessary

                        #5. get average dist of filtered pixels
                        double filtered_rCumulativeDistance=0.0
                        for (unsigned int filtered_index=0; filtered_index<filtered_Used; filtered_Used++)
                            filtered_rCumulativeDistance+=unfiltered_nonreached_distanceq[filtered_indexq[filtered_index]]

                        double filtered_rAvgDist=filtered_rCumulativeDistance/(double)filtered_Used
                        if (PReporting.getIsMegaDebug()) cerr<<"filtered_rAvgDist:"<<filtered_rAvgDist<<"..."<<flush

                        #6. for each filtered pixel found
                        #  a. modify by reach (wait until now since need filtered_rAvgDist)
                        #  b. modify by diffusion (same diffusion (x,y) offset for every radial sample)
                        #  c. collect min & max
                        double rMaxDist=-1
                        double rMinDist=DBL_MAX;#DBL_MAX or DOUBLE_MAX, in <climits> (formerly limits.h) or <cmath> (formerly math.h) or <cfloat> (formerly float.h)
                        #double xOff
                        #double yOff
                        #double rAngleNow
                        int iDiffusionRad=(int)(rDiffusionMultiplier*filtered_rAvgDist+.5)
                        int iDiffusionSpread=iDiffusionRad*2+1; #+1 since if -1 to 1 then range is 3 (-1,0,1) which results in 0,1, after modulus by iDiffusionSpread
                        #subtract radius below since 1 needs to be subtracted from (0,1,2) to get (-1,0,1)
                        double DiffuseAllRadialSamples_X=(double)( PMath.Abs(rand())%iDiffusionSpread-iDiffusionRad )
                        double DiffuseAllRadialSamples_Y=(double)( PMath.Abs(rand())%iDiffusionSpread-iDiffusionRad )
                        for (unsigned int filtered_index=0; filtered_index<filtered_Used; filtered_index++)
                            unsigned int unfiltered_index=filtered_indexq[filtered_index]
                            #--starting at near pixel, away from center by rReachMultiplier toward pixel at unfiltered_rAvgDist from near pixel
                            rAngleNow=unfiltered_angleq[unfiltered_index];#PMath.ThetaDegOfXY(xOff,yOff)
                            #  (reset to center so that rReachMultiplier can be used properly)
                            unfiltered_reached_pointq_rqX[unfiltered_index]=unfiltered_nonreached_pointq_rqX[unfiltered_index]
                            unfiltered_reached_pointq_rqY[unfiltered_index]=unfiltered_nonreached_pointq_rqY[unfiltered_index]
                            #if rReachMultiplier<=1.0, by distance of self point * multiplier
                            #else push by full distance of self point  plus  (multiplier-1.0) * average distance
                            if rReachMultiplier<=1.0) PMath.Travel2d(unfiltered_reached_pointq_rqX[unfiltered_index], unfiltered_reached_pointq_rqY[unfiltered_index], rAngleNow, rReachMultiplier*unfiltered_nonreached_distanceq[unfiltered_index] :
                            else PMath.Travel2d(unfiltered_reached_pointq_rqX[unfiltered_index], unfiltered_reached_pointq_rqY[unfiltered_index], rAngleNow, unfiltered_nonreached_distanceq[unfiltered_index]+(rReachMultiplier-1.0)*filtered_rAvgDist )
                            #now apply diffusion to pixel:
                            unfiltered_reached_pointq_rqX[unfiltered_index]+=DiffuseAllRadialSamples_X
                            unfiltered_reached_pointq_rqY[unfiltered_index]+=DiffuseAllRadialSamples_Y
                            #xOff=unfiltered_reached_pointq_rqX[unfiltered_index]-(double)x
                            #yOff=unfiltered_reached_pointq_rqY[unfiltered_index]-(double)y
                            #push to black mask pixel (corresponds to a usable background pixel)
                            #bool bFoundZeroBeforeEdge=PImage.PushToNearest(unfiltered_nonreached_pointq_rqX[unfiltered_index],unfiltered_nonreached_pointq_rqY[unfiltered_index],rAngleNow,mask0,mask_w,mask_h,mask_BytesPP,mask_Stride,mask_Channel,1,False)

                            #PushToNearest again since just did reach and diffusion:
                            bool bFoundAnyZero=PImage.PushToNearest(unfiltered_reached_pointq_rqX[unfiltered_index],unfiltered_reached_pointq_rqY[unfiltered_index],mask0,w,h,mask_BytesPP,mask_Stride,mask_Channel,1,False)
                            if bFoundAnyZero:
                                #--collect distance from center & keep track of min & max
                                double xOff=unfiltered_nonreached_pointq_rqX[unfiltered_index]-(double)x
                                double yOff=unfiltered_nonreached_pointq_rqY[unfiltered_index]-(double)y
                                rAngleNow=PMath.ThetaDegOfXY(xOff,yOff)
                                unfiltered_reached_distq[unfiltered_index]=PMath.ROfXY(xOff,yOff);#AFTER moving the point
                                if (unfiltered_reached_distq[unfiltered_index]<rMinDist) rMinDist=unfiltered_reached_distq[unfiltered_index]
                                if (unfiltered_reached_distq[unfiltered_index]>rMaxDist) rMaxDist=unfiltered_reached_distq[unfiltered_index]

                                #NOTE: "(int)" typecast for uiLoc is ok since bFoundAnyZero
                                unsigned int uiLoc=(int)unfiltered_nonreached_pointq_rqY[unfiltered_index]*dest_Stride+(int)unfiltered_nonreached_pointq_rqX[unfiltered_index]*dest_BytesPP
                                unfiltered_byqB[unfiltered_index]=dest0[uiLoc+chanB]
                                unfiltered_byqG[unfiltered_index]=dest0[uiLoc+chanG]
                                unfiltered_byqR[unfiltered_index]=dest0[uiLoc+chanR]
                                if (dest_BytesPP>3) unfiltered_byqA[unfiltered_index]=dest0[uiLoc+chanA]
                                else unfiltered_byqA[unfiltered_index]=255
                                #NOTE: weight is not needed yet, color is needed for weighted average below

                            else:
                                Console.Error.WriteLine("Heal error: no background pixel (self should never happen)")
                                break
                                #PImage.PushToNearest(unfiltered_reached_pointq_rqX[unfiltered_index],unfiltered_reached_pointq_rqY[unfiltered_index],mask0,mask_w,mask_h,mask_BytesPP,mask_Stride,mask_Channel,1,False)

                        }#end for filtered_index, reach and diffusion
                        #7. get spread (max-min)
                        double rSpread=0
                        if  (rMaxDist>=0) and (rMinDist<DBL_MAX) :
                            rSpread=rMaxDist-rMinDist

                        else:
                            Console.Error.WriteLine("Heal error: min/max not found, needs at least one background pixel (specified by black mask pixel) {unfiltered_Used:"+Convert.ToString(unfiltered_Used)+"; filtered_Used:"
                                                     +Convert.ToString(filtered_Used)+"}")

                        if (PReporting.getIsMegaDebug()) cerr<<"rMinDist:"<<rMinDist<<"..."<<flush
                        if (PReporting.getIsMegaDebug()) cerr<<"rMaxDist:"<<rMaxDist<<"..."<<flush
                        #if PReporting.getIsMegaDebug():                        #	Console.Error.WriteLine("Heal {unfiltered_Used:"+Convert.ToString(unfiltered_Used)+"; filtered_Used:"
                        #		+Convert.ToString(filtered_Used)+"}")
                        #
                        #8. foreach near pixel, color modified by ratio of current point dist between min to max to weighted average
                        double rTotalColorWeight=0.0
                        double heavypixel_B=0.0
                        double heavypixel_G=0.0
                        double heavypixel_R=0.0
                        double heavypixel_A=0.0
                        for (unsigned int filtered_index=0; filtered_index<filtered_Used; filtered_index++)
                            #add to dcolorCumulative value weighted by nearness to center
                            unsigned int unfiltered_index=filtered_indexq[filtered_index]
                            double rWeightNow=PMath.Nextness('''from'''rMaxDist,'''to'''rMinDist,
                                              unfiltered_reached_distq[unfiltered_index]);#unfiltered_nonreached_distanceq[filtered_indexq[unfiltered_index]])
                            #NOTE: diffused location does NOT reduce diffusion since distance is from the pixel which was the diffusion starting point not diffused source location
                            heavypixel_B+=rWeightNow*(double)unfiltered_byqB[unfiltered_index]
                            heavypixel_G+=rWeightNow*(double)unfiltered_byqG[unfiltered_index]
                            heavypixel_R+=rWeightNow*(double)unfiltered_byqR[unfiltered_index]
                            heavypixel_A+=rWeightNow*(double)unfiltered_byqA[unfiltered_index]
                            rTotalColorWeight+=rWeightNow
                            #multiplier = dist from max point / spread
                            #add weight to fTotalColorWeight

                        #9. get weighted average colorWA dividing heavypixel_ channel values by rTotalColorWeight
                        byte colorWA_B=(byte)(heavypixel_B/rTotalColorWeight+.5);#.5 for rounding
                        byte colorWA_G=(byte)(heavypixel_G/rTotalColorWeight+.5);#.5 for rounding
                        byte colorWA_R=(byte)(heavypixel_R/rTotalColorWeight+.5);#.5 for rounding
                        byte colorWA_A=(byte)(heavypixel_A/rTotalColorWeight+.5);#.5 for rounding
                        #10. overlay colorWA onto *lpDest using *lpMask as alpha
                        double rCookedAlpha=(float)*lpMask/255.0f
                        #alpha formula: (dest-src)*alpharatio+dest
                        #for each colorWA channel as src
                        lpDest[chanB]=PMath.ByRound((lpDest[chanB]-colorWA_B)*rCookedAlpha+lpDest[chanB])
                        if dest_BytesPP>1:
                            lpDest[chanG]=PMath.ByRound((lpDest[chanG]-colorWA_G)*rCookedAlpha+lpDest[chanG])
                            lpDest[chanR]=PMath.ByRound((lpDest[chanR]-colorWA_R)*rCookedAlpha+lpDest[chanR])
                            #NOTE: should always use "alpha on alpha" below so alpha gets healed if present
                            if dest_BytesPP>3) lpDest[chanA]=PMath.ByRound((lpDest[chanA]-colorWA_A)*rCookedAlpha+lpDest[chanA]:

                    }#end if non-black pixel (to heal)
                    lpMask+=mask_BytesPP
                    lpDest+=dest_BytesPP
                }#end for x
                lpMaskLine+=mask_Stride
                lpDestLine+=dest_Stride
            }#end for y

        else Console.Error.WriteLine("Error in Heal: null mask")
        #}#end if dest_BytesPP<4

    else Console.Error.WriteLine("Error in Heal: null dest")
    if unfiltered_angleq!=null) free(unfiltered_angleq:
    if unfiltered_nonreached_distanceq!=null) free(unfiltered_nonreached_distanceq:
    if unfiltered_reached_pointq_rqX!=null) free(unfiltered_reached_pointq_rqX:
    if unfiltered_reached_pointq_rqY!=null) free(unfiltered_reached_pointq_rqY:
    if unfiltered_nonreached_pointq_rqX!=null) free(unfiltered_nonreached_pointq_rqX:
    if unfiltered_nonreached_pointq_rqY!=null) free(unfiltered_nonreached_pointq_rqY:
    if unfiltered_reached_distq!=null) free(unfiltered_reached_distq:
    if filtered_indexq!=null) free(filtered_indexq:
    if unfiltered_byqB!=null) free(unfiltered_byqB:
    if unfiltered_byqG!=null) free(unfiltered_byqG:
    if unfiltered_byqR!=null) free(unfiltered_byqR:
    if unfiltered_byqA!=null) free(unfiltered_byqA:
}#end Heal_WithAveraging_Sequential

}#end namespace
#endif