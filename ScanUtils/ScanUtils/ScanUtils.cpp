/*
	ScanUtils.cpp
	David Gurevich
	October 11th, 2018

	Research In Flows, Inc
*/

#include "stdafx.h"
#include "cbw.hh"
#include "Windows.h"

#include <thread>
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <algorithm>

std::vector<bool> scanCompletion(0);
std::vector<bool> writeCompletion(0);

std::vector<short*> scanResults(0);

int arrSize = 0;
constexpr int CHUNK_SIZE = 1000000;


void scanner(int id, int scanRate, double scanDuration) {
	int BoardNum = 0;
	int ULStat = 0;
	int LowChan = 0;
	int HighChan = 1;
	int Gain = BIP1VOLTS;
	long Rate = (long)scanRate;
	int ChannelCount = (HighChan - LowChan) + 1;

	const int Count = (int)(ChannelCount * scanDuration * scanRate);
	arrSize = Count;

	short *data = (short*)malloc(sizeof(short) * Count);

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
		std::cout << "Out of Memory" << std::endl;
		exit(1);
	}

	Options = CONVERTDATA + BURSTIO;
	ULStat = cbAInScan(BoardNum, LowChan, HighChan, Count, &Rate, Gain, MemHandle, Options);

	if (ULStat != 0) {
		std::cout << "There was a problem while scanning. Error Code: " << ULStat << std::endl;
	}
	else {
		for (int i = 0; i < Count; i++) {
			data[i] = ADData[i];
		}
		cbWinBufFree(MemHandle);
		scanResults[id] = data;
		scanCompletion[id] = 1;
	}
}

void writer(int id) {
	while (1) {
		std::cout << "";
		if (scanCompletion[id] == 1) {
			std::vector<short> currentScanResults(scanResults[id], scanResults[id] + arrSize);
			std::fill_n(scanResults[id], currentScanResults.size(), 0);

			std::vector<short> channelLow;
			std::vector<short> channelHigh;

			std::vector<std::vector<short>> channelLowChunks;
			std::vector<std::vector<short>> channelHighChunks;

			if (!currentScanResults.empty()) {
				for (size_t i = 0; i < (currentScanResults.size() - 1); i += 2) {
					channelLow.push_back(currentScanResults[i]);
					channelHigh.push_back(currentScanResults[i + 1]);
				}
			}

			currentScanResults.clear();
			currentScanResults.shrink_to_fit();

			std::vector<short>::iterator from = channelLow.begin();
			std::vector<short> subList;

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

			////////////////////////////////////////////////////

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
				std::string filename = std::string("Output/DAQ_Output_") + std::to_string(id+1) + std::string("_") +std::to_string(fileNumber+1) + std::string(".csv");

				std::ofstream currentFile;
				currentFile.open(filename);

				for (size_t row = 0; row < channelLowChunks[fileNumber].size(); row++) {
					currentFile << (int)channelLowChunks[fileNumber][row] << ", " << (int)channelHighChunks[fileNumber][row] << "\n";
				}

				currentFile.close();
			}
			writeCompletion[id] = true;

			channelLow.clear();
			channelLow.shrink_to_fit();

			channelHigh.clear();
			channelHigh.shrink_to_fit();

			break;
		}
	}
}

void runDAQScan(int numOfThreads, int scanRate, double scanDuration) {
	std::vector<std::thread> writeThreadManager(0);
	bool scanInProgress = true;

	scanResults.resize(numOfThreads);
	scanCompletion.resize(numOfThreads);
	writeCompletion.resize(numOfThreads);

	std::cout << "Initializing write threads" << std::endl;
	for (size_t i = 0; i < numOfThreads; i++) {
		writeThreadManager.push_back(std::thread(&writer, i));
	}
	std::cout << "Write threads started. Starting scans." << std::endl;
	for (size_t j = 0; j < numOfThreads; j++) {
		scanner(j, scanRate, scanDuration);
	}
	std::cout << "Scans complete." << std::endl;
	while (scanInProgress) {
		if (std::all_of(writeCompletion.begin(), writeCompletion.end(), [](bool x) { return x == true; })) {
			for (size_t n = 0; n < numOfThreads; n++) {
				writeThreadManager[n].join();
			}
			scanInProgress = false;
		}
	}
	std::cout << "Write complete." << std::endl;
}

extern "C" __declspec(dllexport) void runDAQScanDLL(int numOfThreads, int scanRate, double scanDuration) {
	runDAQScan(numOfThreads, scanRate, scanDuration);
}