import pygame
import sys
from button import Button

pygame.init()

WIDTH, HEIGHT = 900, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pomodoro Timer")

CLOCK = pygame.time.Clock()

BACKDROP = pygame.image.load("assets/backdrop.png")
WHITE_BUTTON = pygame.image.load("assets/button.png")
RESET_SYM = pygame.image.load("assets/icon.png")

FONT = pygame.font.Font("assets/ArialRoundedMTBold.ttf", 120)
timer_text = FONT.render("25:00", True, "white")
timer_text_rect = timer_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 25))

START_STOP_BUTTON = Button(WHITE_BUTTON, (WIDTH / 2 - 35, HEIGHT / 2 + 100), 170, 60, "START",
                           pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20), "#3f4299", "#9ab034")
POMODORO_BUTTON = Button(None, (WIDTH / 2 - 150, HEIGHT / 2 - 140), 120, 30, "Pomodoro",
                         pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20), "#FFFFFF", "#9ab034")
SHORT_BREAK_BUTTON = Button(None, (WIDTH / 2, HEIGHT / 2 - 140), 120, 30, "Short Break",
                            pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20), "#FFFFFF", "#9ab034")
LONG_BREAK_BUTTON = Button(None, (WIDTH / 2 + 150, HEIGHT / 2 - 140), 120, 30, "Long Break",
                           pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20), "#FFFFFF", "#9ab034")
RESET_BUTTON = Button(RESET_SYM, (WIDTH / 2 + 87, HEIGHT / 2 + 100), 40, 40, None,
                      pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20), "#FFFFFF", "#9ab034")


POMODORO_LENGTH = 2  # 1500 secs / 25 mins
SHORT_BREAK_LENGTH = 5  # 300 secs / 5 mins
LONG_BREAK_LENGTH = 10  # 900 secs / 15 mins

current_seconds = POMODORO_LENGTH
pygame.time.set_timer(pygame.USEREVENT, 1000) # after how many milliseconds the event itterates
started = False
pomodoro = True
short = False
long = False
count = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if RESET_BUTTON.check_for_input(pygame.mouse.get_pos()):
                count = 0
                pomodoro = True
                short = False
                long = False
                started = False
                current_seconds = POMODORO_LENGTH
            if START_STOP_BUTTON.check_for_input(pygame.mouse.get_pos()):
                if started:
                    started = False
                else:
                    started = True
            if POMODORO_BUTTON.check_for_input(pygame.mouse.get_pos()):
                current_seconds = POMODORO_LENGTH
                started = False
                pomodoro = True
                short = False
            if SHORT_BREAK_BUTTON.check_for_input(pygame.mouse.get_pos()):
                current_seconds = SHORT_BREAK_LENGTH
                started = False
                pomodoro = False
                short = True
            if LONG_BREAK_BUTTON.check_for_input(pygame.mouse.get_pos()):
                current_seconds = LONG_BREAK_LENGTH
                started = False
                pomodoro = False
            if started:
                START_STOP_BUTTON.text_input = "PAUSE"
                START_STOP_BUTTON.text = pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20).render(
                                        START_STOP_BUTTON.text_input, True, START_STOP_BUTTON.base_color)
            else:
                START_STOP_BUTTON.text_input = "START"
                START_STOP_BUTTON.text = pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20).render(
                    START_STOP_BUTTON.text_input, True, START_STOP_BUTTON.base_color)
        if pomodoro and (count % 3 != 0) and current_seconds == 0 and started:
            current_seconds = SHORT_BREAK_LENGTH + 1
            short = True
            pomodoro = False
            count = count + 1
        if (count % 3 == 0) and current_seconds == 0 and started:
            count = count + 1
            current_seconds = LONG_BREAK_LENGTH + 1
            long = True
        if short and current_seconds == 0 and started:
            current_seconds = POMODORO_LENGTH + 1
            pomodoro = True
            short = False
        if long and current_seconds == 0 and started:
            current_seconds = POMODORO_LENGTH + 1
            pomodoro = True
            long = False
        if event.type == pygame.USEREVENT and started:
            current_seconds -= 1

    SCREEN.fill("#e9e9e9")
    SCREEN.blit(BACKDROP, BACKDROP.get_rect(center=(WIDTH / 2, HEIGHT / 2)))

    START_STOP_BUTTON.update(SCREEN)
    START_STOP_BUTTON.change_color(pygame.mouse.get_pos())
    POMODORO_BUTTON.update(SCREEN)
    POMODORO_BUTTON.change_color(pygame.mouse.get_pos())
    SHORT_BREAK_BUTTON.update(SCREEN)
    SHORT_BREAK_BUTTON.change_color(pygame.mouse.get_pos())
    LONG_BREAK_BUTTON.update(SCREEN)
    LONG_BREAK_BUTTON.change_color(pygame.mouse.get_pos())
    RESET_BUTTON.update(SCREEN)

    COUNT_BUTTON = Button(None, (WIDTH / 2, HEIGHT / 2 + 145), 120, 30, f"Pomodoro Count: {count}",
                          pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20), "#FFFFFF", "#FFFFFF")
    COUNT_BUTTON.update(SCREEN)

    if current_seconds >= 0:
        # convert current seconds to time format
        display_seconds = current_seconds % 60
        display_minutes = int(current_seconds / 60) % 60
    # :02 -> add a padding using character 0 and the padding to be 2 (zero-adding)
    timer_text = FONT.render(f"{display_minutes:02}:{display_seconds:02}", True, "white")
    SCREEN.blit(timer_text, timer_text_rect)


    pygame.display.update()