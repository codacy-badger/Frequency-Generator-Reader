/*
	ScanUtils.cpp
	David Gurevich

	Research In Flows, Inc

	(c) David Gurevich, 2018
*/

#include "stdafx.h"
#include "cbw.hh"
#include "Windows.h"

#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <algorithm>
#include <future>

using namespace std;

int arrSize = 0;
int CHUNK_SIZE = 1000000;

vector<future<int>> fut;

int writer(int id, vector<short> currentScanResults) {
	vector<short> channelLow;
	vector<short> channelHigh;

	vector<vector<short>> channelLowChunks;
	vector<vector<short>> channelHighChunks;

	for (size_t i = 0; i < currentScanResults.size() - 1; i += 2) {
		channelLow.push_back((short)currentScanResults.at(i));
		channelHigh.push_back((short)currentScanResults.at(i + 1));
	}

	vector<short>::iterator from = channelLow.begin();
	vector<short> subList;

	do {
		if (channelLow.end() - from > CHUNK_SIZE) {
			subList.assign(from, from + CHUNK_SIZE);
			from += CHUNK_SIZE;
			channelLowChunks.push_back(subList);
		}
		else {
			subList.assign(from, channelLow.end());
			subList.resize(channelLow.size() - (channelLowChunks.size() * CHUNK_SIZE));
			channelLowChunks.push_back(subList);

			channelLow.clear();
			channelLow.shrink_to_fit();

			subList.clear();
			subList.shrink_to_fit();
		}
	} while (!channelLow.empty());

	from = channelHigh.begin();

	do {
		if (channelHigh.end() - from > CHUNK_SIZE) {
			subList.assign(from, from + CHUNK_SIZE);
			from += CHUNK_SIZE;
			channelHighChunks.push_back(subList);
		}
		else {
			subList.assign(from, channelHigh.end());
			subList.resize(channelHigh.size() - (channelHighChunks.size() * CHUNK_SIZE));
			channelHighChunks.push_back(subList);

			channelHigh.clear();
			channelHigh.shrink_to_fit();

			subList.clear();
			subList.shrink_to_fit();
		}
	} while (!channelHigh.empty());

	for (size_t fileNumber = 0; fileNumber < channelLowChunks.size(); fileNumber++) {
		string fileName = string("Output/DAQ_Output_") + to_string(id + 1) + string("_") + to_string(fileNumber + 1) + string(".csv");

		ofstream currentFile;
		currentFile.open(fileName);

		for (size_t row = 0; row < channelLowChunks.at(fileNumber).size(); row++) {
			currentFile << (int)channelLowChunks.at(fileNumber).at(row) << ", " << (int)channelHighChunks.at(fileNumber).at(row) << "\n";
		}

		currentFile.close();
	}

	currentScanResults.clear();
	currentScanResults.shrink_to_fit();

	channelLowChunks.clear();
	channelLowChunks.shrink_to_fit();

	channelHighChunks.clear();
	channelHighChunks.shrink_to_fit();

	return 0;
}

void scanner(int id, int scanRate, double scanDuration) {
	int BoardNum = 0;
	int ULStat = 0;
	int LowChan = 0;
	int HighChan = 1;
	int Gain = BIP1VOLTS;
	int ChannelCount = (HighChan - LowChan) + 1;

	long Rate = (long)scanRate;
	const int Count = (int)(ChannelCount * scanDuration * Rate);

	arrSize = Count;

	HANDLE MemHandle = 0;
	WORD *ADData = NULL;

	unsigned Options;
	float RevLevel = (float)CURRENTREVNUM;
	int ADRes;

	ULStat = cbDeclareRevision(&RevLevel);
	cbErrHandling(DONTPRINT, DONTSTOP);
	cbGetConfig(BOARDINFO, BoardNum, 0, BIADRES, &ADRes);

	MemHandle = cbWinBufAlloc(Count);
	ADData = (WORD *)MemHandle;

	if (!MemHandle) {
		cout << "Out of Memory" << endl;
		exit(1);
	}

	Options = CONVERTDATA + BURSTIO;
	ULStat = cbAInScan(BoardNum, LowChan, HighChan, Count, &Rate, Gain, MemHandle, Options);

	if (ULStat != 0)
		cout << "There was a problem while scanning. Error Code: " << ULStat << endl;
	else {
		vector<short> currentScanResults(ADData, ADData + arrSize);

		fut.push_back(async(launch::async, writer, id, currentScanResults));
		cbWinBufFree(MemHandle);
	}
}

void runDAQScan(int numOfThreads, int scanRate, double scanDuration) {
	fut.clear();
	fut.shrink_to_fit();

	for (size_t id = 0; id < numOfThreads; id++) {
		scanner(id, scanRate, scanDuration);
	}

	cout << "Scans Initialized" << endl;

	for (size_t f = 0; f < numOfThreads; f++) {
		fut.at(f).wait();
	}

	cout << "Writing Complete" << endl;
}

extern "C" __declspec(dllexport) void runDAQScanDLL(int numOfThreads, int scanRate, double scanDuration) {
	runDAQScan(numOfThreads, scanRate, scanDuration);
}