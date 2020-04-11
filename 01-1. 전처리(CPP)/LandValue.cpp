#include "LandValue.h"

void getLandValue()
{
    ::cout << "Execute getLandValue()" << endl;
    string rootDir = "D:\\Research\\Data\\";
    string restFilePath = "D:\\Research\\Data\\99.Location_Restaurants.csv";    
    string landvalueFilename = "_LandValue.csv";
    string outPath = "D:\\Research\\Data\\99.LandValue.csv";

    // Step1. �Ϲ��������� ��ǥ ������ �б�    
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
    
    // Step2: ������ �������� ������ �б�
    const int NUM_YEARS = 10;
    const int FIRST_YEAR = 2010;
    const int NUM_LANDVALUE_COLUMNS = 5;
    // �ϴ� �ӽ÷� 7000���� �ִٰ� �����ϰ� �����͸� �Է�
    const int TEMP_NUM_RECORDS = 7000;
    double* landvalue[NUM_YEARS];
    // �������� ���ڵ� ������ �� ������ ����    
    int numRecords[NUM_YEARS];
    
    ::cout << "Step2. Read LandValue files..." << endl;
    // ������ ������ �б�
    for (int y = 0; y < NUM_YEARS; y++) {
        string tmp = rootDir + "42." + to_string(FIRST_YEAR + y) + landvalueFilename;
        ::cout << "\tReading " << tmp << "..." << endl;
        // 7000�� ���ڵ尡 �ִٰ� ����
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

    // �������� ����
    // 1:�ְ�, 2:���, 3:����, 4:����, 5:��������, 6:����
    const int NUM_LANDTYPES = 6;    
    // ����� ������ ����
    int* result = new int[NUM_REST * (2 * NUM_YEARS + 1)];
    // �ݰ�
    const double RADIUS = 500.0;

    // Step3: �������� �Ĵ� ������ ��� ��������(������ ���� ������� ���) �� �̿����
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

        // �Ĵ� ��ȣ ����� ����
        *(result + i * (NUM_YEARS * 2 + 1) + 0) = no;                
        
        // ������ �ֺ� �� ����, ��������, ��������
        double total_area[NUM_YEARS];
        double total_landvalue[NUM_YEARS];
        int land_type[NUM_YEARS];

        // �Ĵ��� ��ġ������ ������ ��簪�� -1�� �������� ����(���� �м��� ����)
        for (int y = 0; y < NUM_YEARS; y++) {
            total_area[y] = total_landvalue[y] = -1.0;
            land_type[y] = -1;
        }

        // �Ĵ��� ��ġ������ �ִ� ��쿡�� ���
        if (latitude != 0.0) {
            for (int y = 0; y < NUM_YEARS; y++) {
                total_area[y] = total_landvalue[y] = 0.0;
                land_type[y] = 0;

                double total_area_landtype[NUM_LANDTYPES];
                for (int j = 0; j < NUM_LANDTYPES; j++)
                    total_area_landtype[j] = 0.0;

                // ���翬���� �������� �����͸� �˻��ؼ� ������ ��ó ���� ����, ��������, ���������� ���ϱ�
                for (int j = 0; j < numRecords[y]; j++) {
                    double tmp_latitude = *(landvalue[y] + j * NUM_LANDVALUE_COLUMNS + 0);
                    double tmp_longitude = *(landvalue[y] + j * NUM_LANDVALUE_COLUMNS + 1);
                    int tmp_type = int(*(landvalue[y] + j * NUM_LANDVALUE_COLUMNS + 2));
                    double tmp_area = *(landvalue[y] + j * NUM_LANDVALUE_COLUMNS + 3);
                    double tmp_landvalue = *(landvalue[y] + j * NUM_LANDVALUE_COLUMNS + 4);

                    double dist = calculateDistance(latitude, longitude, tmp_latitude, tmp_longitude);
                    // �ݰ� �ȿ� ��ġ�� ���
                    if (dist <= RADIUS) {
                        total_area_landtype[tmp_type - 1] += tmp_area;
                        total_area[y] += tmp_area;
                        total_landvalue[y] += (tmp_area * tmp_landvalue);
                    }
                }

                // �������� �� ������ ���� ���� ���� ����
                double tmp_max = 0.0;
                int tmp_index = 0;
                for (int j = 0; j < NUM_LANDTYPES; j++) {
                    if (total_area_landtype[j] > tmp_max) {
                        tmp_index = j;
                        tmp_max = total_area_landtype[j];
                    }
                }
                // �ε����� 0���� ���������� ���������� 1���� �����ϹǷ�...                
                // ���࿡ ������ ������ -1 �Է�
                if (total_area[y] == 0)
                    land_type[y] = -1;
                else
                    land_type[y] = tmp_index + 1;
            }
        }

        // �������
        // 1. �Ĵ� ��ȣ
        *(result + i * (NUM_YEARS * 2 + 1) + 0) = no;
        // ������ ��� ����
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

    // �������
    outFile << "No";
    for (int y = 0; y < NUM_YEARS; y++)
        outFile << "," << to_string(y + FIRST_YEAR) + " LandType" << "," << to_string(y + FIRST_YEAR) + " AvgLandValue";
    outFile << endl;

    //Step4: ��� �����ϱ�    
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