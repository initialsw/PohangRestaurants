#pragma once
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>
#include <cmath>

using namespace std;
double calculateDistance(double lat1, double long1, double lat2, double long2);
int diffMonths(int year1, int month1, int year2, int month2);
vector<string> split(const char* str, char c = ',');