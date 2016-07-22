import os

import pandas as pd

def samtools_flagstat_to_dict(uuid, metric_path, logger):
    data_dict = dict()
    values_to_store = ['in total', 'mapped', 'paired in sequencing', 'read1', 'read2']
    with open(flagstat_path, 'r') as f_open:
        for line in f_open:
            line = line.strip('\n')
            for value_to_store in values_to_store:
                if value_to_store in line:
                    if value_to_store == 'mapped':
                        if 'mate' in line:  # avoid 'with mate mapped to a different chr'/'with itself and mate mapped'
                            continue
                    line_split = line.split(' ')
                    first_val = line_split[0]
                    second_val = line_split[2]
                    total_val = str(int(first_val) + int(second_val))
                    data_dict[value_to_store] = total_val
    return data_dict

def run(uuid, metric_path, bam, input_state, engine, logger):
    data_dict = samtools_flagstat_to_dict(uuid, bam_path, flagstat_path, logger)
    data_dict['uuid'] = [uuid]
    data_dict['bam'] = bam
    data_dict['input_state'] = input_state
    df = pd.DataFrame(data_dict)
    table_name = 'samtools_flagstat'
    df.to_sql(table_name, engine, if_exists='append')
    return
