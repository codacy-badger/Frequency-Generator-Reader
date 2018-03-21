/*
*	File Name: C_ScanA.c
*	Project: Currently Unnamed
*
*	Company: Research in Flows, Inc
*	Author: David Gurevich
*
*	Dependencies:
*		- cbw.h
*		- cbw32.lib
*		- cbw64.lib
*
*	Purpose:
*			This software reads the count and the rate generated by Main.py 'config.txt' to determine
*		the number of points to measure, and at what rate to measure them.
*			This software runs an analyzer on Board 1, and gets x many Analog input values.
*		It is kept in a Windows Buffer, and then one by one, exported into a file 'output.txt'
*/

#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <conio.h>
#include "cbw.h"

void scan_a_in(long count, long rate) {
	int BoardNum = 1;
	int ULStat = 0;
	int LowChan = 0;
	int HighChan = 1;
	int Gain = BIP2VOLTS;
	long Count = count;
	long Rate = rate;
	
	HANDLE MemHandle = 0;
	WORD *ADData = NULL;
	DWORD *ADData32 = NULL;

	unsigned Options;
	float	RevLevel = (float)CURRENTREVNUM;
	BOOL HighResAD = FALSE;
	int ADRes;

	FILE * fp;

	ULStat = cbDeclareRevision(&RevLevel);
	cbErrHandling(PRINTALL, DONTSTOP);
	cbGetConfig(BOARDINFO, BoardNum, 0, BIADRES, &ADRes);

	if (ADRes > 16)
		HighResAD = TRUE;

	if (HighResAD) {
		MemHandle = cbWinBufAlloc32(Count);
		ADData32 = (DWORD*)MemHandle;
		}
	else {
		MemHandle = cbWinBufAlloc(Count);
		ADData = (WORD*)MemHandle;
		}

	if (!MemHandle) {
		printf("\nOut Of Memory\n");
		exit(1);
		}

	Options = CONVERTDATA;
	ULStat = cbAInScan(BoardNum, LowChan, HighChan, Count, &Rate, Gain, MemHandle, Options);

	fp = fopen("output.txt", "w+");

	for (int i = 0; i < Count / 2; i++) {
		fprintf(fp, "%4u\n", ADData[i * 2]);
		// printf("%4u", ADData[i*2]);
		// printf("\n");
	}
	printf("Complete!\n");
	fclose(fp);

	cbWinBufFree(MemHandle);
}

int main() {
	FILE * fp;
	fp = fopen("config.txt", "r");

	char char_count[150];
	fgets(char_count, 150, fp);

	char rate_count[150];
	fgets(rate_count, 150, fp);

	fclose(fp);

	int count;
	int rate;
	sscanf(char_count, "%d", &count);
	sscanf(rate_count, "%d", &rate);

	scan_a_in(count, rate);
	return 0;
}