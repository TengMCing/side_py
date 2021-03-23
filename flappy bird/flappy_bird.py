import pygame
import color
import random


class bird_cls():

    def __init__(self, file_name):

        self.img = pygame.image.load(file_name)
        self.img = pygame.transform.scale(self.img, (128, 65))
        self.pos = [0, 0]


class bg_cls():

    def __init__(self, file_name):

        self.img = pygame.image.load(file_name)
        self.pos = [0, 0]


class game_over_cls():

    def __init__(self, file_name):

        self.img = pygame.image.load(file_name)
        self.img = pygame.transform.scale(self.img, (250, 125))
        self.pos = [100, 150]
        self.show = False


class module_pipe_cls():

    def __init__(self, file_name):

        self.img = pygame.image.load(file_name)
        self.img = pygame.transform.scale(self.img, (25, 25))


class single_pipe_cls():

    body_file_name = "pipe_body.png"
    head_file_name = "pipe_head.png"

    def __init__(self, pos_x):

        self.t_num = 16
        self.u_num = random.randrange(1, self.t_num + 1)
        self.d_num = self.t_num - self.u_num

        self.body = module_pipe_cls(self.body_file_name)
        self.head = module_pipe_cls(self.head_file_name)
        self.rev_body = module_pipe_cls(self.body_file_name)
        self.rev_head = module_pipe_cls(self.head_file_name)
        self.rev_body.img = pygame.transform.rotate(self.rev_body.img, 180)
        self.rev_head.img = pygame.transform.rotate(self.rev_head.img, 180)
        self.pos = [0, 0]
        self.pos[0] = pos_x
        self.free_space = 100
        self.set_free_space(100)

    def set_free_space(self, space):
        self.free_space = space
        self.t_num = (500 - space) // 25
        self.u_num = random.randrange(1, self.t_num)
        self.d_num = self.t_num - self.u_num

    def module_pos(self):
        pos_x = self.pos[0]
        pos_y = 0
        pipe_list = []
        for i in range(self.u_num - 1):
            pipe_list.append([self.rev_body.img, [pos_x, pos_y], 0])
            pos_y += 25
        pipe_list.append([self.rev_head.img, [pos_x, pos_y], 0])

        pos_y = 475
        for i in range(self.d_num - 1):
            pipe_list.append([self.body.img, [pos_x, pos_y], 1])
            pos_y -= 25
        pipe_list.append([self.head.img, [pos_x, pos_y], 1])

        return pipe_list


class screen_pipe_cls():

    def __init__(self):
        self.pipe_num = 18
        pipe = []
        x = 450
        for i in range(1, self.pipe_num + 1):
            pipe.append(single_pipe_cls(x))
            x += 200
        self.pipe = pipe

    def pipe_move(self, move):
        for pipe in self.pipe:
            pipe.pos[0] -= move
        if self.pipe[0].pos[0] < -25:
            self.pipe.pop(0)
            x = self.pipe[-1].pos[0]
            self.pipe.append(single_pipe_cls(x + 200))


def main():

    pygame.init()

    w = 450
    h = 500
    count = 0
    up = 2
    up_count = 0
    screen = pygame.display.set_mode((w, h))
    screen.fill(color.white)
    bird = bird_cls("bird.png")
    bg = bg_cls("bg.png")
    clock = pygame.time.Clock()
    drop = 0
    game_over = game_over_cls("game_over.png")
    pipes = screen_pipe_cls()
    font_2 = pygame.font.SysFont('Comic Sans MS', 30)
    run = True

    while run:
        clock.tick(60)

        if game_over.show:

            screen.blit(game_over.img, game_over.pos)

        else:
            screen.fill(color.white)
            screen.blit(bg.img, bg.pos)
            screen.blit(bird.img, bird.pos)
            # pygame.draw.circle(screen,color.black,[70,int(bird.pos[1])+30],20)

            pipes.pipe_move(1)

            for pipe in pipes.pipe:
                take = True
                for item in pipe.module_pos():
                    screen.blit(item[0], item[1])
                    if item[2] == 0:
                        if abs((item[1][0] + 12) - 70) < 20 and abs((item[1][1] + 25) - ((bird.pos[1]) + 30)) < 15:
                            game_over.show = True
                    else:
                        if abs((item[1][0] + 12) - 70) < 20 and abs(item[1][1] - ((bird.pos[1]) + 30)) < 15:
                            game_over.show = True
                    if item[1][0] == 20 and take:
                        count += 1
                        take = False

            drop += 0.2
            bird.pos[1] += drop
            if bird.pos[1] > 500:
                game_over.show = True

            bg.pos[0] -= 1

            if bg.pos[0] == -300:
                bg.pos[0] = 0

            up_count += 1
            pressed = pygame.key.get_pressed()
            if up_count == 5:
                up = 2

            if pressed[pygame.K_UP]:
                bird.pos[1] -= up
                up += 0.2
                up_count = 0
                if bird.pos[1] < 0:
                    bird.pos[1] = 0
                drop = 0

        textsurface = font_2.render(str(count), True, color.red)
        screen.blit(textsurface, (400, 25))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    run = False


if __name__ == '__main__':
    main()
