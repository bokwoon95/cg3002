moves = ['doublepump', 'cowboy', 'crab', 'chicken', 'raffles', 'jamesbond',        'runningman', 'hunchback', 'mermaid', 'snake', 'idle', 'logout']
moves_upper = ['Doublepump', 'Cowboy', 'Crab', 'Chicken', 'Raffles','Jamesbond', 'Runningman', 'Hunchback', 'Mermaid', 'Snake', 'Idle', 'Final']

columns_raw = ['move', 'acc1_x', 'acc1_y', 'acc1_z', 'gyro1_x', 'gyro1_y', 'gyro1_z',
	'acc2_x', 'acc2_y', 'acc2_z', 'gyro2_x', 'gyro2_y', 'gyro2_z',
	'acc3_x', 'acc3_y', 'acc3_z', 'gyro3_x', 'gyro3_y', 'gyro3_z', 'checksum']

feature_prefix = ["mean_", "var_", "iqr_", "psd_"]

x_columns = ['acc1_x', 'acc1_y', 'acc1_z', 'gyro1_x', 'gyro1_y', 'gyro1_z',
	'acc2_x', 'acc2_y', 'acc2_z', 'gyro2_x', 'gyro2_y', 'gyro2_z',
	'acc3_x', 'acc3_y', 'acc3_z', 'gyro3_x', 'gyro3_y', 'gyro3_z']

headers = []
for prefix in feature_prefix:
	for x in x_columns:
		headers.append(prefix + x)
