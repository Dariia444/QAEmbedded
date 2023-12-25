import subprocess
import re

# Ip-адреса iperf сервера.
server_ip = '192.168.0.107'

def client(server_ip):
    try:
        process = subprocess.Popen(['iperf', '-c', server_ip, '-i', '1'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, error = process.communicate()

        if process.returncode == 0:
            return output, None
        else:
            return None, f'Error: {error}'

    except Exception as e:
        return None, f'Exception: {str(e)}'





def parser(output):
    intervals = []

    if not output:
        print("Error: No output to parse.")
        return intervals

    try:
        # use regex to find info in output of iperf
        interval_pattern_for_last = re.compile(r'(\d+\.\d+-\d+\.\d+) sec\s+(\d+\.\d+)\s+(\S+)\s+(\d+\.\d+)\s+(\S+)')
        interval_pattern_for_others = re.compile(r'(\d+\.\d+-\d+\.\d+) sec\s+(\d+)\s+(\S+)\s+(\d+\.\d+)\s+(\S+)')

        # find matches for all but last record in output
        matchesOthers = interval_pattern_for_others.findall(output)
        matchesLast = interval_pattern_for_last.findall(output)

        for match in matchesOthers:
            interval_dict = {
                'Interval': match[0],
                'Transfer': float(match[1]),
                'Transfer_Unit': match[2],
                'Bandwidth': float(match[3]),
                'Bandwidth_Unit': match[4]
            }
            intervals.append(interval_dict)
        for match in matchesLast:
            interval_dict = {
                'Interval': match[0],
                'Transfer': float(match[1]),
                'Transfer_Unit': match[2],
                'Bandwidth': float(match[3]),
                'Bandwidth_Unit': match[4]
            }
            intervals.append(interval_dict)

    except Exception as e:
        print(f"Error during parsing: {str(e)}")

    return intervals


output, error = client(server_ip)

if output is not None:
    print('Output:\n', output)
else:
    print('Error:\n', error)

print('\n\n\n')

transfetConditionValue = 200
bandwidthConditionValue = 1.6

if error:
    print(error)
else:
    print('Output intervals Transfer > {transfetConditionValue} and Bandwidth > {bandwidthConditionValue}:\n')
    result_list = parser(output)
    for value in result_list:
        if value['Transfer'] > transfetConditionValue and value['Bandwidth'] > bandwidthConditionValue:
            print(value)
