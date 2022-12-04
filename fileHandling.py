from csv import writer

with open(r'C:\Users\Lenovo\PycharmProjects\pythonProject\Lighting_Art.csv', 'w', encoding='utf8', newline='') as f:
    write_data = writer(f)
    header = ['Sr No.','Image links']
    write_data.writerow(header)

