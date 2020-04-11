#include "ConvenientStores.h"

## �ۼ�����... Python���δ� �� 20�� �ҿ�

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
    �� ����� ������ �׸� (�뷫 �� ����� 500m ����)
       - ������ : �Ĵ��� ����(���㰡)�� ���� (�ش� ���� ����)
         => �ݰ� 500m �� �������� ������ ��
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

        // �Ĵ� ��ȣ ����
        *(convStores + i * NUM_OUT_COLUMNS + 0) = no;

                   
        
        // 2. �ݰ� 500m �� �Ĵ� ��
        *(competition + i * NUM_OUT_COLUMNS + 1) = cntNearby;
        // 3. �ݰ� 500m �� ���� �޴� �Ĵ� ��
        
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
        �� ����� ������ �׸� (�뷫 �� ����� 500m ����)
           - ������ : �Ĵ��� ����(���㰡)�� ���� (�ش� ���� ����)
          1. �Ĵ� ��ȣ
          2. �Ĵ��� ��������
          3. �Ĵ��� ������
          4. �Ĵ��� �������
          5. �Ĵ��� �����
          6. �Ĵ� �޴�
          7. �ݰ� 500m �� �������� ������ ��          
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