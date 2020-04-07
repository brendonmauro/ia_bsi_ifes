def get_symbol(point, parent):
	dic_symbol = { (0,1) : '>' , (1,0) : 'v', (0,-1): '<', (-1,0):'^'}
	x = point['x'] - parent['x']
	y = point['y'] - parent['y']
	return dic_symbol[(x,y)]

# Funções de coordenadas
def cr_point(x,y, symbol = ''):
	return {'x': x, 'y': y, 'symbol': symbol}

def equal_points(p1, p2):
	return p1['x'] == p2['x'] and p1['y'] == p2['y']

def point_as_tuple(point):
	return (point['x'],point['y'])

def verify_point(point, closed_list, map_problem):
	x = point['x']
	y = point['y']
	sizeA = len(map_problem)
	sizeB = len(map_problem[0])
	
	for p_close in closed_list:
		if equal_points(point,p_close):
			return False
	
	return x < sizeA and x > -1 and y < sizeB and y > -1 and map_problem[x][y] == 0

def heuristic_func(point,target):
	return abs(target['x']-point['x']) + abs(target['y']-point['y'])
	
def get_adj_points():
	return [cr_point(0,1),cr_point(1,0), cr_point(0,-1), cr_point(-1,0)]

def get_valid_adj_points(point, closed_list, map_problem):
	adj_points = get_adj_points()
	valid_adj_points = []
	for adj_point in adj_points:
		new_point = cr_point(point['x'] + adj_point['x'],  point['y'] + adj_point['y'], adj_point['symbol'])
		if verify_point(new_point, closed_list, map_problem):
			valid_adj_points.append(new_point)
	return valid_adj_points
	
########################################################################

#funções de leitura de arquivo
def read_line(file_map):
	return list(map(lambda x: int(x),file_map.readline().strip().split()))

def create_map(path):
    matrix = []
    file_map = open(path, "r")
    line = read_line(file_map)

    while (line != []):
        matrix.append(line)
        line = read_line(file_map)

    return matrix
########################################################################

# funções de saída
def print_line(line):
	[print(elem, end=" ") for elem in line]
	print()
	
def print_map(map_problem):
	[print_line(line) for line in map_problem]	
	
def get_main_path(point, dic_paths):
	new_list = []
	point_tuple = point_as_tuple(point)
	
	if point_tuple in dic_paths:
		parent = dic_paths[point_tuple]['parent']
		if point['symbol'] != 'X':
			point['symbol'] = get_symbol(point,parent)
		new_list.append(parent)
		new_list += get_main_path(parent, dic_paths)
		
	return new_list

def draw_solution(target, dic_paths, map_problem):	
	new_map = list(map_problem)
	
	points = get_main_path(target,dic_paths)
	points.append(target)
	for point in points:
		x = point['x']
		y = point['y']
		new_map[x][y] = point['symbol']
	
	print_map(new_map)

########################################################################	
	
	
def search(ini_point,target, map_problem):
	ini_point['cost'] = 0
	open_list = [ini_point]
	closed_list = []
	
	if equal_points(ini_point,target):
		print("Você já está em seu alvo")
	
	dic_paths = {}
	
	while open_list != []:
		current_point = open_list.pop(0)
		
		adj_points = get_valid_adj_points(current_point, closed_list, map_problem)
		
		for adj_point in adj_points:
			adj_point['cost'] = current_point['cost'] + 1
			dic_paths[point_as_tuple(adj_point)] = { 'parent': current_point }
		
		if equal_points(current_point,target):
			draw_solution(target, dic_paths, map_problem)
			print()
			print('O custo total percorrido foi: ',current_point['cost'])
		else:
			closed_list.append(current_point)
		
		for adj_point in adj_points:
			if verify_point(adj_point,open_list, map_problem):
				open_list.append(adj_point)
		open_list.sort(key=lambda p: p['cost'] + heuristic_func(p,target))
	

########################################################################

#função de entrada
def input_list_integer(msg):
	return list(map(lambda x: int(x), input(msg).split(' ')))
	
def main():
	file_arg = input("Informe o nome do arquivo [ex:mapa.txt]:\n")
	map_problem = create_map(file_arg)
	
	print("O mapa de entrada foi:")
	print_map(map_problem)
	print()
	
	input_ini_point = input_list_integer("Informe a posicao inicial [ex: 0 0]:\n")
	ini_point = cr_point(input_ini_point[0],input_ini_point[1], '*')
	
	input_target = input_list_integer("Informe a posicao final [ex: 9 8]:\n")
	target = cr_point(input_target[0],input_target[1], 'X')
	
	print()
	print("Solução proposta foi:")
	search(ini_point,target, map_problem)
	return 0

if __name__ == "__main__":
    main()

    
