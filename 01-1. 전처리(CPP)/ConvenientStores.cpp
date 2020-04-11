#include "ConvenientStores.h"

## 작성중임... Python으로는 약 20분 소요

void getNearbyConvenientStores()
{
    ::cout << "Execute getNearByRestaurants()" << endl;
    string filePath = "D:\\Research\\Data\\99.Location_Restaurants.csv";
    string outfilePath = "D:\\Research\\Data\\01-1.NearbyConvenientStores.csv";
    string convfilePath = "D:\\Research\\Data\\99.Location_Restaurants.csv";

    // read file
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

    const int NUM_REST = 13530;
    const int NUM_COLUMNS = 9;
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


    ::cout << "Step2. Read " << filePath << endl;


    /*
    ㅁ 결과에 포함할 항목 (대략 한 블록이 500m 정도)
       - 기준일 : 식당이 개업(인허가)한 연월 (해당 달을 포함)
         => 반경 500m 내 영업중인 편의점 수
    */
    ::cout << "Step2. Count nearby convenient stores..." << endl;
    const int NUM_OUT_COLUMNS = 2;
    int* convStores = new int[NUM_REST * NUM_OUT_COLUMNS];

    for (int i = 0; i < NUM_REST; i++) {
        // Columns = [ Index,No,OpenYear,OpenMonth,CloseYear,CloseMonth,Menu,Latitude,Longitude ]
        int no = int(location[i * NUM_COLUMNS + 1]);
        int openYear = int(location[i * NUM_COLUMNS + 2]);
        int openMonth = int(location[i * NUM_COLUMNS + 3]);
        int closeYear = int(location[i * NUM_COLUMNS + 4]);
        int closeMonth = int(location[i * NUM_COLUMNS + 5]);
        int menu = int(location[i * NUM_COLUMNS + 6]);
        double latitude = location[i * NUM_COLUMNS + 7];
        double longitude = location[i * NUM_COLUMNS + 8];
        /*
        ::cout << "Restaurants No." << to_string(no) << " Menu: " << to_string(menu)
            << " Open " << to_string(openYear) << "-" << to_string(openMonth)
            << " Close " << to_string(closeYear) << "-" << to_string(closeMonth) << endl;
        //*/
        int cntNearby = -1;        

        // 식당 번호 저장
        *(convStores + i * NUM_OUT_COLUMNS + 0) = no;

                   
        
        // 2. 반경 500m 내 식당 수
        *(competition + i * NUM_OUT_COLUMNS + 1) = cntNearby;
        // 3. 반경 500m 내 동일 메뉴 식당 수
        
        /* For Test...
        if (i >= nLIMIT)
            break;
        //*/
    }

    ::cout << "Step3. Save output..." << endl;
    string outPath = "d:/research/data/NearbyConvenientStores.csv";
    ofstream outFile = ofstream(outPath.data());

    for (int i = 0; i < NUM_REST; i++) {        
        /*
        ㅁ 결과에 포함할 항목 (대략 한 블록이 500m 정도)
           - 기준일 : 식당이 개업(인허가)한 연월 (해당 달을 포함)
          1. 식당 번호
          2. 식당의 개업연도
          3. 식당의 개업월
          4. 식당의 폐업연도
          5. 식당의 폐업월
          6. 식당 메뉴
          7. 반경 500m 내 영업중인 편의점 수          
        */
        outFile << *(location + i * NUM_COLUMNS + 1) << ","
            << *(location + i * NUM_COLUMNS + 2) << ","
            << *(location + i * NUM_COLUMNS + 3) << ","
            << *(location + i * NUM_COLUMNS + 4) << ","
            << *(location + i * NUM_COLUMNS + 5) << ","
            << *(location + i * NUM_COLUMNS + 6) << ","            
            << *(convStores + i * NUM_OUT_COLUMNS + 6) << ","
            << *(location + i * NUM_COLUMNS + 7) << ","
            << *(location + i * NUM_COLUMNS + 8) << endl;
    }

    outFile.close();

    delete[] location;
    delete[] convStores;
    ::cout << "Finished getNearbyConvenientStores()." << endl;

}