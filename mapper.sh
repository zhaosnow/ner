#!/usr/bin/env bash
set -x
CMD_HADOOP_RM_DIR="sudo -uzhaox hadoop fs -rm -r "
CMD_HADOOP_STREAMING="sudo -uzhaox /usr/bin/hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar "
LOG() {
    echo "$(date '+%F %T')  $@"
}
ner() {
    local src_hdfs="hdfs:////user/hive/warehouse/zhihu.db/pure_question"
    # local  src_hdfs="hdfs:///user/zhaox/output/quetion.txt"
    local  dst_hdfs="hdfs:///user/zhaox/seg_output"
    ${CMD_HADOOP_RM_DIR} ${dst_hdfs}

    ${CMD_HADOOP_STREAMING}\
        -D mapreduce.job.name="Segment" \
        -file "movie_extract.py"\
        -file "result.txt"\
        --mapper "/usr/bin/python2.7 movie_extract.py"\
        --input ${src_hdfs} \
        --output ${dst_hdfs} \
        -cmdenv LC_CTYPE="zh_CN.UTF-8"

    LOG "DONE"
}
ner
set +x