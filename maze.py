import pygame
import numpy as np
import time

# Constants
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
CELL_SIZE = 40
GRID_SIZE = 10


pygame.init()
win = pygame.display.set_mode((GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE))
pygame.display.set_caption("Q-Learning Agent")


q_table = np.zeros((GRID_SIZE, GRID_SIZE, 4))
actions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
start = (0, 0)
goal = (GRID_SIZE - 1, GRID_SIZE - 1)
exploration_rate = 1.0
min_exploration_rate = 0.01
exploration_decay = 0.995
learning_rate = 0.1
discount_factor = 0.99

# Define obstacles
obstacles = [(3, 3), (3, 4), (3, 5), (4, 3), (5, 3)]


def draw_maze():
    for x in range(0, GRID_SIZE * CELL_SIZE, CELL_SIZE):
        for y in range(0, GRID_SIZE * CELL_SIZE, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(win, BLACK, rect, 1)

    pygame.draw.rect(
        win, RED, (goal[1] * CELL_SIZE, goal[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    for obs in obstacles:
        pygame.draw.rect(
            win, YELLOW, (obs[1] * CELL_SIZE, obs[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))


def get_next_position(pos, action):
    next_pos = (pos[0] + action[0], pos[1] + action[1])
    if 0 <= next_pos[0] < GRID_SIZE and 0 <= next_pos[1] < GRID_SIZE and next_pos not in obstacles:
        return next_pos
    return pos


def train_and_visualize():
    global exploration_rate
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    for episode in range(1000):
        state = start
        done = False
        agent_pos = start

        start_time = time.time()

        while not done:
            win.fill(WHITE)
            draw_maze()

            if np.random.rand() < exploration_rate:
                action_index = np.random.randint(4)
            else:
                action_index = np.argmax(q_table[state[0], state[1]])

            next_state = get_next_position(state, actions[action_index])
            reward = 1 if next_state == goal else -0.1
            done = next_state == goal

            old_value = q_table[state[0], state[1], action_index]
            next_max = np.max(q_table[next_state[0], next_state[1]])

            new_value = (1 - learning_rate) * old_value + \
                learning_rate * (reward + discount_factor * next_max)
            q_table[state[0], state[1], action_index] = new_value

            state = next_state
            agent_pos = next_state

            pygame.draw.rect(
                win, BLUE, (agent_pos[1] * CELL_SIZE, agent_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

            episode_text = font.render(f'Episode: {episode + 1}', True, BLACK)
            win.blit(episode_text, (10, 10))

            pygame.display.update()
            clock.tick(10)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

        episode_duration = time.time() - start_time
        print(
            f"Episode {episode + 1} completed in {episode_duration:.2f} seconds")

        exploration_rate = max(min_exploration_rate,
                               exploration_rate * exploration_decay)


if __name__ == "__main__":
    train_and_visualize()
