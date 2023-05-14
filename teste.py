
import random;

def enemy_car_position(start_road, size_road, height):
    seed = random.randint(0, 3);
    return (start_road + (2*seed+1)*size_road/8, height*0.2)

for i in range(10):
    print(enemy_car_position(200, 400, 400));