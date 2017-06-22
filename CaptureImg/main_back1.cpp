 /*
* Copyright(C) 2011,Hikvision Digital Technology Co., Ltd 
* 
* File   name��main.cpp
* Discription��demo for muti thread get stream
* Version    ��1.0
* Author     ��luoyuhua
* Create Date��2011-12-10
* Modification History��
*/

#include <stdio.h>
#include <unistd.h>
#include <errno.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "HCNetSDK.h"
#include "iniFile.h"
#include <fstream>
#include <iostream>
#include <string>
using namespace std;

typedef struct tagREAL_PLAY_INFO
{
	char szIP[16];
	int iUserID;
	int iChannel;
}REAL_PLAY_INFO, *LPREAL_PLAY_INFO;

string *CameraTask = new string[10];
int Num=0;
int CameraID[10];
int CameraChannel[10];
NET_DVR_JPEGPARA CameraJpegParas[10];
string *CameraPath = new string[100];

void GetCamera()
{
	ifstream in;
	char filename[100];
	//char filename = "../human_count_project/CameraList.txt";
	strcpy(filename,"../human_count_project/CameraList.txt");
	string s;
	in.open(filename);
	while (getline(in,s))
	{
		CameraTask[Num] = s.c_str();
		cout << CameraTask[Num]<< endl;
		Num++;
	}
}

void OpenCamera()
{
	for(int i=0;i<Num;i++)
	{
		char *TaskID = new char[CameraTask[i].size()+1];
		strcpy(TaskID, CameraTask[i].c_str());
		char DeviceDir[] = "../human_count_project/camera/";
		strcat(DeviceDir,TaskID);
		strcat(DeviceDir,"/config/Device.ini");
		IniFile ini(DeviceDir);  //读取配置文件
		unsigned int dwSize = 0;
		char sSection[16] = "DEVICE";

		char *sIP = ini.readstring(sSection, "ip", "error", dwSize);
		int iPort = ini.readinteger(sSection, "port", 0);
		char *sUserName = ini.readstring(sSection, "username", "error", dwSize);
		char *sPassword = ini.readstring(sSection, "password", "error", dwSize);
		int iChannel = ini.readinteger(sSection, "channel", 0);

		NET_DVR_DEVICEINFO_V30 struDeviceInfo;  //设备参数结构体
		int iUserID = NET_DVR_Login_V30(sIP, iPort, sUserName, sPassword, &struDeviceInfo); //相机注册
		NET_DVR_JPEGPARA JpegPara  = {0xff,0};
		char ImagePath[] = "../human_count_project/camera/";
		strcat(ImagePath,TaskID);
		strcat(ImagePath,"/");

		CameraID[i] = iUserID;
		CameraChannel[i] = iChannel;
		CameraJpegParas[i] = JpegPara;
		CameraPath[i] = ImagePath;

		cout << CameraID[i]<< endl;
		cout << CameraChannel[i] << endl;



	}
}

void GetJPG()
{
	while(1)
	{
		for(int i=0;i<Num;i++)
		{
			char ImagePath[] = "../human_count_project/camera/";
			char *TaskID = new char[CameraTask[i].size()+1];
			strcpy(TaskID, CameraTask[i].c_str());
			strcat(ImagePath,TaskID);
			strcat(ImagePath,"/");
			time_t timer = time(NULL);
			strcat(ImagePath,ctime(&timer));
			strcat(ImagePath,".src.jpg");
			int CaptureImg = NET_DVR_CaptureJPEGPicture(CameraID[i],CameraChannel[i],&CameraJpegParas[i],ImagePath);
		}
		sleep(5);
	}
}

int main()
{
    NET_DVR_Init();
	NET_DVR_SetLogToFile(3, "./record/");
	
	GetCamera();
	OpenCamera();
	GetJPG();

	char c = 0;
	while('q' != c)
	{
		printf("input 'q' to quit\n");
		printf("input: ");
		scanf("%c", &c);
	}


    NET_DVR_Cleanup();
    return 0;
}


