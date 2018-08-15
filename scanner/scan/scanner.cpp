#include <Windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <conio.h>
#include <chrono>
#include <fstream>
#include <iostream>

#include "cbw.h"

using namespace std;
using namespace std::chrono;

extern "C" {
	__declspec(dllexport) void scan(int** input, long long* startTime, long long* endTime, int rate, double dur) {
		int BoardNum = 0;
		int ULStat = 0;
		int LowChan = 0;
		int HighChan = 1;
		int Gain = BIP1VOLTS;
		int ChannelCount = (HighChan - LowChan) + 1;

		const int Count = (int)(ChannelCount * dur * rate);

		long Rate = rate;
		
		int* data = (int*)malloc((int)Count * sizeof(int));

		HANDLE MemHandle = 0;
		WORD *ADData = NULL;

		unsigned Options;
		float RevLevel = (float)CURRENTREVNUM;
		int ADRes;

		ULStat = cbDeclareRevision(&RevLevel);

		cbErrHandling(PRINTALL, DONTSTOP);
		cbGetConfig(BOARDINFO, BoardNum, 0, BIADRES, &ADRes);

		MemHandle = cbWinBufAlloc(Count);
		ADData = (WORD *)MemHandle;

		if (!MemHandle) {
			printf("\nOut of Memory\n");
			exit(1);
		}

		Options = CONVERTDATA + BURSTIO;

		auto start_time = high_resolution_clock::now();
		ULStat = cbAInScan(BoardNum, LowChan, HighChan, Count, &Rate, Gain, MemHandle, Options);
		auto end_time = high_resolution_clock::now();

		if (ULStat != 0) {
			printf("There was a problem while scanning. Error Code: %d\n", ULStat);

		}
		else {
			for (int i = 0; i < Count; i++) {
				data[i] = ADData[i];
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