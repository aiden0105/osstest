import pygame
import random

# 게임 설정: 화면 크기, 격자 크기 및 지뢰 수 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
MINE_COUNT = 40    # 지뢰 총 개수

class Minesweeper:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Minesweeper")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.choose_difficulty()
        self.reset()

    # 난이도 설정 (easy, medium, hard)
    def choose_difficulty(self):
        print("Choose difficulty: Easy (1), Medium (2), Hard (3)")
        choice = input("Enter your choice (1, 2, or 3): ")
        if choice == '1':
            self.grid_size = 8
            self.mine_count = 10
            self.screen_width = 400
            self.screen_height = 400
        elif choice == '2':
            self.grid_size = 10
            self.mine_count = 15
            self.screen_width = 500
            self.screen_height = 500
        else:  # Default to hard if no or invalid input
            self.grid_size = 20
            self.mine_count = 40
            self.screen_width = 800
            self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

    # 모든 게임 필드 초기화
    def reset(self):
        self.mines = [[False] * self.grid_size for _ in range(self.grid_size)]
        self.adjacent = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.flags = [[False] * self.grid_size for _ in range(self.grid_size)]
        self.grid = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.game_over = False
        self.victory = False
        self.place_mines()

                        
    # 지뢰를 게임 보드에 무작위로 배치하는 함수
    def place_mines(self):
        placed = 0
        while placed < self.mine_count:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            if not self.mines[x][y]:
                self.mines[x][y] = True
                self.increment_adjacent(x, y)  # 인접 칸 지뢰 수 증가
                placed += 1

    # 주어진 위치 주변의 지뢰 수를 증가시키는 함수
    def increment_adjacent(self, x, y):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                    self.adjacent[nx][ny] += 1
                    
    # 마우스 입력 처리 함수
    def handle_mouse_input(self, event):
        x, y = event.pos[0] // (self.screen_width // self.grid_size), event.pos[1] // (self.screen_height // self.grid_size)
        if event.button == 1 and not self.flags[x][y]:  # 왼쪽 클릭 처리
            self.open_cell(x, y)
        elif event.button == 3 and not self.grid[x][y]:  # 오른쪽 클릭 처리
            self.toggle_flag(x, y)


    # 지정된 위치의 칸을 여는 함수
    def open_cell(self, x, y):
        if not self.grid[x][y]:
            self.grid[x][y] = 1
            if self.mines[x][y]:
                self.game_over = True
            elif self.adjacent[x][y] == 0:
                self.open_adjacent_cells(x, y)  # 인접한 칸 자동으로 열기

    # 지정된 위치의 인접 칸을 자동으로 여는 함수
    def open_adjacent_cells(self, x, y):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and not self.grid[nx][ny]:
                    self.open_cell(nx, ny)

    # 깃발 상태를 토글하는 함수
    def toggle_flag(self, x, y):
        self.flags[x][y] = not self.flags[x][y]

    # 게임 보드 그리기 함수
    def draw_board(self):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                rect = pygame.Rect(x * (self.screen_width // self.grid_size), y * (self.screen_height // self.grid_size),
                                   self.screen_width // self.grid_size, self.screen_height // self.grid_size)
                if self.grid[x][y] == 1:
                    if self.mines[x][y]:
                        pygame.draw.rect(self.screen, (255, 0, 0), rect)  # 지뢰가 있는 칸은 빨간색으로 표시
                    else:
                        pygame.draw.rect(self.screen, (255, 255, 255), rect)  # 안전한 칸은 흰색으로 표시
                        if self.adjacent[x][y] > 0:
                            label = self.font.render(str(self.adjacent[x][y]), True, (0, 0, 0))
                            self.screen.blit(label, rect.topleft)  # 인접 지뢰 수를 표시
                else:
                    pygame.draw.rect(self.screen, (160, 160, 160), rect)  # 닫힌 칸은 회색으로 표시
                    if self.flags[x][y]:
                        pygame.draw.circle(self.screen, (0, 0, 255), (rect.centerx, rect.centery), 10)  # 깃발이 있는 칸에는 파란색 원을 표시
        if self.game_over:
            message = self.font.render("Game Over! You hit a mine.", True, (255, 0, 0))
            self.screen.blit(message, (SCREEN_WIDTH / 2 - message.get_width() / 2, SCREEN_HEIGHT / 2))

        if self.victory:
            message = self.font.render("You Won! All safe squares revealed.", True, (0, 255, 0))
            self.screen.blit(message, (SCREEN_WIDTH / 2 - message.get_width() / 2, SCREEN_HEIGHT / 2))

    # 게임 실행 함수
    def run(self):
        while True:  # 게임을 계속 반복 실행할 수 있도록 무한 루프로 변경
            while not self.game_over and not self.victory:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.handle_mouse_input(event)
                self.screen.fill((0, 0, 0))
                self.draw_board()
                pygame.display.flip()
                self.clock.tick(30)
    
                if self.game_over:
                    pygame.time.wait(1000)  # 게임 오버시 1초 대기
                    break
                if self.victory:
                    pygame.time.wait(5000)  # 승리시 5초 대기
                    break
    
            self.reset()  # 게임 상태를 초기화하여 새 게임 시작

if __name__ == "__main__":
    game = Minesweeper()
    game.run()
