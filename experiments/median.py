import sys

feature0 = 0.0
feature1 = 0.0
feature2 = 0.0
feature3 = 0.0
feature4 = 0.0
feature5 = 0.0
feature6 = 0.0
feature7 = 0.0
feature8 = 0.0
feature9 = 0.0
feature10 = 0.0
feature11 = 0.0
feature12 = 0.0
feature13 = 0.0
feature14 = 0.0
feature15 = 0.0
feature16 = 0.0
feature17 = 0.0
feature18 = 0.0
feature19 = 0.0

dir = sys.argv[1]
model =  sys.argv[2]
output = sys.argv[3]

f1 = ""
with open(dir + 'f1.' + model) as f:
    f1 = f.readlines()

f2 = ""
with open(dir + 'f2.' + model) as f:
    f2 = f.readlines()

f3 = ""
with open(dir + 'f3.' + model) as f:
    f3 = f.readlines()

f4 = ""
with open(dir + 'f4.' + model) as f:
    f4 = f.readlines()

f5 = ""
with open(dir + 'f5.' + model) as f:
    f5 = f.readlines()


model = open(dir + output, 'w')
model.write(f1[0])
model.write(f1[1])
model.write(f1[2])
model.write(f1[3])
model.write(f1[4])

for i in range(0,20):
	sum = float(f1[5 + i][4:][:-1])
	print(sum)
	sum += float(f2[5 + i].split(' ')[2][:-1])
	sum += float(f3[5 + i].split(' ')[2][:-1])
	sum += float(f4[5 + i].split(' ')[2][:-1])
	sum += float(f5[5 + i].split(' ')[2][:-1])
	model.write(f1[5 + i].split(' ')[0] + ' ' + f1[5 + i].split(' ')[1] + ' ' + str(sum/5) + f1[5 + i][-1:])
	print(sum/5)

