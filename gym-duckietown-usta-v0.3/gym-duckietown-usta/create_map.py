

map_name = 'city_5x5_s1'
NUM_AV = 5
NUM_ST = 5
SPACE = 1

TILE_SIZE = 0.585
SIGN_SIZE = 0.1

map_path = f'./gym_duckietown/maps/{map_name}.yaml'

objects = ''

with open(map_path, "w") as f:
    f.write(f'num_av: {NUM_AV}\n')
    f.write(f'num_st: {NUM_ST}\n')
    f.write(f'space: {SPACE}\n\n')

    f.write('tiles:\n')
    num_grasses = 2 + (1+SPACE)*NUM_AV - SPACE
    f.write('- [grass' + (num_grasses-1)*', grass' + ']\n')
    for st in range(NUM_ST):

        f.write('- [grass')
        for av in range(NUM_AV):

            if av != (NUM_AV-1):
                objects += f'- kind: sign_st{st+1}_av{av+1}_E\n'
                objects += f'  pos: [{2.0+(SPACE/2.0)+(1+SPACE)*av},{2.0+(1+SPACE)*st}]\n'
                objects += f'  rotate: 180\n'
                objects += f'  height: {SIGN_SIZE}\n'

                objects += f'- kind: sign_st{st+1}_av{av+1}_W\n'
                objects += f'  pos: [{2.0+(SPACE/2.0)+(1+SPACE)*av},{1.0+(1+SPACE)*st}]\n'
                objects += f'  rotate: 0\n'
                objects += f'  height: {SIGN_SIZE}\n'

            if st != (NUM_ST-1):
                objects += f'- kind: sign_av{av+1}_st{st+1}_N\n'
                objects += f'  pos: [{2.0+(1+SPACE)*av},{2.0+(SPACE/2.0)+(1+SPACE)*st}]\n'
                objects += f'  rotate: 270\n'
                objects += f'  height: {SIGN_SIZE}\n'

                objects += f'- kind: sign_av{av+1}_st{st+1}_S\n'
                objects += f'  pos: [{1.0+(1+SPACE)*av},{2.0+(SPACE/2.0)+(1+SPACE)*st}]\n'
                objects += f'  rotate: 90\n'
                objects += f'  height: {SIGN_SIZE}\n'

            if av==0:
                if st==0:
                    f.write(', curve_left/W' + SPACE*', straight/W')
                elif st==(NUM_ST-1):
                    f.write(', curve_left/S' + SPACE*', straight/W')
                else:
                    f.write(', 3way_left/S' + SPACE*', straight/W')
            elif av==(NUM_AV-1):
                if st==0:
                    f.write(', curve_left/N')
                elif st==(NUM_ST-1):
                    f.write(', curve_left/E')
                else:
                    f.write(', 3way_left/N ')
            else:
                if st==0:
                    f.write(', 3way_left/W' + SPACE*', straight/W')
                elif st==(NUM_ST-1):
                    f.write(', 3way_left/E' + SPACE*', straight/W')
                else:
                    f.write(', 4way       ' + SPACE*', straight/W')
        f.write(', grass]\n')

        for space in range(SPACE):
            if st < (NUM_ST-1):
                f.write('- [grass')
                for av in range(NUM_AV):
                    if av==(NUM_AV-1):
                        f.write(', straight/N')
                    else:
                        f.write(', straight/S' + SPACE*', grass')
                f.write(', grass]\n')

    f.write('- [grass' + (num_grasses-1)*', grass' + ']\n')


    
    f.write(f'\nobjects:\n')
    f.write(objects)


    f.write(f'\ntile_size: {TILE_SIZE}\n')
