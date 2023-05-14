import pygame
from pygame.locals import *
import random

#Desenha uma linha tracejada com "frequency" traços
def drawn_traced_line(screen: pygame.display, 
                      dimensions: set, 
                      frequency=10, 
                      color="#ffffff"):
    
    x0 = dimensions[0];
    y0 = dimensions[1];
    width = dimensions[2]; 
    height = dimensions[3];

    interval = height/frequency;
    counter = 0;
    base = y0;

    while((counter)*interval < height):

        if (counter%2 == 0):

            pygame.draw.rect(
                surface = screen,
                color =color,
                rect = (x0, counter*interval + base, width, interval),
            )

        counter += 1;

def enemy_car_position(start_road, size_road):
    seed = random.randint(0, 3);
    return (start_road + (2*seed+1)*size_road/8, 0);

def constroi_background_dinamico(
                   screen, 
                   width, 
                   height,
                   road_w, 
                   roadmark_w,
                   background_game,
                   road_final,
                   start_line = 0,
                   ):

    screen.blit(background_game, (0,start_line));
    screen.blit(road_final, (width/2-road_w/2, start_line));

    #Desenhando as linhas tracejadas da estrada
    c = 1;
    while(c < 4):
        drawn_traced_line(screen, (c*int(road_w/4)+x0_road, start_line, roadmark_w, height), frequency=20);
        c += 1;

def constroi_background_estatico(screen, height, road_w, roadmark_w):

    #Desenhando as bordas da estrada
    pygame.draw.rect(
        surface=screen,
        color="#ffffff",
        rect=(2*roadmark_w + x0_road, 0, roadmark_w, height)
    )
    pygame.draw.rect(
        surface=screen,
        color="#ffffff",
        rect=(x0_road + road_w - 3*roadmark_w, 0, roadmark_w, height)
    )


def calculate_speed(height, screen_crossed):
    if screen_crossed < 60:
        return int(height/60); #Normal Speed
    if (screen_crossed < 100):
        return int(height/54); #Decent Speed
    if (screen_crossed < 160):
        return int(height/50); #Nice Speed
    if (screen_crossed < 300):
        return int(height/46); #Kinda Fast
    if (screen_crossed < 500):
        return int(height/42); #Bro u serious?

#Inicia a aplicação
pygame.init()

#Variáveis de Contexto
height = 900;
width = int(height*0.75);
size = (width, height);
road_w = int(width/1.25);
roadmark_w = int(width/80);
game_over_screen_w = int(width/1.5);
game_over_screen_h = int(height/3);
title_size = int(height/15);
x0_road = width/2 - road_w/2;

clock = pygame.time.Clock();
FPS = 60;
running = True #Usarei essa variável para controlar a execução do app

#Importando e ajustando as imagens
background_original = pygame.image.load("background.jpg");
background = pygame.transform.scale(background_original, (width, height));

road_original = pygame.image.load("road.jpg");
road_final = pygame.transform.scale(road_original, (road_w, height));

#Montando a tela
screen = pygame.display.set_mode(size); #define o tamanho da janela com base no set "size"
pygame.display.set_caption("Vrum vrum carros");

#Atualiza o display
pygame.display.update();

#Importando a arte do carro e localizando-a na tela
car = pygame.image.load("car.png");
#Mantendo a figura em escala com a imagem
car = pygame.transform.scale(car, (int(width/4.8), int(height/6.4)));
car_loc = car.get_rect();   #Método para gerar um objeto que será usado para manipular 
                            #a posição da imagem na tela        

car_loc.center = (width/2 + road_w/8, height*0.9) #Posiciona o centro da imagem nas coordenadas especificadas
print("POSICAO CARRO: " + str(car_loc.center[0]));

enemy_car = pygame.image.load("otherCar.png");
enemy_car = pygame.transform.scale(enemy_car, (int(width/4.8), int(height/6.4)));
enemy_car_loc = car.get_rect(); 
enemy_car_loc.center = enemy_car_position(x0_road, road_w);

enemy_car2 = pygame.image.load("otherCar.png");
enemy_car2 = pygame.transform.scale(enemy_car2, (int(width/4.8), int(height/6.4)));
enemy_car2_loc = car.get_rect(); 
enemy_car2_loc.center = enemy_car_position(x0_road, road_w);

enemy_car3 = pygame.image.load("otherCar.png");
enemy_car3 = pygame.transform.scale(enemy_car3, (int(width/4.8), int(height/6.4)));
enemy_car3_loc = car.get_rect(); 
enemy_car3_loc.center = enemy_car_position(x0_road, road_w);

#Debugger
print("Inicio/Fim da Pista: " + str(x0_road) + " " + str(x0_road+road_w));
print("Inicio/Fim da tela " + str(width) + "x" + str(height));

list_enemy_cars = [(enemy_car, enemy_car_loc), (enemy_car2, enemy_car2_loc), (enemy_car3, enemy_car3_loc)];

speed = int(height/60);
counter = 0;
screen_crossed = 0;
flag_crossed = False;
start_line = 0;

while running:
    clock.tick(FPS);

    speed = calculate_speed(height, screen_crossed);

    start_line += speed;
    if start_line > height:
        start_line = 0;

    for each in list_enemy_cars:
        height_modifier = random.randint(1,5);
        each[1][1] += speed;
        if each[1][1] > height:
            each[1].center = (enemy_car_position(x0_road, road_w)[0], -125*height_modifier) #CUIDADO COM car_loc e car_loc.center !! 
            screen_crossed += 1;
            print("Carros que passaram : " + str(screen_crossed));

    #end game condition
    for each in list_enemy_cars:
        if car_loc[0] == each[1][0] and each[1][1] > car_loc[1] - 85:
            print("GAME OVER!!");
            print("PONTUAÇÃO : " + str(screen_crossed*100));

            game_over_screen = pygame.draw.rect(
                surface=screen,
                color="#00BFFF",
                rect = (width/2 - game_over_screen_w/2, height/2 - game_over_screen_h/2, game_over_screen_w , game_over_screen_h),
            )
            
            padding_up = height//120 + title_size;
            pygame.font.init();
            #fonte = pygame.font.Font("Rubik", 40);
            fonte = pygame.font.SysFont(pygame.font.get_default_font(), title_size);
            sub_title = pygame.font.SysFont(pygame.font.get_default_font(), int(title_size/1.25));

            texto_game_over = fonte.render("Game Over!", True, "#ffffff");
            rect_texto = texto_game_over.get_rect();
            x_text = width/2;
            y_text = height/2 - game_over_screen_h/2 + padding_up;
            rect_texto.center = (x_text, y_text);

            pontuacao1 = sub_title.render("Score : " + str(screen_crossed*100), True, "#ffffff");
            pontuacao1_rect = pontuacao1.get_rect();
            pontuacao1_rect.center = (x_text, y_text + padding_up);

            screen.blit(texto_game_over, rect_texto);
            screen.blit(pontuacao1, pontuacao1_rect);
            pygame.display.update();

            while(running):
                for event in pygame.event.get():
                    if event.type == KEYDOWN or event.type == QUIT:
                        running = False;

    if running == False:
        break;

    for event in pygame.event.get(): #Varrendo todo os eventos que estão presentes no projeto

        if event.type == QUIT:  #Se o usuário clica para fechar, quebra o ciclo e segue
                                #para finalizar a aplicação
            running = False;
    
        if event.type == KEYDOWN: #detecta que uma tecla foi pressionada
            move_x = int(road_w/4);
            if event.key in [K_a, K_LEFT]: #pressionou a tecla A ou seta para esquerda 
                if car_loc.center[0] - move_x > x0_road:
                    car_loc = car_loc.move([-move_x, 0]);
            if event.key in [K_d, K_RIGHT]:
                if car_loc.center[0] + move_x < x0_road + road_w:
                    car_loc = car_loc.move([move_x, 0]);        
    
    #Trecho responsável por mover a pista
    constroi_background_dinamico(screen, width, height, road_w, roadmark_w, background, road_final, start_line - height);
    constroi_background_dinamico(screen, width, height, road_w, roadmark_w, background, road_final, start_line);

    #Trecho responsável por construir a parte que não muda (linhas laterais)
    constroi_background_estatico(screen, height, road_w, roadmark_w);

    screen.blit(car, car_loc); #Operação que prepara a inicialização de um novo elemento gráfico na tela
    
    for each in list_enemy_cars:
        screen.blit(each[0], each[1]); #Criando cada carro inimigo
    
    pygame.display.update();

    #counter += 1;
    #if screen_crossed%10 == 0 and screen_crossed != 0:
    #    speed += 1;

print("Quantidade de ciclos: " + str(counter));
#Fecha a aplicação
pygame.quit()