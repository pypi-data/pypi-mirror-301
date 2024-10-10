# coding:utf-8
from tools_hjh import DBConn, Tools, ProcessPool
from tools_hjh.Tools import locatdate
from tools_hjh import Log
from tools_hjh import ThreadPool
from tools_hjh import OracleTools
import time
import gc
from math import ceil
import sys

date = locatdate()

try:
    run_mode = sys.argv[2]
except:
    run_mode = None
try:
    config_file = sys.argv[1]
except:
    config_file = None
try:
    log_file = sys.argv[3]
except:
    log_file = date + '.log'
    
if config_file == None or config_file == 'help':
    print('python3 ora2pg.py xxx.conf mode_type xxx.log')
    print('mode_type: copy, report, compare_index, compare_constraint')
    print('xxx.log: default value YYYY-MM-DD.log')
    sys.exit()

Tools.rm(log_file)
log = Log(log_file)

conf = Tools.cat(config_file)
conf_map = {}
for line in conf.split('\n'):
    if '=' in line and '#' not in line:
        key = line.split('=')[0].strip()
        val = line.split('=')[1].strip()
        conf_map[key] = val

smallest_object = conf_map['smallest_object']
if_truncate = conf_map['if_truncate']
if_only_scn = conf_map['if_only_scn']

src_db_type = conf_map['src_db_type']
src_ip = conf_map['src_ip']
src_port = int(conf_map['src_port'])
src_database = conf_map['src_db']
src_read_username = conf_map['src_read_username']
src_read_password = conf_map['src_read_password']
# src_schema = conf_map['src_schema']

tables = conf_map['tables']
exclude_tables = conf_map['exclude_tables']
copy_from_sql = conf_map['copy_from_sql']

dst_db_type = conf_map['dst_db_type']
dst_ip = conf_map['dst_ip']
dst_port = int(conf_map['dst_port'])
dst_database = conf_map['dst_db']
dst_username = conf_map['dst_username']
dst_password = conf_map['dst_password']
# dst_schema = conf_map['dst_schema']

parallel_table_num = int(conf_map['parallel_table_num'])
table_parallel_num = int(conf_map['table_parallel_num'])
save_parallel_num = int(conf_map['save_parallel_num'])

commit_num = int(conf_map['commit_num'])
input_global_scn = conf_map['scn']

report = {}


def get_table_map_list(src_db):
    # 解析出需要迁移的表以及映射关系
    table_map_list = []
    for table_mess in tables.split(','):
        table_mess = table_mess.strip()
        if ':' in table_mess:
            src_schema = table_mess.split(':')[0].split('.')[0]
            src_table = table_mess.split(':')[0].split('.')[1]
            dst_schema = table_mess.split(':')[1].split('.')[0]
            dst_table = table_mess.split(':')[1].split('.')[1]
        else:
            src_schema = table_mess.split('.')[0]
            src_table = table_mess.split('.')[1]
            dst_schema = src_schema
            dst_table = src_table
            
        if src_table == '*':
            select_tables_sql = "select table_name from dba_tables where owner = '" + src_schema + "' order by 1"
            tables_from_sql = src_db.run(select_tables_sql).get_rows()
            for table_from_sql in tables_from_sql:
                if ':' in table_mess:
                    table_map = (src_schema, table_from_sql[0], dst_schema, table_from_sql[0])
                else:
                    table_map = (src_schema, table_from_sql[0], src_schema, table_from_sql[0])
                if table_map not in table_map_list and table_map[0] + '.' + table_map[1] not in exclude_tables:
                    table_map_list.append(table_map)
        else:
            table_map = (src_schema, src_table, dst_schema, dst_table)
            if table_map not in table_map_list and table_map[0] + '.' + table_map[1] not in exclude_tables:
                table_map_list.append(table_map)
        
    return table_map_list


# 主控制程序
def main():
    if run_mode == 'copy':
        # 获取连接
        src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password)
        dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password)
        
        # 解析出需要迁移的表以及映射关系
        table_map_list = get_table_map_list(src_db)
        
        # 清理表
        if if_truncate == 'true':
            for table_map in table_map_list:
                dst_schema = table_map[2]
                dst_table = table_map[3]
                dst_conn = dst_db.dbpool.connection()
                truncate_table_sql = 'truncate table ' + dst_schema + '.' + dst_table + ' cascade'
                try:
                    dst_cur = dst_conn.cursor()
                    dst_cur.execute(truncate_table_sql)
                    dst_conn.commit()
                    log.info(truncate_table_sql)
                except Exception as _:
                    log.warning(truncate_table_sql, str(_))
                finally:
                    dst_cur.close()
                
        # 获取scn，如果需要
        if if_only_scn == 'true' and len(input_global_scn) == 0:
            global_scn = src_db.run('select to_char(current_scn) from v$database').get_rows()[0][0]
        elif if_only_scn == 'true' and len(input_global_scn) > 0:
            global_scn = input_global_scn
        else:
            global_scn = None
        
        # 多线程启动表分析程序
        tp = ThreadPool(parallel_table_num, while_wait_time=0.1)
        for table_map in table_map_list:
            tp.run(run_table, (table_map, global_scn))
        tp.wait()
        
        src_db.close()
        dst_db.close()
        
        # 获取输出报告
        get_report(run_mode)
        
    elif run_mode == 'report':
        get_report(run_mode)
        
    elif run_mode == 'compare_index':
        compare_index()
        
    elif run_mode == 'compare_constraint':
        compare_constraint()
        
    elif run_mode == 'copy_from_sql':
        dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password)
        
        table_map_list = []
        for table_mess in copy_from_sql.split(','):
            dst_schema = table_mess.split(':')[1].split('.')[0]
            dst_table = table_mess.split(':')[1].split('.')[1]
            src_sql = table_mess.split(':')[0]
            table_map_list.append((None, None, dst_schema, dst_table, src_sql))
            
        # 清理表
        if if_truncate == 'true':
            for table_map in table_map_list:
                dst_schema = table_map[2]
                dst_table = table_map[3]
                dst_conn = dst_db.dbpool.connection()
                truncate_table_sql = 'truncate table ' + dst_schema + '.' + dst_table + ' cascade'
                try:
                    dst_cur = dst_conn.cursor()
                    dst_cur.execute(truncate_table_sql)
                    dst_conn.commit()
                    log.info(truncate_table_sql)
                except Exception as _:
                    log.warning(truncate_table_sql, str(_))
                finally:
                    dst_cur.close()
            
        # 多进程启动导数
        tp = ProcessPool(parallel_table_num, while_wait_time=0.1)
        for table_map in table_map_list:
            tp.run(get_data_from_sql, (table_map,))
        tp.wait()
        
        dst_db.close()


# 表分析程序
def run_table(table_map, global_scn):
    src_schema = table_map[0]
    src_table = table_map[1]
    dst_schema = table_map[2]
    dst_table = table_map[3]
    try:
        # 获取连接
        src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password)
         
        # 如果没有scn，则此处获取
        if global_scn is None:
            table_scn = src_db.run('select to_char(current_scn) from v$database').get_rows()[0][0]
        else:
            table_scn = global_scn
        
        # 获取表元数据信息
        mess_map = OracleTools.get_table_metadata(src_db, src_schema, src_table, partition=True)
        
        # 获取表数量，用于对数
        count_sql = 'select count(1) from ' + src_schema + '."' + src_table + '" as of scn ' + table_scn
        src_num = src_db.run(count_sql).get_rows()[0][0]
        report_table_id = src_schema + '.' + src_table + '-->' + dst_schema + '.' + dst_table
        report[report_table_id] = [table_scn, src_num, None]
    
        # 遍历分区子分区，多进程分配查询任务及后续任务
        tp = ProcessPool(table_parallel_num, while_wait_time=0.1)
        partition_mess = mess_map['partition']
        if partition_mess is not None and smallest_object != 'table':
            for partition in partition_mess['partitions']:
                partition_name = partition['name']
                subpartitions = partition['subpartitions']
                if len(subpartitions) > 0 and smallest_object == 'subpartition':
                    for subpartition in subpartitions:
                        subpartition_name = subpartition['name']
                        mess = src_schema + '."' + src_table + '" subpartition(' + subpartition_name + ')'
                        tp.run(get_data_from_oracle, (table_map, mess, table_scn))
                else:
                    mess = src_schema + '."' + src_table + '" partition(' + partition_name + ')'
                    tp.run(get_data_from_oracle, (table_map, mess, table_scn))
        else:
            mess = src_schema + '."' + src_table + '"'
            page_num = ceil(src_num / commit_num)
            if page_num <= table_parallel_num:
                tp.run(get_data_from_oracle, (table_map, mess, table_scn))
            else:
                page_rn = ceil(src_num / table_parallel_num)
                for page in range(1, table_parallel_num + 1):
                    tp.run(get_data_from_oracle, (table_map, mess, table_scn, page, page_rn))
        tp.wait()
        src_db.close()
    except Exception as _:
        log.error('run_table', src_table, str(_))

        
def get_data_from_oracle(table_map, mess, table_scn, page=None, page_rn=None): 
    try:
        # 获取连接
        src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password)
        
        if page is None:
            select_sql = 'select /*+ FIRST_ROWS */ *  from ' + mess + ' as of scn ' + table_scn
        else:
            cols_tuple = src_db.run('select * from ' + mess + ' as of scn ' + table_scn + ' where rownum = 1').get_cols()
            cols_str = ''
            for col in cols_tuple:
                cols_str = cols_str + col + ','
            cols_str = cols_str[:-1]
            select_sql = '''
                select ''' + cols_str + ''' from (
                    select t.*,rownum rn 
                    from ''' + mess + ''' 
                    as of scn ''' + str(table_scn) + ''' t
                    where rownum <= ''' + str(page) + ''' * ''' + str(page_rn) + '''
                ) where rn <= ''' + str(page) + ''' * ''' + str(page_rn) + '''
                and rn > ''' + str(page - 1) + ''' * ''' + str(page_rn) + '''
            '''
            
        rs = src_db.run(select_sql)
        cols = rs.get_cols_description()
        
        i = 1
        tp = ThreadPool(save_parallel_num, while_wait_time=0.1)
        while True:
            if page is None:
                my_mess = mess + '(' + str(i) + ')'
            else:
                my_mess = mess + '(' + str(page) + '-' + str(i) + ')'
            time_start = time.time()
            rows = rs.get_rows(commit_num)
            select_time = time.time() - time_start
            if len(rows) == 0:
                break
            tp.run(save_to_pg, (table_map, rows, cols, my_mess, select_time, table_scn))
            i = i + 1
            if len(rows) < commit_num:
                break
            del rows
            gc.collect()
        tp.wait()
        src_db.close()
    except Exception as _:
        log.error('get_data_from_oracle', mess, str(_))

        
def get_data_from_sql(table_map): 
    dst_schema = table_map[2]
    dst_table = table_map[3]
    src_sql = table_map[4]
    try:
        # 获取连接
        src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password)
        
        select_sql = src_sql
        
        rs = src_db.run(select_sql)
        cols = rs.get_cols_description()
        
        i = 1
        tp = ThreadPool(save_parallel_num, while_wait_time=0.1)
        while True:
            time_start = time.time()
            rows = rs.get_rows(commit_num)
            select_time = time.time() - time_start
            if len(rows) == 0:
                break
            tp.run(save_to_pg, (table_map, rows, cols, dst_schema + '.' + dst_table, select_time, ''))
            i = i + 1
            if len(rows) < commit_num:
                break
            del rows
            gc.collect()
        tp.wait()
        src_db.close()
    except Exception as _:
        log.error('get_data_from_oracle', dst_schema + '.' + dst_table, str(_))

        
def save_to_pg(table_map, rows, cols, mess, select_time, table_scn):
    dst_schema = table_map[2]
    dst_table = table_map[3]
    time_start = time.time()
    # 获取连接
    try:
        dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password, options='-c search_path=' + dst_schema + ',public')
    except Exception as _:
        log.error('save_to_pg', mess, str(_))
        return
    
    wenhaos = ''
    for _ in cols:
        wenhaos = wenhaos + '?,'
    wenhaos = wenhaos[0:-1]
    insert_sql = 'insert into ' + dst_table + ' values(' + wenhaos + ')'
    
    try:
        num = dst_db.pg_copy_from(dst_table.lower(), rows, cols)
        num = str(num) + '(copy)' 
        del rows
        gc.collect()
        dst_db.close()
    except Exception as _:
        log.warning(mess, str(_))
        try:
            num = dst_db.run(insert_sql, rows)
            if num == -1:
                raise Exception('unknown error, num = -1')
            num = str(num) + '(insert)' 
            del rows
            gc.collect()
            dst_db.close()
        except Exception as _:
            log.error(mess, str(_))
            return

    save_time = time.time() - time_start
    log.info(mess, num, str(round(select_time, 2)) + 's', str(round(save_time, 2)) + 's', 'scn=' + table_scn)


def get_report(run_mode):
    tp = ThreadPool(16)

    def count(db, sql, k):
        e1 = ''
        try:
            num = int(db.run(sql).get_rows()[0][0])
        except Exception as _:
            num = -1
            e1 = str(_)
        report[k][2] = num
        log.info('report', report[k][1] == report[k][2], k, report[k][1], report[k][2], 'scn=' + str(report[k][0]), str(e1))
    
    def count2(table_map, src_db, dst_db, global_scn):
        src_schema = table_map[0]
        src_table = table_map[1]
        dst_schema = table_map[2]
        dst_table = table_map[3]
        
        src_sql = 'select /*+ parallel(8) */ count(1) from ' + src_schema + '."' + src_table + '" as of scn ' + global_scn
        dst_sql = 'select count(1) from ' + dst_schema + '.' + dst_table
        
        e1 = ''
        e2 = ''
        try:
            src_num = int(src_db.run(src_sql).get_rows()[0][0])
        except Exception as _:
            src_num = -1
            e1 = str(_)
        try:
            dst_num = int(dst_db.run(dst_sql).get_rows()[0][0])
        except Exception as _:
            dst_num = -1
            e2 = str(_)
            
        report_table_id = src_schema + '.' + src_table + '-->' + dst_schema + '.' + dst_table
        report[report_table_id] = [global_scn, src_num, dst_num]
        log.info('report', report[report_table_id][1] == report[report_table_id][2], report_table_id, report[report_table_id][1], report[report_table_id][2], 'scn=' + global_scn, str(e1), str(e2))
    
    if run_mode == 'copy':
        log.info('Generating report')
        try:
            dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password, poolsize=8)
        except Exception as _:
            log.error('report', str(_))
        error_table = ''
        
        for k in report:
            src_schema = k.split('-->')[1].split('.')[0]
            src_table = k.split('-->')[1].split('.')[1]
            dst_sql = 'select count(1) from ' + src_schema + '.' + src_table
            tp.run(count, (dst_db, dst_sql, k))
        tp.wait()
        
        for k in report:
            if report[k][1] != report[k][2]:
                error_table = error_table + k.replace('-->', ':') + ','
                
        log.info('error_table', error_table)
        dst_db.close()
            
    elif run_mode == 'report':
        try:
            src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password, poolsize=8)
            dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password, poolsize=8)
        except Exception as _:
            log.error('report', str(_))
            
        # 如果没有scn，则此处获取
        if len(input_global_scn) == 0:
            global_scn = src_db.run('select to_char(current_scn) from v$database').get_rows()[0][0]
        else:
            global_scn = input_global_scn
        
        # 解析出需要迁移的表以及映射关系
        table_map_list = get_table_map_list(src_db)
        
        error_table = ''
        for table_map in table_map_list:
            tp.run(count2, (table_map, src_db, dst_db, global_scn))
        tp.wait()
            
        for k in report:
            if report[k][1] != report[k][2]:
                error_table = error_table + k.replace('-->', ':') + ','
                
        log.info('error_table', error_table)
        src_db.close()
        dst_db.close()

        
def compare_index():
    try:
        src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password, poolsize=8)
        dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password, poolsize=8)
    except Exception as _:
        log.error('compare_index', str(_))
    
    # 解析出需要迁移的表以及映射关系
    table_map_list = get_table_map_list(src_db)
    
    for table_map in table_map_list:
        src_schema = table_map[0]
        src_table = table_map[1]
        dst_schema = table_map[2]
        dst_table = table_map[3]
        e1 = ''
        e2 = ''
        src_sql = "select count(distinct index_name) from dba_indexes where index_type not in('LOB') and table_owner = '" + src_schema + "' and table_name = '" + src_table + "'"
        dst_sql = "select count(distinct indexname) from pg_indexes where schemaname = '" + dst_schema + "' and tablename = '" + dst_table + "'"
        try:
            src_num = src_db.run(src_sql).get_rows()[0][0]
        except Exception as _: 
            src_num = -1
            e1 = str(_)
        try:
            dst_num = dst_db.run(dst_sql).get_rows()[0][0]
        except Exception as _:
            dst_num = -2
            e2 = str(_)
        log.info('compare_index', src_num == dst_num, src_table, 'oracle=' + str(src_num), 'pgsql=' + str(dst_num), str(e1), str(e2))

    src_db.close()
    dst_db.close()

    
def compare_constraint():
    try:
        src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password, poolsize=8)
        dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password, poolsize=8)
    except Exception as _:
        log.error('compare_index', str(_))
    
    # 解析出需要迁移的表以及映射关系
    table_map_list = get_table_map_list(src_db)
    
    for table_map in table_map_list:
        src_schema = table_map[0]
        src_table = table_map[1]
        dst_schema = table_map[2]
        dst_table = table_map[3]
        e1 = ''
        e2 = ''
        src_sql = "select count(distinct index_name) from dba_constraints where owner = '" + src_schema + "' and table_name = '" + src_table + "'"
        dst_sql = "select count(distinct constraint_name) from information_schema.constraint_table_usage where table_catalog = '" + dst_database + "' and table_schema = '" + dst_schema + "' and table_name = '" + dst_table + "'"
        try:
            src_num = src_db.run(src_sql).get_rows()[0][0]
        except Exception as _: 
            src_num = -1
            e1 = str(_)
        try:
            dst_num = dst_db.run(dst_sql).get_rows()[0][0]
        except Exception as _:
            dst_num = -2
            e2 = str(_)
        log.info('compare_constraint', src_num == dst_num, src_table, 'oracle=' + str(src_num), 'pgsql=' + str(dst_num), str(e1), str(e2))

    src_db.close()
    dst_db.close()

            
if __name__ == '__main__': 
    main()
