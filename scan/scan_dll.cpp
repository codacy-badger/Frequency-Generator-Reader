/*
  File Name: scan.c
  Project: Currently Unnamed

  Company: Research in Flows, Inc
  Author: David Gurevich

    Frequency-Generator Reader | Local software for generating and processing high-frequency signals
    Copyright (C) 2018  David A. Gurevich

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

  Dependencies:
    - cbw.h
    - cbw32.lib
    - cbw64.lib

*/

#include <Windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <conio.h>
#include "cbw.h"

extern "C" {

  __declspec(dllexport) void scan(int** input, int rate, int dur) {
    int BoardNum = 0;
    int ULStat = 0;
    int LowChan = 0;
    int HighChan = 1;
    int Gain = 4;
    int ChannelCount = (HighChan - LowChan) + 1;

    const long Count = ChannelCount * dur * rate;
    long Rate = rate;

    int* data = (int*)malloc((int)Count * sizeof(int));


    HANDLE MemHandle = 0;
    WORD *ADData = NULL;
    DWORD *ADData32 = NULL;

    unsigned Options;
    float RevLevel = (float)CURRENTREVNUM;
    BOOL HighResAD = FALSE;
    int ADRes;

    ULStat = cbDeclareRevision(&RevLevel);

    cbErrHandling(PRINTALL, STOPALL);
    cbGetConfig(BOARDINFO, BoardNum, 0 , BIADRES, &ADRes);

    if (ADRes > 16) {
      HighResAD = TRUE;
    }

    if (HighResAD) {
      MemHandle = cbWinBufAlloc32(Count);
      ADData32 = (DWORD *)MemHandle;
    } else {
      MemHandle = cbWinBufAlloc(Count);
      ADData = (WORD *)MemHandle;
    }

    if (!MemHandle) {
      printf("\nOut of Memory\n");
      exit(1);
    }

    Options = CONVERTDATA;

    ULStat = cbAInScan(BoardNum, LowChan, HighChan, Count, &Rate, Gain, MemHandle, Options);

    for (int i = 0; i < Count; i++) {
      data[i] = ADData[i];
    }

    *input = data;
    cbWinBufFree(MemHandle);
  }

  __declspec(dllexport) void release(int* input) {
    free(input);
  }
}
