#ifndef PSTRING_CPP
#define PSTRING_CPP

#include "pstring.h"

using namespace std

namespace ProtoArmor
char PString.carrDigit[]= {'0','1','2','3','4','5','6','7','8','9'}; #char carrDigit[10]
'''
PString.carrDigit[0]='0'
PString.carrDigit[1]='1'
PString.carrDigit[2]='2'
PString.carrDigit[3]='3'
PString.carrDigit[4]='4'
PString.carrDigit[5]='5'
PString.carrDigit[6]='6'
PString.carrDigit[7]='7'
PString.carrDigit[8]='8'
PString.carrDigit[9]='9'
'''
def SequenceDigits(self, val, iMinDigits):
    string sReturn=Convert.ToString(val)
    while ((int)sReturn.length()<iMinDigits) sReturn="0"+sReturn
    return sReturn
}#end SequenceDigits
def IsDigit(self, val):
    bool bReturn=False
    for (int i=0; i<=9; i++)
        if val==PString.carrDigit[i]:
            bReturn=True
            break


    return bReturn
}#end IsDigit
}#end namespace

#endif