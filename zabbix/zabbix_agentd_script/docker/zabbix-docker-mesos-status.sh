#!/bin/bash
#set -x
#status_txt为存放截取mesos中容器task_id
status_txt=/tmp/mesos-container-status-$1
#curl -s "http://mesos-exporter/metrics"获取container消亡的状态
curl -s "http://192.168.3.7:19110/metrics" | grep mesos_slave_task_state_time | grep -v "#" | cut -d "="  -f 5 | cut -d "\"" -f 2 > $status_txt
#把status_txt中的值存入数组
results=(`cat $status_txt`)
#查看数组中有多少为输入的task_id
samenum=`cat $status_txt | grep $1 | wc -l`
#取数组长度
num=${#results[@]}
#查看输入是否为mysql相关的有状态服务,因为有状态服务task-id 不变
echo $1 > /tmp/$1.txt
input=`cat /tmp/$1.txt | grep mysql`
#如果没有mysql，则判断截取的task_id中是否有$1,有输出１，没有输出0.
#如果有mysql,则输出相匹配的$1数量.
#判断自动发现脚本里的容器名字是否与数组相匹配，有匹配说明该容器为消亡状态
if      [ -z $input ]
        then
                for((i=0;i<=$num;i++));
                        do
                                if [ "${results[$i]}" == "$1" ]
                                        then status=1
                                        break
                                else status=0
                                fi
                        done
                echo $status
        else
                echo $samenum
fi

