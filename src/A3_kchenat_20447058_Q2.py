import csv;
import numpy;


def getData():
    filename = '/Users/chenkang/Desktop/DM/Assingment3/dataset/Q2Q3_input.csv';
    data = [];
    with open(filename) as label:
        reader = csv.DictReader(label);
        numberOfId = 0;
        for row in reader:
            data.append([float(row['load_video']),float(row['pause_video']),float(row['play_video']),float(row['seek_video']),float(row['speed_change_video']),float(row['stop_video'])])
            numberOfId += 1;
        print 'having load :' + str(numberOfId) + ' ids';
    return data;

def dist(x,y):
    dist = 0;
    for i in range(0,len(x)):
        dist += ( x[i] - y[i] ) * ( x[i] - y[i] );
    return dist;

def wight( x, c1 , c2 ):
    return dist(x,c2) * 1.0 /( dist(x,c1) + dist(x,c2) );

def EM_Algrothm():
    data = getData();
    c1 = [1, 1, 1, 1, 1, 1];
    c2 = [0, 0, 0, 0, 0, 0];
    # data = [[3,3],[4,10],[9,6],[14,8],[18,11],[21,7]];
    # c1 = [3,3];
    # c2 = [4,10];
    count = 0;
    while 1==1:
        # E-step
        matrix = [];
        for row in data:
            matrix.append([wight(row,c1,c2),1-wight(row,c1,c2)]);
        # M-step
        # new_c1_up = [0, 0];
        # new_c2_up = [0, 0];
        # new_c1_down = [0, 0];
        # new_c2_down = [0, 0];
        new_c1_up = [0, 0, 0, 0, 0, 0];
        new_c2_up = [0, 0, 0, 0, 0, 0];
        new_c1_down = [0, 0, 0, 0, 0, 0];
        new_c2_down = [0, 0, 0, 0, 0, 0];
        for j in range(0,len(data)):
            for i in range(0,len(new_c1_up)):
                new_c1_up[i] += 1.0 * data[j][i] * matrix[j][0] * matrix[j][0];
                new_c1_down[i] += 1.0 * matrix[j][0] * matrix[j][0];
                new_c2_up[i] += 1.0 * data[j][i] * matrix[j][1] * matrix[j][1];
                new_c2_down[i] += 1.0 * matrix[j][1] * matrix[j][1];
        new_c2 = [0, 0, 0, 0, 0, 0];
        new_c1 = [0, 0, 0, 0, 0, 0];
        # new_c2 = [0, 0];
        # new_c1 = [0, 0];
        for i in range(0, len(new_c1_up)):
            new_c1[i] += 1.0 * new_c1_up[i] / new_c1_down[i];
            new_c2[i] += 1.0 * new_c2_up[i] / new_c2_down[i];
        count += 1;
        print 'it is ' + str(count) + ' iterations! c1 = ' + str(new_c1) + ';\n c2 = ' + str(new_c2);
        if numpy.sqrt(dist(c1,new_c1)) < 0.001 and numpy.sqrt(dist(c2,new_c2)) < 0.001:
            c1 = new_c1;
            c2 = new_c2;
            break;
        else:
            c1 = new_c1;
            c2 = new_c2;
        if count >= 50:
            break;
        if count <= 2:
            sse = 0.0;
            for i in range(0,len(data)):
                sse += pow(matrix[i][0],2) * dist(data[i],c1);
                sse += pow(matrix[i][1],2) * dist(data[i],c2);
            print 'the SSE is ' + str(sse) + '!';


EM_Algrothm();
#print str(wight([14,8],[3,3],[4,10]));