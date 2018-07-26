/*
  File Name: scan_dll.cpp
  Project: Currently Unnamed

  Company: Research in Flows, Inc
  Author: David A. Gurevich

  Frequency Generator Reader | Local software for generating, reading, and processing high-frequency signals
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
#include <chrono>

#include "cbw.h"

using namespace std::chrono;

extern "C" {
	__declspec(dllexport) void scan(int** input, long long* startTime, long long* endTime, int rate, double dur) {
		/*
			(int*, int, double) --> (None)

			Connects to USB2020 module, scans using settings as inputted by user, and
			saves information to inputted pointer.
		*/
		int BoardNum = 0;							// InstaCal board number. 0 by default
		int ULStat = 0;								// Initialize ULStat
		int LowChan = 0;							// Channel 0
		int HighChan = 1;							// Channel 1
		int Gain = BIP1VOLTS;						// Digital values conditioned for +/- 1V input
		int ChannelCount = (HighChan - LowChan) + 1;

		const int Count = (int)(ChannelCount * dur * rate);

		long Rate = rate;

		int* data = (int*)malloc((int)Count * sizeof(int)); // Allocate memory for incoming scan

		HANDLE MemHandle = 0;	// Using windows types because that's the ony thing this
		WORD *ADData = NULL;	// stupid driver supports.

		unsigned Options;
		float RevLevel = (float)CURRENTREVNUM;
		int ADRes;

		ULStat = cbDeclareRevision(&RevLevel);

		cbErrHandling(PRINTALL, STOPALL);
		cbGetConfig(BOARDINFO, BoardNum, 0, BIADRES, &ADRes);

		MemHandle = cbWinBufAlloc(Count);
		ADData = (WORD *)MemHandle;

		if (!MemHandle) {
			printf("\nOut of Memory\n");
			exit(1);
		}

		Options = CONVERTDATA + BURSTIO; // CONVERTDATA converts to digital values
										 // BURSTIO saves the data on onboard storage, then offloads it

		auto start_time = high_resolution_clock::now();
		ULStat = cbAInScan(BoardNum, LowChan, HighChan, Count, &Rate, Gain, MemHandle, Options);
		auto end_time = high_resolution_clock::now();

		if (ULStat != 0) {
			printf("There was a problem while scanning. Error Code: %d\n", ULStat);
		}
		else {
			for (int i = 0; i < Count; i++) {
				data[i] = ADData[i];	// Copy all the information from the array to the pointer.
			}

			*input = data;
			*startTime = duration_cast<nanoseconds>(start_time.time_since_epoch()).count();
			*endTime = duration_cast<nanoseconds>(end_time.time_since_epoch()).count();

			cbWinBufFree(MemHandle);
		}
	}

	__declspec(dllexport) void release(int* input) {
		if (input != NULL) {
			free(input);
			input = NULL;
		}
	}

	__declspec(dllexport) void stopBackground() {
		cbStopBackground(0, AIFUNCTION);
	}
}
