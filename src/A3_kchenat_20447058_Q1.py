import csv;
import datetime as dt;
from sklearn.neighbors import KNeighborsClassifier

def getTrainData():
    filenameOflabel = '/Users/chenkang/Desktop/DM/Assingment3/dataset/TrainLabel.csv'
    data = [];
    with open(filenameOflabel) as label:
        reader = csv.DictReader(label);
        numberOfId = 0;
        for row in reader:
            data.append(
                {'id': row['user_id'], 'grade': row['grade'], "numOfBack": 0, 'numOfForward': 0, 'numOfPause': 0,
                 'numOflearning': 0, 'totalTime': 0, 'numOfFast': 0, 'numOfSlow': 0, 'currentSession': 'null',
                 'startTime': 'null', 'currentVedio': 'null'});
            numberOfId += 1;
        print 'having load :' + str(numberOfId) + ' ids';
    return data
def getTestData():
    filenameOflabel = '/Users/chenkang/Desktop/DM/Assingment3/dataset/TestData.csv'
    data = [];
    with open(filenameOflabel) as label:
        reader = csv.DictReader(label);
        numberOfId = 0;
        for row in reader:
            data.append(
                {'id': row['user_id'], 'grade': -1, "numOfBack": 0, 'numOfForward': 0, 'numOfPause': 0,
                 'numOflearning': 0, 'totalTime': 0, 'numOfFast': 0, 'numOfSlow': 0, 'currentSession': 'null',
                 'startTime': 'null', 'currentVedio': 'null'});
            numberOfId += 1;
        print 'having load :' + str(numberOfId) + ' test ids';
    return data

def prepareData( emptyData , filename):
    # filename = '/Users/chenkang/Desktop/DM/Assingment3/dataset/TrainFeatures.csv'
    data = emptyData;
    with open(filename) as f:
        reader = csv.DictReader(f);
        current = {'id':'null','index':-1};
        for row in reader:
            if current['id']==row['user_id']:
                index = current['index'];
                if row['event_type'] == 'seek_video' and float(row['old_time']) > float(row['new_time']):
                    data[index]['numOfBack'] += 1;
                elif row['event_type'] == 'seek_video' and float(row['old_time']) <= float(row['new_time']):
                    data[index]['numOfForward'] += 1;
                elif row['event_type'] == 'speed_change_video' and float(row['new_speed']) > float(row['old_speed']):
                    data[index]['numOfFast'] += 1;
                elif row['event_type'] == 'speed_change_video' and float(row['new_speed']) <= float(row['old_speed']):
                    data[index]['numOfSlow'] += 1;
                elif row['event_type'] == 'pause_video':
                    data[index]['numOfPause'] += 1;
                elif row['video_id'] != data[index]['currentVedio']:
                    data[index]['currentVedio'] = row['video_id'];
                    data[index]['numOflearning'] += 1;
                elif row['session'] != data[index]['currentSession']:
                    data[index]['currentVedio'] = row['video_id'];
                    data[index]['currentSession'] = row['session'];
                    data[index]['numOflearning'] += 1;
                # print data[index];
                if row['event_type'] != 'load_video' :
                    if data[index]['startTime'] != 'null' and row['event_time'] != "null":
                        oldTime = dt.datetime.strptime(data[index]['startTime'],"%Y-%m-%d %H:%M:%S.%f");
                        nweTime = dt.datetime.strptime(row['event_time'],"%Y-%m-%d %H:%M:%S.%f");
                        duration = (nweTime - oldTime).seconds;
                        if duration > 0:
                            data[index]['totalTime'] += duration;
                    data[index]['startTime'] = row['event_time'];
            else :
                current['id'] = row['user_id'];
                for i in range(0,len(data)-1,1):
                    if data[i]['id'] == row['user_id']:
                        current['index'] = i;
                        break
                index = current['index'];
                if row['event_type'] == 'seek_video' and float(row['old_time']) > float(row['new_time']):
                    data[index]['numOfBack'] += 1;
                elif row['event_type'] == 'seek_video' and float(row['old_time']) <= float(row['new_time']):
                    data[index]['numOfForward'] += 1;
                elif row['event_type'] == 'speed_change_video' :
                    if float(row['new_speed']) > float(row['old_speed']):
                        data[index]['numOfFast'] += 1;
                    else:
                        data[index]['numOfSlow'] += 1;
                elif row['event_type'] == 'pause_video':
                    data[index]['numOfPause'] += 1;
                elif row['video_id'] != data[index]['currentVedio']:
                    data[index]['currentVedio'] = row['video_id'];
                    data[index]['numOflearning'] += 1;
                elif row['session'] != data[index]['currentSession']:
                    data[index]['currentVedio'] = row['video_id'];
                    data[index]['currentSession'] = row['session'];
                    data[index]['numOflearning'] += 1;
                # print data[index]
                if row['event_type'] != 'load_video' :
                    if data[index]['startTime'] != 'null' and row['event_time'] != "null":
                        oldTime = dt.datetime.strptime(data[index]['startTime'],"%Y-%m-%d %H:%M:%S.%f");
                        nweTime = dt.datetime.strptime(row['event_time'],"%Y-%m-%d %H:%M:%S.%f");
                        duration = (nweTime - oldTime).seconds;
                        if duration > 0:
                            data[index]['totalTime'] += duration;
                    data[index]['startTime'] = row['event_time'];
            # print 'working on the other row......'
    return data

def main():
    # emptyData = getTrainData();
    # trainData = prepareData(emptyData,'/Users/chenkang/Desktop/DM/Assingment3/dataset/TrainFeatures.csv');
    # print 'finished training!'
    # emptyTestData = getTestData();
    # testData = prepareData(emptyTestData,'/Users/chenkang/Desktop/DM/Assingment3/dataset/TestFeatures.csv');
    # print 'finished test data!'
    # h1 = ['id', 'grade', "numOfBack", 'numOfForward', 'numOfPause','numOflearning', 'totalTime', 'numOfFast', 'numOfSlow', 'currentSession','startTime', 'currentVedio'];
    # with open('temp1.csv', 'w') as f:
    #     writer = csv.DictWriter(f,h1);
    #     writer.writeheader();
    #     for row in trainData:
    #         writer.writerow({'id': row['id'], 'grade': row['grade'], "numOfBack": row['numOfBack'], 'numOfForward': row['numOfForward'], 'numOfPause': row['numOfPause'],'numOflearning': row['numOflearning'], 'totalTime': row['totalTime'], 'numOfFast': row['numOfFast'], 'numOfSlow': row['numOfSlow']});
    # with open('temp2.csv', 'w') as f:
    #     writer = csv.DictWriter(f, h1);
    #     writer.writeheader()
    #     for row in testData:
    #         writer.writerow({'id': row['id'], 'grade': row['grade'], "numOfBack": row['numOfBack'],
    #                          'numOfForward': row['numOfForward'], 'numOfPause': row['numOfPause'],
    #                          'numOflearning': row['numOflearning'], 'totalTime': row['totalTime'],
    #                          'numOfFast': row['numOfFast'], 'numOfSlow': row['numOfSlow']});
    # print 'finished to temp1,temp2!start to classify!'
    # trainAttribut = [];
    # trainLabel = [];
    # for row in trainData:
    #     trainAttribut.append([int(row['numOfBack']),int(row['numOfForward']),int(row['numOfPause']),int(row['numOflearning']),int(row['numOfFast']),int(row['numOfSlow']),int(row['totalTime'])]);
    #     trainLabel.append(int(row['grade']));
    # testAttribut = [];
    # ids = [];
    # for row in testData:
    #     testAttribut.append([int(row['numOfBack']),int(row['numOfForward']),int(row['numOfPause']),int(row['numOflearning']),int(row['numOfFast']),int(row['numOfSlow']),int(row['totalTime'])]);
    #     ids.append(row['id']);
    ################################################################################################################
    # all above is the data from memory! all below is data from temp1,temp2 for saving time the result is the same!#
    ################################################################################################################
    trainAttribut = [];
    trainLabel = [];
    with open('temp1.csv') as trainDataFile:
        reader = csv.DictReader(trainDataFile);
        for row in reader:
            trainAttribut.append([int(row['numOfBack']),int(row['numOfForward']),int(row['numOfPause']),int(row['numOflearning']),int(row['numOfFast']),int(row['numOfSlow'])]);
            trainLabel.append(int(row['grade']))
    testAttribut = [];
    ids = [];
    with open('temp2.csv') as trainDataFile:
        reader = csv.DictReader(trainDataFile);
        for row in reader:
            testAttribut.append([int(row['numOfBack']),int(row['numOfForward']),int(row['numOfPause']),int(row['numOflearning']),int(row['numOfFast']),int(row['numOfSlow'])]);
            ids.append(row['id']);
    ###########################################
    # all above is the data from temp1,temp2! #
    ###########################################
    knn = KNeighborsClassifier(n_neighbors=3,leaf_size=90,n_jobs=-1);
    knn.fit(trainAttribut,trainLabel);
    result = knn.predict(testAttribut);
    print 'finished prediction!';
    header = ['user_id','grade'];
    with open('A3_kchenat_20447058_Q1prediction.csv', 'w') as f:
        writer = csv.DictWriter(f,header);
        writer.writeheader();
        for i in range(0,len(testAttribut)-1):
            writer.writerow({'user_id':ids[i],'grade':result[i]});

def test_main():
    trainAttribut = [];
    trainLabel = [];
    count = 0;
    testAttribut = [];
    testLabel = [];
    totalTime = 0;
    # with open('/Users/chenkang/Desktop/DM/Assingment3/dataset/VideoInfo.csv') as time:
    #     reader = csv.DictReader(time);
    #     for row in reader:
    #         totalTime += float(row['duration']);
    with open('temp1.csv') as trainDataFile:
        reader = csv.DictReader(trainDataFile);
        for row in reader:
            if count <=3000:
                count += 1;
                trainAttribut.append(
                    [int(row['numOfBack']), int(row['numOfForward']), int(row['numOfPause']), int(row['numOflearning']),
                     int(row['numOfFast']), int(row['numOfSlow'])]);
                trainLabel.append(int(row['grade']))
            else:
                testAttribut.append(
                    [int(row['numOfBack']), int(row['numOfForward']), int(row['numOfPause']), int(row['numOflearning']),
                     int(row['numOfFast']), int(row['numOfSlow'])]);
                testLabel.append(int(row['grade']));
    knn = KNeighborsClassifier(n_neighbors=3, leaf_size=90, n_jobs=-1);
    knn.fit(trainAttribut, trainLabel);
    result = knn.predict(testAttribut);
    correctNum = 0;
    for i in range(0,len(result)):
        if result[i] == testLabel[i]:
                correctNum += 1;
    print correctNum * 1.00 / len(result)

# main() is for submission,and the test_main() is for work out my correct rate!
main();
# test_main()