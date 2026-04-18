```python
import os
import pandas as pd
import re
import glob

def parse_moveit_log_file(file_path):
    """
    Parse a single MoveIt! log file and extract planner run data
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as file:
            content = file.read()
    
    planners_data = []
    current_planner = None
    current_data = []
    in_data_section = False
    
    lines = content.split('\n')
    
    for line in lines:
        line = line.strip()
        
        # Check if this is a planner name line
        planner_match = re.match(r'^(RewardRRT|SBLkConfigDefault|RGRRT|ESTkConfigDefault|BKPIECEkConfigDefault|BKPIECEGood|KPIECEkConfigDefault|RRTkConfigDefault|RRTConnect[_a-zA-Z0-9]*|RRTstarkConfigDefault|TRRTkConfigDefault|PRMkConfigDefault|PRMstarkConfigDefault|InformedRRTstar|SORRTstar|AITstar|ABITstar|BITstar|LazyPRMstar|EITstar)$', line)
        if planner_match:
            if current_planner and current_data:
                planners_data.append({'name': current_planner, 'data': current_data})
            current_planner = planner_match.group(1)
            current_data = []
            in_data_section = False
            continue
        
        # Check if entering data section (after 100 runs)
        if '100 runs' in line.lower():
            in_data_section = True
            continue
        
        # If this is a data line with semicolon
        if in_data_section and ';' in line and line and not line == '.':
            data_line = line.rstrip(';').strip()
            values = [v.strip() for v in data_line.split(';')]
            
            if len(values) == 20:
                current_data.append(values)
    
    if current_planner and current_data:
        planners_data.append({'name': current_planner, 'data': current_data})
    
    return planners_data


def create_excel_format_data(planners_data, filename):
    """
    Create Excel-formatted data for a single file
    """
    excel_data = []
    
    for planner in planners_data:
        planner_name = planner['name']
        data = planner['data']
        
        columns = [
            'time', 'success', 'correct', 'length', 'machine_hostname', 
            'machine_process_id', 'machine_thread_id', 'query_finish_time', 
            'query_index', 'query_start_time', 'query_timeout_trial', 
            'query_trial', 'request_group_name', 'request_num_planning_attempts',
            'request_planner_id', 'request_planner_type', 'robowflex_planner_name',
            'robowflex_robot_name', 'smoothness', 'waypoints'
        ]
        
        df = pd.DataFrame(data, columns=columns)
        
        df['time'] = pd.to_numeric(df['time'], errors='coerce')
        df['success'] = df['success'].map({'1': 1, '0': 0, 'True': 1, 'False': 0, 'true': 1, 'false': 0})
        df['length'] = pd.to_numeric(df['length'], errors='coerce')
        df['smoothness'] = pd.to_numeric(df['smoothness'], errors='coerce')
        df['waypoints'] = pd.to_numeric(df['waypoints'], errors='coerce')
        
        success_rate = round(df['success'].mean() * 100, 2)
        successful_runs = len(df[df['success'] == 1])
        total_runs = len(df)
        
        success_df = df[df['success'] == 1]
        
        if len(success_df) > 0:
            excel_data.append({
                'Source File': filename,
                'Planner': planner_name,
                'Success Rate (%)': success_rate,
                'Total Runs': total_runs,
                'Successful Runs': successful_runs,
                'Metric': 'Time (s)',
                'Mean': round(success_df['time'].mean(), 6),
                'Min': round(success_df['time'].min(), 6),
                'Max': round(success_df['time'].max(), 6),
                'Median': round(success_df['time'].median(), 6)
            })
            
            excel_data.append({
                'Source File': filename,
                'Planner': planner_name,
                'Success Rate (%)': success_rate,
                'Total Runs': total_runs,
                'Successful Runs': successful_runs,
                'Metric': 'Path Length',
                'Mean': round(success_df['length'].mean(), 6),
                'Min': round(success_df['length'].min(), 6),
                'Max': round(success_df['length'].max(), 6),
                'Median': round(success_df['length'].median(), 6)
            })
            
            excel_data.append({
                'Source File': filename,
                'Planner': planner_name,
                'Success Rate (%)': success_rate,
                'Total Runs': total_runs,
                'Successful Runs': successful_runs,
                'Metric': 'Smoothness',
                'Mean': round(success_df['smoothness'].mean(), 6),
                'Min': round(success_df['smoothness'].min(), 6),
                'Max': round(success_df['smoothness'].max(), 6),
                'Median': round(success_df['smoothness'].median(), 6)
            })
            
            excel_data.append({
                'Source File': filename,
                'Planner': planner_name,
                'Success Rate (%)': success_rate,
                'Total Runs': total_runs,
                'Successful Runs': successful_runs,
                'Metric': 'Waypoints',
                'Mean': round(success_df['waypoints'].mean(), 2),
                'Min': round(success_df['waypoints'].min(), 2),
                'Max': round(success_df['waypoints'].max(), 2),
                'Median': round(success_df['waypoints'].median(), 2)
            })
        else:
            excel_data.extend([
                {
                    'Source File': filename,
                    'Planner': planner_name,
                    'Success Rate (%)': 0.0,
                    'Total Runs': total_runs,
                    'Successful Runs': 0,
                    'Metric': 'Time (s)',
                    'Mean': 0.0,
                    'Min': 0.0,
                    'Max': 0.0,
                    'Median': 0.0
                },
                {
                    'Source File': filename,
                    'Planner': planner_name,
                    'Success Rate (%)': 0.0,
                    'Total Runs': total_runs,
                    'Successful Runs': 0,
                    'Metric': 'Path Length',
                    'Mean': 0.0,
                    'Min': 0.0,
                    'Max': 0.0,
                    'Median': 0.0
                },
                {
                    'Source File': filename,
                    'Planner': planner_name,
                    'Success Rate (%)': 0.0,
                    'Total Runs': total_runs,
                    'Successful Runs': 0,
                    'Metric': 'Smoothness',
                    'Mean': 0.0,
                    'Min': 0.0,
                    'Max': 0.0,
                    'Median': 0.0
                },
                {
                    'Source File': filename,
                    'Planner': planner_name,
                    'Success Rate (%)': 0.0,
                    'Total Runs': total_runs,
                    'Successful Runs': 0,
                    'Metric': 'Waypoints',
                    'Mean': 0.0,
                    'Min': 0.0,
                    'Max': 0.0,
                    'Median': 0.0
                }
            ])
    
    return excel_data


def add_empty_row(excel_data):
    """
    Add an empty row separator
    """
    excel_data.append({
        'Source File': '',
        'Planner': '',
        'Success Rate (%)': '',
        'Total Runs': '',
        'Successful Runs': '',
        'Metric': '',
        'Mean': '',
        'Min': '',
        'Max': '',
        'Median': ''
    })
    return excel_data


def process_log_files(folder_path):
    """
    Process all .log files in a folder
    """
    log_files = glob.glob(os.path.join(folder_path, "*.log"))
    
    if not log_files:
        print(f"No .log files found in folder: {folder_path}")
        return None
    
    print(f"Found {len(log_files)} .log files:")
    for file in log_files:
        print(f"  - {os.path.basename(file)}")
    
    all_excel_data = []
    
    for i, log_file in enumerate(log_files):
        filename = os.path.basename(log_file)
        print(f"\nProcessing file: {filename}")
        
        try:
            planners_data = parse_moveit_log_file(log_file)
            
            if planners_data:
                print(f"  Found {len(planners_data)} planners")
                
                file_excel_data = create_excel_format_data(planners_data, filename)
                
                if i < len(log_files) - 1:
                    file_excel_data = add_empty_row(file_excel_data)
                
                all_excel_data.extend(file_excel_data)
                
                for planner in planners_data:
                    print(f"    - {planner['name']}: {len(planner['data'])} rows")
            else:
                print(f"  Warning: No valid data found in {filename}")
                
        except Exception as e:
            print(f"  Error processing {filename}: {str(e)}")
    
    return all_excel_data


def main():
    robot_name = "baxter"
    folder_path = f"motion_bench_maker/benchmark/results_{robot_name}"
    output_excel_path = f"{folder_path}/000{robot_name}_planners_summary.xlsx"

    print("Starting log file processing...")
    
    all_data = process_log_files(folder_path)
    
    if not all_data:
        print("No valid data found. Exiting.")
        return
    
    result_df = pd.DataFrame(all_data)
    
    column_order = ['Source File', 'Planner', 'Success Rate (%)', 'Total Runs', 'Successful Runs', 
                   'Metric', 'Mean', 'Min', 'Max', 'Median']
    result_df = result_df[column_order]
    
    with pd.ExcelWriter(output_excel_path, engine='openpyxl') as writer:
        result_df.to_excel(writer, sheet_name='All_Data', index=False)
    
    print("\nProcessing complete!")
    print(f"Excel file saved to: {output_excel_path}")


if __name__ == "__main__":
    main()
```

