#include "LandValue.h"

void getLandValue()
{
    ::cout << "Execute getLandValue()" << endl;
    string rootDir = "D:\\Research\\Data\\";
    string restFilePath = "D:\\Research\\Data\\99.Location_Restaurants.csv";    
    string landvalueFilename = "_LandValue.csv";
    string outPath = "D:\\Research\\Data\\99.LandValue.csv";

    // Step1. 일반음식점의 좌표 데이터 읽기    
    ifstream in(restFilePath.data());
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

    ::cout << "Step1. Read " << restFilePath << endl;

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
    
    // Step2: 연도별 공시지가 데이터 읽기
    const int NUM_YEARS = 10;
    const int FIRST_YEAR = 2010;
    const int NUM_LANDVALUE_COLUMNS = 5;
    // 일단 임시로 7000건이 있다고 가정하고 데이터를 입력
    const int TEMP_NUM_RECORDS = 7000;
    double* landvalue[NUM_YEARS];
    // 연도별로 레코드 개수가 몇 개인지 저장    
    int numRecords[NUM_YEARS];
    
    ::cout << "Step2. Read LandValue files..." << endl;
    // 연도별 데이터 읽기
    for (int y = 0; y < NUM_YEARS; y++) {
        string tmp = rootDir + "42." + to_string(FIRST_YEAR + y) + landvalueFilename;
        ::cout << "\tReading " << tmp << "..." << endl;
        // 7000개 레코드가 있다고 가정
        landvalue[y] = new double[TEMP_NUM_RECORDS * NUM_LANDVALUE_COLUMNS];
        numRecords[y] = 0;

        ifstream in(tmp.data());
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

        while (in) {
            in.getline(buf, BUFFER_SIZE);
            if (strlen(buf) < 10) break;
            vector<string> result = split(&buf[0]);
            for (int i = 0; i < NUM_LANDVALUE_COLUMNS; i++) {
                //::cout << result[i] << " ";
                *(landvalue[y] + cnt * NUM_LANDVALUE_COLUMNS + i) = stod(result[i]);
            }
            //::cout << endl;
            cnt++;
            /* For Test...
            if (nLIMIT <= cnt)
                break;
            //*/
        }
        numRecords[y] = cnt;

        in.close();
    }

    // 토지유형 개수
    // 1:주거, 2:상업, 3:공업, 4:녹지, 5:관리지역, 6:농림지
    const int NUM_LANDTYPES = 6;    
    // 결과를 저장할 변수
    int* result = new int[NUM_REST * (2 * NUM_YEARS + 1)];
    // 반경
    const double RADIUS = 500.0;

    // Step3: 연도별로 식당 주위의 평균 공시지가(면적에 따른 가중평균 사용) 및 이용상태
    ::cout << "Step3. Get land type and average land value..." << endl;
    for (int i = 0; i < NUM_REST; i++) {
        // Columns = [ Index,No,OpenYear,OpenMonth,CloseYear,CloseMonth,Menu,Latitude,Longitude ]
        if (i % 1000 == 0)
            ::cout << to_string(i) << "/" << to_string(NUM_REST) << endl;
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

        // 식당 번호 결과에 저장
        *(result + i * (NUM_YEARS * 2 + 1) + 0) = no;                
        
        // 연도별 주변 총 면적, 공시지가, 토지유형
        double total_area[NUM_YEARS];
        double total_landvalue[NUM_YEARS];
        int land_type[NUM_YEARS];

        // 식당의 위치정보가 없으면 모든값이 -1로 나오도록 설정(향후 분석시 제외)
        for (int y = 0; y < NUM_YEARS; y++) {
            total_area[y] = total_landvalue[y] = -1.0;
            land_type[y] = -1;
        }

        // 식당의 위치정보가 있는 경우에만 계산
        if (latitude != 0.0) {
            for (int y = 0; y < NUM_YEARS; y++) {
                total_area[y] = total_landvalue[y] = 0.0;
                land_type[y] = 0;

                double total_area_landtype[NUM_LANDTYPES];
                for (int j = 0; j < NUM_LANDTYPES; j++)
                    total_area_landtype[j] = 0.0;

                // 현재연도의 공시지가 데이터를 검색해서 음식점 근처 땅의 면적, 공시지가, 토지유형을 구하기
                for (int j = 0; j < numRecords[y]; j++) {
                    double tmp_latitude = *(landvalue[y] + j * NUM_LANDVALUE_COLUMNS + 0);
                    double tmp_longitude = *(landvalue[y] + j * NUM_LANDVALUE_COLUMNS + 1);
                    int tmp_type = int(*(landvalue[y] + j * NUM_LANDVALUE_COLUMNS + 2));
                    double tmp_area = *(landvalue[y] + j * NUM_LANDVALUE_COLUMNS + 3);
                    double tmp_landvalue = *(landvalue[y] + j * NUM_LANDVALUE_COLUMNS + 4);

                    double dist = calculateDistance(latitude, longitude, tmp_latitude, tmp_longitude);
                    // 반경 안에 위치할 경우
                    if (dist <= RADIUS) {
                        total_area_landtype[tmp_type - 1] += tmp_area;
                        total_area[y] += tmp_area;
                        total_landvalue[y] += (tmp_area * tmp_landvalue);
                    }
                }

                // 토지유형 중 면적이 가장 넓은 것을 선택
                double tmp_max = 0.0;
                int tmp_index = 0;
                for (int j = 0; j < NUM_LANDTYPES; j++) {
                    if (total_area_landtype[j] > tmp_max) {
                        tmp_index = j;
                        tmp_max = total_area_landtype[j];
                    }
                }
                // 인덱스는 0부터 시작하지만 토지유형은 1부터 시작하므로...                
                // 만약에 정보가 없으면 -1 입력
                if (total_area[y] == 0)
                    land_type[y] = -1;
                else
                    land_type[y] = tmp_index + 1;
            }
        }

        // 결과저장
        // 1. 식당 번호
        *(result + i * (NUM_YEARS * 2 + 1) + 0) = no;
        // 연도별 결과 저장
        for (int y = 0; y < NUM_YEARS; y++) {
            *(result + i * (NUM_YEARS * 2 + 1) + 2 * y + 1) = int(land_type[y]);
            double avg_landvalue = -1;
            if ( total_area[y] != 0 )
                avg_landvalue = total_landvalue[y] / total_area[y];
            *(result + i * (NUM_YEARS * 2 + 1) + 2 * y + 2) = int(avg_landvalue);
        }        
    }

    ::cout << "Step4. Save the result..." << endl;
    ofstream outFile = ofstream(outPath.data());

    // 헤더쓰기
    outFile << "No";
    for (int y = 0; y < NUM_YEARS; y++)
        outFile << "," << to_string(y + FIRST_YEAR) + " LandType" << "," << to_string(y + FIRST_YEAR) + " AvgLandValue";
    outFile << endl;

    //Step4: 결과 저장하기    
    for (int i = 0; i < NUM_REST; i++) {
        outFile << *(result + i * (NUM_YEARS * 2 + 1) + 0);
        for (int y = 0; y < NUM_YEARS; y++) {            
            outFile << "," << *(result + i * (NUM_YEARS * 2 + 1) + 2 * y + 1)
                << "," << *(result + i * (NUM_YEARS * 2 + 1) + 2 * y + 2);
        }
        outFile << endl;
    }

    outFile.close();

    delete[] location;
    for (int i = 0; i < NUM_YEARS; i++)
        delete[] landvalue[i];
    delete result;
    
    cout << "Finished getLandValue()!" << endl;
}