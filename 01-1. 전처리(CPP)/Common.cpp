#include "Common.h"

// This code is from CodeProject(https://www.codeproject.com/Articles/22488/Distance-using-Longitiude-and-latitude-using-c)
double calculateDistance(double lat1, double long1, double lat2, double long2) {
    double PI = 4.0 * atan(1.0);

    //main code inside the class
    double dlat1 = lat1 * (PI / 180);

    double dlong1 = long1 * (PI / 180);
    double dlat2 = lat2 * (PI / 180);
    double dlong2 = long2 * (PI / 180);

    double dLong = dlong1 - dlong2;
    double dLat = dlat1 - dlat2;

    double aHarv = pow(sin(dLat / 2.0), 2.0) + cos(dlat1) * cos(dlat2) * pow(sin(dLong / 2), 2);
    double cHarv = 2 * atan2(sqrt(aHarv), sqrt(1.0 - aHarv));
    //earth's radius from wikipedia varies between 6,356.750 km — 6,378.135 km (˜3,949.901 — 3,963.189 miles)
    //The IUGG value for the equatorial radius of the Earth is 6378.137 km (3963.19 mile)
    const double earth = 6378.137 * 1000;   // in meters
    double distance = earth * cHarv;
    return distance;
}

int diffMonths(int year1, int month1, int year2, int month2)
{
    return (year1 - year2) * 12 + (month1 - month2);
}

vector<string> split(const char* str, char c)
{
    vector<string> result;

    do
    {
        const char* begin = str;

        while (*str != c && *str)
            str++;

        result.push_back(string(begin, str));
    } while (0 != *str++);

    return result;
}