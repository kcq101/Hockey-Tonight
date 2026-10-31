import json
J=[]
def add(nm,anim,times,grab=0):
    for i,t in enumerate(times): J.append({'name':f'{nm}_{i}','anim':anim,'t':t,'grab':grab})
idle=[3.67*i/8 for i in range(8)]
add('guard','Idle_10',idle)
add('hold','Idle_10',idle,1)
add('jab','Right_Jab_from_Guard',[.25,.42,.56,.67,.83,1.05],1)
add('ljab','Left_Jab_from_Guard',[.14,.3,.44,.58,.75,.98])
add('upper','Right_Uppercut_from_Guard',[.12,.25,.38,.5,.6,.7,.8,.92],1)
add('block','Block2',[1.6*i/8 for i in range(8)])
add('hurt','Face_Punch_Reaction',[.45,.62,.8,1.0,1.3,1.7,2.1,2.45])
add('ko','Dead',[2.97*i/11 for i in range(12)])
add('flex','Show_Both_Arm_Muscles',[1.87*i/6 for i in range(6)])
json.dump(J,open('jobs.json','w')); print(len(J))
