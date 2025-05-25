# 写入excel数据
def write_excel(workbook, env, row):
    column_names = ['row', 'x', 'y', 'v', 'theta', 'is_stop']
    for vehicle in env.road.vehicles:
        sheet_name = str(vehicle.id)
        # 为每一辆车创建一个sheet，如果存在则直接在后面添加
        if sheet_name not in workbook.sheetnames:
            worksheet = workbook.create_sheet(sheet_name)
            worksheet.append(column_names)
        else:
            worksheet = workbook[sheet_name]
        
        is_stop = vehicle.speed == 0
        row_data = [row, round(vehicle.position[0], 2), round(vehicle.position[1], 2), round(vehicle.speed, 2), round(vehicle.heading, 2), is_stop]
        worksheet.append(row_data)