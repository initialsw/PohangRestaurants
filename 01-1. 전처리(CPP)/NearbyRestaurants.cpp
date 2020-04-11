#include "NearbyRestaurants.h"

void getNearbyRestaurantsYearly(bool isSameMenu)
{
    ::cout << "Execute getNearByRestaurants()" << endl;
    string filePath = "D:\\Research\\Data\\99.Location_Restaurants.csv";
    string outPath = "";
    if (isSameMenu)
        outPath = "D:\\Research\\Data\\99.NearbyRestaurantsSameMenu.csv";
    else
        outPath = "D:\\Research\\Data\\99.NearbyRestaurants.csv";

    // Step1. 일반음식점의 좌표 데이터 읽기    
    ifstream in(filePath.data());
    const int BUFFER_SIZE = 1000;
    char buf[BUFFER_SIZE];
    if (!in.is_open()) {
        ::cout << "Cannot open the file!!!" << endl;
        return;
    }

    string delimiter = ",";
    int cnt = 0;

    // skip header
    in.getline(buf, BUFFER_SIZE);

    const int NUM_REST = 16922;
    const int NUM_COLUMNS = 8;
    const int nLIMIT = 10;
    double* location = new double[NUM_REST * NUM_COLUMNS];

    ::cout << "Step1. Read " << filePath << endl;

    while (in) {
        in.getline(buf, BUFFER_SIZE);
        if (strlen(buf) < 10) break;
        vector<string> result = split(&buf[0]);
        for (int i = 0; i < NUM_COLUMNS; i++) {
            // Columns = [ Index,No,OpenYear,OpenMonth,CloseYear,CloseMonth,Menu,Latitude,Longitude ]
            *(location + cnt * NUM_COLUMNS + i) = stod(result[i]);
        }
        //::cout << endl;
        cnt++;
        /* For Test...
        if (nLIMIT <= cnt)
            break;
        //*/
    }
    in.close();

    // 2000년부터 2019년까지 매년 주위 식당 수가 어떻게 바뀌는지 식당별로 계산
    ::cout << "Step2. Count nearby restaurants..." << endl;
    const int NUM_YEARS = 20;
    const int FIRST_YEAR = 2000;
    const double RADIUS = 500;  // 반경 500m 내
    int* result = new int[NUM_REST * (NUM_YEARS + 1)];

    for (int i = 0; i < NUM_REST; i++) {
        // Columns = [ Index,No,OpenYear,OpenMonth,CloseYear,CloseMonth,Menu,Latitude,Longitude ]
        int no = int(location[i * NUM_COLUMNS + 0]);
        int openYear = int(location[i * NUM_COLUMNS + 1]);
        int openMonth = int(location[i * NUM_COLUMNS + 2]);
        int closeYear = int(location[i * NUM_COLUMNS + 3]);
        int closeMonth = int(location[i * NUM_COLUMNS + 4]);
        int menu = int(location[i * NUM_COLUMNS + 5]);
        double latitude = location[i * NUM_COLUMNS + 6];
        double longitude = location[i * NUM_COLUMNS + 7];

        /*
        ::cout << "Restaurants No." << to_string(no) << " Menu: " << to_string(menu)
            << " Open " << to_string(openYear) << "-" << to_string(openMonth)
            << " Close " << to_string(closeYear) << "-" << to_string(closeMonth) << endl;
        //*/
        int cntNearby[NUM_YEARS];
        // 위치정보가 없는 식당인 경우 카운트를 -1로 지정(이후에 분석시 제외)
        for (int y = 0; y < NUM_YEARS; y++)
            cntNearby[y] = -1;

        // 1. 식당 번호
        *(result + i * (NUM_YEARS + 1) + 0) = no;

        // 위치정보가 있는 경우에만 실행
        if (latitude != 0.0 && longitude != 0.0) {

            // 연도별 주위 식당 수를 0으로 초기화
            for (int y = 0; y < NUM_YEARS; y++) 
                cntNearby[y] = 0;

            // 다른 식당과의 거리를 계산한 후 근처 식당 수 카운트
            for (int j = 0; j < NUM_REST; j++) {
                if (i == j) continue;
                int tmp_no = int(location[j * NUM_COLUMNS + 0]);
                int tmp_openYear = int(location[j * NUM_COLUMNS + 1]);
                int tmp_openMonth = int(location[j * NUM_COLUMNS + 2]);
                int tmp_closeYear = int(location[j * NUM_COLUMNS + 3]);
                int tmp_closeMonth = int(location[j * NUM_COLUMNS + 4]);
                int tmp_menu = int(location[j * NUM_COLUMNS + 5]);
                double tmp_latitude = location[j * NUM_COLUMNS + 6];
                double tmp_longitude = location[j * NUM_COLUMNS + 7];
                
                // 같은 메뉴만 고려하는 경우
                // 메뉴 다르면 넘어감
                if (isSameMenu && (menu == tmp_menu))
                    continue;

                double distance = calculateDistance(latitude, longitude, tmp_latitude, tmp_longitude);

                // 거리가 500m 이상이면 넘어감
                if (distance > RADIUS) continue;

                // 2. 반경 500m 내 위치한 식당이면 영업기간이 겹치는 연도의 카운트를 증가
                for (int y = 0; y < NUM_YEARS; y++) {
                    int year = y + FIRST_YEAR;
                    if ((year >= tmp_openYear && year <= tmp_closeYear))
                        //&& (year >= openYear && year <= closeYear))                        
                        cntNearby[y]++;

                }
            }
        }

        for (int y = 0; y < NUM_YEARS; y++) {
            //cout << " " << to_string(cntNearby[y]);
            *(result + i * (NUM_YEARS + 1) + (y + 1)) = cntNearby[y];
        }
        //cout << endl;
        if (i % 1000 == 0)
            cout << to_string(i) << "/" << to_string(NUM_REST) << endl;
        /* For Test...
        if (i >= nLIMIT)
            break;
        //*/
    }

    ::cout << "Step3. Save the result..." << endl;
    ofstream outFile = ofstream(outPath.data());

    // 헤더쓰기
    outFile << "No,OpenYear,OpenMonth,CloseYear,CloseMonth,Menu,"
        << "Latitude,Longitude";
    for (int y = 0; y < NUM_YEARS; y++)
        outFile << "," << to_string(y + FIRST_YEAR);
    outFile << endl;

    for (int i = 0; i < NUM_REST; i++) {
        /*
        ::cout << "Restaurants No." << *(location + i * NUM_COLUMNS + 1)
            << " Menu: " << to_string(*(location + i * NUM_COLUMNS + 2))
            << " Open " << to_string(*(location + i * NUM_COLUMNS + 3))            
            << " Close " << to_string(*(location + i * NUM_COLUMNS + 5))            
        //*/

        /*
        ㅁ 결과에 포함할 항목 (대략 한 블록이 500m 정도)
           - 기준일 : 식당이 개업(인허가)한 연도
          1. 식당 번호
          2. 식당의 개업연도
          3. 식당의 개업월
          4. 식당의 폐업연도
          5. 식당의 폐업월
          6. 식당 메뉴          
          7. 경도
          8. 위도
          9. 영업기간 중 반경 500m 내 식당 수 (2000년~2019년)
        */
        
        outFile << *(location + i * NUM_COLUMNS + 0) << ","
            << *(location + i * NUM_COLUMNS + 1) << ","
            << *(location + i * NUM_COLUMNS + 2) << ","
            << *(location + i * NUM_COLUMNS + 3) << ","
            << *(location + i * NUM_COLUMNS + 4) << ","
            << *(location + i * NUM_COLUMNS + 5) << ","
            << *(location + i * NUM_COLUMNS + 6) << ","
            << *(location + i * NUM_COLUMNS + 7);

        for (int y = 0; y < NUM_YEARS; y++)
            outFile << "," << *(result + i * (NUM_YEARS + 1) + (y + 1));
        outFile << endl;
    }
    outFile.close();

    delete[] location;
    delete[] result;
    cout << "Finished getNearbyRestaurants()!" << endl;
}

void getNearbyNewRestaurantsYearly(bool isSameMenu)
{
    ::cout << "Execute getNearbyNewRestaurants()" << endl;
    string filePath = "D:\\Research\\Data\\99.Location_Restaurants.csv";
    string outPath = "";
    if (isSameMenu)
        outPath = "D:\\Research\\Data\\99.NearbyNewRestaurantsSameMenu.csv";
    else
        outPath = "D:\\Research\\Data\\99.NearbyNewRestaurants.csv";

    // Step1. 일반음식점의 좌표 데이터 읽기    
    ifstream in(filePath.data());
    const int BUFFER_SIZE = 1000;
    char buf[BUFFER_SIZE];
    if (!in.is_open()) {
        ::cout << "Cannot open the file!!!" << endl;
        return;
    }

    string delimiter = ",";
    int cnt = 0;

    // skip header
    in.getline(buf, BUFFER_SIZE);

    const int NUM_REST = 16922;
    const int NUM_COLUMNS = 8;
    const int nLIMIT = 10;
    double* location = new double[NUM_REST * NUM_COLUMNS];

    ::cout << "Step1. Read " << filePath << endl;

    while (in) {
        in.getline(buf, BUFFER_SIZE);
        if (strlen(buf) < 10) break;
        vector<string> result = split(&buf[0]);
        for (int i = 0; i < NUM_COLUMNS; i++) {
            // Columns = [ Index,No,OpenYear,OpenMonth,CloseYear,CloseMonth,Menu,Latitude,Longitude ]
            *(location + cnt * NUM_COLUMNS + i) = stod(result[i]);
        }
        //::cout << endl;
        cnt++;
        /* For Test...
        if (nLIMIT <= cnt)
            break;
        //*/
    }
    in.close();

    // 2000년부터 2019년까지 매년 주위 식당 수가 어떻게 바뀌는지 식당별로 계산
    ::cout << "Step2. Count nearby restaurants..." << endl;
    const int NUM_YEARS = 20;
    const int FIRST_YEAR = 2000;
    const double RADIUS = 500;  // 반경 500m 내
    int* result = new int[NUM_REST * (NUM_YEARS + 1)];

    for (int i = 0; i < NUM_REST; i++) {
        // Columns = [ Index,No,OpenYear,OpenMonth,CloseYear,CloseMonth,Menu,Latitude,Longitude ]
        int no = int(location[i * NUM_COLUMNS + 0]);
        int openYear = int(location[i * NUM_COLUMNS + 1]);
        int openMonth = int(location[i * NUM_COLUMNS + 2]);
        int closeYear = int(location[i * NUM_COLUMNS + 3]);
        int closeMonth = int(location[i * NUM_COLUMNS + 4]);
        int menu = int(location[i * NUM_COLUMNS + 5]);
        double latitude = location[i * NUM_COLUMNS + 6];
        double longitude = location[i * NUM_COLUMNS + 7];

        /*
        ::cout << "Restaurants No." << to_string(no) << " Menu: " << to_string(menu)
            << " Open " << to_string(openYear) << "-" << to_string(openMonth)
            << " Close " << to_string(closeYear) << "-" << to_string(closeMonth) << endl;
        //*/
        int cntNearby[NUM_YEARS];
        // 위치정보가 없는 식당인 경우 카운트를 -1로 지정(이후에 분석시 제외)
        for (int y = 0; y < NUM_YEARS; y++)
            cntNearby[y] = -1;

        // 1. 식당 번호
        *(result + i * (NUM_YEARS + 1) + 0) = no;

        // 위치정보가 있는 경우에만 실행
        if (latitude != 0.0 && longitude != 0.0) {

            // 연도별 주위 새로 개업한 식당 수를 0으로 초기화
            for (int y = 0; y < NUM_YEARS; y++)
                cntNearby[y] = 0;

            // 다른 식당과의 거리를 계산한 후 근처 식당 수 카운트
            for (int j = 0; j < NUM_REST; j++) {
                if (i == j) continue;
                int tmp_no = int(location[j * NUM_COLUMNS + 0]);
                int tmp_openYear = int(location[j * NUM_COLUMNS + 1]);
                int tmp_openMonth = int(location[j * NUM_COLUMNS + 2]);
                int tmp_closeYear = int(location[j * NUM_COLUMNS + 3]);
                int tmp_closeMonth = int(location[j * NUM_COLUMNS + 4]);
                int tmp_menu = int(location[j * NUM_COLUMNS + 5]);
                double tmp_latitude = location[j * NUM_COLUMNS + 6];
                double tmp_longitude = location[j * NUM_COLUMNS + 7];

                // 같은 메뉴만 고려하는 경우
                // 메뉴 다르면 넘어감
                if (isSameMenu && (menu == tmp_menu))
                    continue;

                double distance = calculateDistance(latitude, longitude, tmp_latitude, tmp_longitude);

                // 거리가 500m 이상이면 넘어감
                if (distance > RADIUS) continue;

                // 2. 반경 500m 내 위치한 식당일 때 개업연도별로 카운트
                for (int y = 0; y < NUM_YEARS; y++) {
                    int year = y + FIRST_YEAR;
                    if ( tmp_openYear == year )
                        cntNearby[y]++;
                }
            }
        }

        for (int y = 0; y < NUM_YEARS; y++) {
            //cout << " " << to_string(cntNearby[y]);
            *(result + i * (NUM_YEARS + 1) + (y + 1)) = cntNearby[y];
        }
        //cout << endl;
        if (i % 1000 == 0)
            cout << to_string(i) << "/" << to_string(NUM_REST) << endl;
        /* For Test...
        if (i >= nLIMIT)
            break;
        //*/
    }

    ::cout << "Step3. Save the result..." << endl;
    ofstream outFile = ofstream(outPath.data());

    // 헤더쓰기
    outFile << "No,OpenYear,OpenMonth,CloseYear,CloseMonth,Menu,"
        << "Latitude,Longitude";
    for (int y = 0; y < NUM_YEARS; y++)
        outFile << "," << to_string(y + FIRST_YEAR);
    outFile << endl;

    for (int i = 0; i < NUM_REST; i++) {
        /*
        ::cout << "Restaurants No." << *(location + i * NUM_COLUMNS + 1)
            << " Menu: " << to_string(*(location + i * NUM_COLUMNS + 2))
            << " Open " << to_string(*(location + i * NUM_COLUMNS + 3))
            << " Close " << to_string(*(location + i * NUM_COLUMNS + 5))
        //*/

        /*
        ㅁ 결과에 포함할 항목 (대략 한 블록이 500m 정도)
           - 기준일 : 식당이 개업(인허가)한 연도
          1. 식당 번호
          2. 식당의 개업연도
          3. 식당의 개업월
          4. 식당의 폐업연도
          5. 식당의 폐업월
          6. 식당 메뉴
          7. 경도
          8. 위도
          9. 영업기간 중 반경 500m 내 개업한 식당 수 (2000년~2019년)
        */

        outFile << *(location + i * NUM_COLUMNS + 0) << ","
            << *(location + i * NUM_COLUMNS + 1) << ","
            << *(location + i * NUM_COLUMNS + 2) << ","
            << *(location + i * NUM_COLUMNS + 3) << ","
            << *(location + i * NUM_COLUMNS + 4) << ","
            << *(location + i * NUM_COLUMNS + 5) << ","
            << *(location + i * NUM_COLUMNS + 6) << ","
            << *(location + i * NUM_COLUMNS + 7);

        for (int y = 0; y < NUM_YEARS; y++)
            outFile << "," << *(result + i * (NUM_YEARS + 1) + (y + 1));
        outFile << endl;
    }
    outFile.close();

    delete[] location;
    delete[] result;
    cout << "Finished getNearbyNewRestaurants()!" << endl;
}

void getNearbyClosedRestaurantsYearly(bool isSameMenu)
{
    ::cout << "Execute getNearbyClosedRestaurants()" << endl;
    string filePath = "D:\\Research\\Data\\99.Location_Restaurants.csv";
    string outPath = "";
    if (isSameMenu)
        outPath = "D:\\Research\\Data\\99.NearbyClosedRestaurantsSameMenu.csv";
    else
        outPath = "D:\\Research\\Data\\99.NearbyClosedRestaurants.csv";

    // Step1. 일반음식점의 좌표 데이터 읽기    
    ifstream in(filePath.data());
    const int BUFFER_SIZE = 1000;
    char buf[BUFFER_SIZE];
    if (!in.is_open()) {
        ::cout << "Cannot open the file!!!" << endl;
        return;
    }

    string delimiter = ",";
    int cnt = 0;

    // skip header
    in.getline(buf, BUFFER_SIZE);

    const int NUM_REST = 16922;
    const int NUM_COLUMNS = 8;
    const int nLIMIT = 10;
    double* location = new double[NUM_REST * NUM_COLUMNS];

    ::cout << "Step1. Read " << filePath << endl;

    while (in) {
        in.getline(buf, BUFFER_SIZE);
        if (strlen(buf) < 10) break;
        vector<string> result = split(&buf[0]);
        for (int i = 0; i < NUM_COLUMNS; i++) {
            // Columns = [ Index,No,OpenYear,OpenMonth,CloseYear,CloseMonth,Menu,Latitude,Longitude ]
            *(location + cnt * NUM_COLUMNS + i) = stod(result[i]);
        }
        //::cout << endl;
        cnt++;
        /* For Test...
        if (nLIMIT <= cnt)
            break;
        //*/
    }
    in.close();

    // 2000년부터 2019년까지 매년 주위 식당 수가 어떻게 바뀌는지 식당별로 계산
    ::cout << "Step2. Count nearby restaurants..." << endl;
    const int NUM_YEARS = 20;
    const int FIRST_YEAR = 2000;
    const double RADIUS = 500;  // 반경 500m 내
    int* result = new int[NUM_REST * (NUM_YEARS + 1)];

    for (int i = 0; i < NUM_REST; i++) {
        // Columns = [ Index,No,OpenYear,OpenMonth,CloseYear,CloseMonth,Menu,Latitude,Longitude ]
        int no = int(location[i * NUM_COLUMNS + 0]);
        int openYear = int(location[i * NUM_COLUMNS + 1]);
        int openMonth = int(location[i * NUM_COLUMNS + 2]);
        int closeYear = int(location[i * NUM_COLUMNS + 3]);
        int closeMonth = int(location[i * NUM_COLUMNS + 4]);
        int menu = int(location[i * NUM_COLUMNS + 5]);
        double latitude = location[i * NUM_COLUMNS + 6];
        double longitude = location[i * NUM_COLUMNS + 7];

        /*
        ::cout << "Restaurants No." << to_string(no) << " Menu: " << to_string(menu)
            << " Open " << to_string(openYear) << "-" << to_string(openMonth)
            << " Close " << to_string(closeYear) << "-" << to_string(closeMonth) << endl;
        //*/
        int cntNearby[NUM_YEARS];
        // 위치정보가 없는 식당인 경우 카운트를 -1로 지정(이후에 분석시 제외)
        for (int y = 0; y < NUM_YEARS; y++)
            cntNearby[y] = -1;

        // 1. 식당 번호
        *(result + i * (NUM_YEARS + 1) + 0) = no;

        // 위치정보가 있는 경우에만 실행
        if (latitude != 0.0 && longitude != 0.0) {

            // 연도별 주위 새로 개업한 식당 수를 0으로 초기화
            for (int y = 0; y < NUM_YEARS; y++)
                cntNearby[y] = 0;

            // 다른 식당과의 거리를 계산한 후 근처 식당 수 카운트
            for (int j = 0; j < NUM_REST; j++) {
                if (i == j) continue;
                int tmp_no = int(location[j * NUM_COLUMNS + 0]);
                int tmp_openYear = int(location[j * NUM_COLUMNS + 1]);
                int tmp_openMonth = int(location[j * NUM_COLUMNS + 2]);
                int tmp_closeYear = int(location[j * NUM_COLUMNS + 3]);
                int tmp_closeMonth = int(location[j * NUM_COLUMNS + 4]);
                int tmp_menu = int(location[j * NUM_COLUMNS + 5]);
                double tmp_latitude = location[j * NUM_COLUMNS + 6];
                double tmp_longitude = location[j * NUM_COLUMNS + 7];

                // 같은 메뉴만 고려하는 경우
                // 메뉴 다르면 넘어감
                if (isSameMenu && (menu == tmp_menu))
                    continue;

                double distance = calculateDistance(latitude, longitude, tmp_latitude, tmp_longitude);

                // 거리가 500m 이상이면 넘어감
                if (distance > RADIUS) continue;

                // 2. 반경 500m 내 위치한 식당일 때 폐업연도별로 카운트
                for (int y = 0; y < NUM_YEARS; y++) {
                    int year = y + FIRST_YEAR;
                    if (tmp_closeYear == year)
                        cntNearby[y]++;
                }
            }
        }

        for (int y = 0; y < NUM_YEARS; y++) {
            //cout << " " << to_string(cntNearby[y]);
            *(result + i * (NUM_YEARS + 1) + (y + 1)) = cntNearby[y];
        }
        //cout << endl;
        if (i % 1000 == 0)
            cout << to_string(i) << "/" << to_string(NUM_REST) << endl;
        /* For Test...
        if (i >= nLIMIT)
            break;
        //*/
    }

    ::cout << "Step3. Save the result..." << endl;
    ofstream outFile = ofstream(outPath.data());

    // 헤더쓰기
    outFile << "No,OpenYear,OpenMonth,CloseYear,CloseMonth,Menu,"
        << "Latitude,Longitude";
    for (int y = 0; y < NUM_YEARS; y++)
        outFile << "," << to_string(y + FIRST_YEAR);
    outFile << endl;

    for (int i = 0; i < NUM_REST; i++) {
        /*
        ::cout << "Restaurants No." << *(location + i * NUM_COLUMNS + 1)
            << " Menu: " << to_string(*(location + i * NUM_COLUMNS + 2))
            << " Open " << to_string(*(location + i * NUM_COLUMNS + 3))
            << " Close " << to_string(*(location + i * NUM_COLUMNS + 5))
        //*/

        /*
        ㅁ 결과에 포함할 항목 (대략 한 블록이 500m 정도)
           - 기준일 : 식당이 개업(인허가)한 연도
          1. 식당 번호
          2. 식당의 개업연도
          3. 식당의 개업월
          4. 식당의 폐업연도
          5. 식당의 폐업월
          6. 식당 메뉴
          7. 경도
          8. 위도
          9. 영업기간 중 반경 500m 내 폐업한 식당 수 (2000년~2019년)
        */

        outFile << *(location + i * NUM_COLUMNS + 0) << ","
            << *(location + i * NUM_COLUMNS + 1) << ","
            << *(location + i * NUM_COLUMNS + 2) << ","
            << *(location + i * NUM_COLUMNS + 3) << ","
            << *(location + i * NUM_COLUMNS + 4) << ","
            << *(location + i * NUM_COLUMNS + 5) << ","
            << *(location + i * NUM_COLUMNS + 6) << ","
            << *(location + i * NUM_COLUMNS + 7);

        for (int y = 0; y < NUM_YEARS; y++)
            outFile << "," << *(result + i * (NUM_YEARS + 1) + (y + 1));
        outFile << endl;
    }
    outFile.close();

    delete[] location;
    delete[] result;
    cout << "Finished getNearbyClosedRestaurants()!" << endl;
}