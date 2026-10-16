
import random
import math
import pygame

CELL, COLS, ROWS = 20, 30, 30
WIDTH, HEIGHT = COLS * CELL, ROWS * CELL + 30
ZONE_TOP = ROWS - 6
TICK, PLAYER_SPEED, BULLET_SPEED = 0.09, 260, 620
MUSHROOM_HP = 4

# Temporary visual particles for centipede hits.
HIT_SPARKS = []


# TASK 2: Mushroom colors based on remaining health.
def mushroom_color(hp):
    colors = {
        4: (200, 80, 170),
        3: (255, 180, 70),
        2: (255, 100, 70),
        1: (220, 60, 60),
    }
    return colors.get(hp, (200, 80, 170))


# TASK 3: Create sparks when a centipede segment is hit.
def on_segment_hit(segment, score):
    x = segment.col * CELL + CELL // 2
    y = segment.row * CELL + CELL // 2

    for _ in range(10):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(45, 130)

        HIT_SPARKS.append([
            float(x),
            float(y),
            math.cos(angle) * speed,
            math.sin(angle) * speed,
            0.35
        ])


# TASK 4: Increase speed by 15% for every new wave.
def wave_speed_bonus(wave):
    return 1 + 0.15 * max(0, wave - 1)


class Segment:
    def __init__(self, row, col, direction):
        self.row, self.col, self.dx, self.dy = row, col, direction, 1

    def step(self, mushrooms):
        nxt = self.col + self.dx

        if nxt < 0 or nxt >= COLS or (self.row, nxt) in mushrooms:
            self.row += self.dy
            self.dx = -self.dx

            if self.row >= ROWS - 1:
                self.row, self.dy = ROWS - 1, -1
            elif self.row <= ZONE_TOP and self.dy < 0:
                self.dy = 1
        else:
            self.col = nxt


class Game:
    def __init__(self):
        self.font = pygame.font.Font(None, 26)
        self.reset()

    def reset(self):
        HIT_SPARKS.clear()

        self.score, self.lives, self.wave, self.state = 0, 3, 1, "play"
        self.mushrooms = {}
        self.mushroom_flash = {}

        for _ in range(45):
            cell = (
                random.randint(1, ZONE_TOP - 2),
                random.randint(0, COLS - 1)
            )
            self.mushrooms[cell] = MUSHROOM_HP

        self.respawn()
        self.spawn_wave()

    def respawn(self):
        self.x = WIDTH / 2
        self.y = HEIGHT - 50
        self.bullet = None
        self.invulnerable = 1.5

    def spawn_wave(self):
        length = 10 + self.wave
        self.chains = [[
            Segment(0, COLS - 1 - i, -1)
            for i in range(length)
        ]]
        self.timer = 0.0

    def fire(self):
        if self.bullet is None and self.state == "play":
            self.bullet = pygame.Vector2(self.x, self.y - 12)

    # TASK 1: Mushrooms disappear after four hits.
    # TASK 2: Flash white briefly when hit.
    def hit_mushroom(self, cell):
        if cell not in self.mushrooms:
            return

        self.mushrooms[cell] -= 1

        if self.mushrooms[cell] <= 0:
            del self.mushrooms[cell]
            self.mushroom_flash.pop(cell, None)
            self.score += 5
        else:
            self.mushroom_flash[cell] = 0.12

    def split_chain(self, chain, index):
        segment = chain[index]

        self.chains.remove(chain)

        left, right = chain[:index], chain[index + 1:]
        self.chains.extend(part for part in (left, right) if part)

        self.mushrooms[(segment.row, segment.col)] = MUSHROOM_HP
        self.score += 100 if index == 0 else 10

        on_segment_hit(segment, self.score)

    def update_bullet(self, dt):
        if self.bullet is None:
            return

        self.bullet.y -= BULLET_SPEED * dt
        cell = (
            int(self.bullet.y // CELL),
            int(self.bullet.x // CELL)
        )

        if self.bullet.y < 0:
            self.bullet = None

        elif cell in self.mushrooms:
            self.hit_mushroom(cell)
            self.bullet = None

        else:
            for chain in self.chains:
                for index, segment in enumerate(chain):
                    if (segment.row, segment.col) == cell:
                        self.split_chain(chain, index)
                        self.bullet = None
                        return

    def update(self, dt, keys):
        # Update spark particles even if the game is over.
        updated_sparks = []

        for x, y, vx, vy, life in HIT_SPARKS:
            life -= dt

            if life > 0:
                x += vx * dt
                y += vy * dt
                updated_sparks.append([x, y, vx, vy, life])

        HIT_SPARKS[:] = updated_sparks

        # Update mushroom flash timers.
        for cell in list(self.mushroom_flash):
            self.mushroom_flash[cell] -= dt

            if self.mushroom_flash[cell] <= 0:
                del self.mushroom_flash[cell]

        if self.state != "play":
            return

        self.invulnerable = max(0.0, self.invulnerable - dt)

        self.x += (
            keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        ) * PLAYER_SPEED * dt

        self.y += (
            keys[pygame.K_DOWN] - keys[pygame.K_UP]
        ) * PLAYER_SPEED * dt

        self.x = max(10, min(WIDTH - 10, self.x))
        self.y = max(
            ZONE_TOP * CELL + 10,
            min(ROWS * CELL - 10, self.y)
        )

        if keys[pygame.K_SPACE]:
            self.fire()

        self.update_bullet(dt)
        self.timer += dt

        # TASK 4: Higher waves move faster.
        effective_tick = TICK / wave_speed_bonus(self.wave)

        while self.timer >= effective_tick:
            self.timer -= effective_tick

            for chain in self.chains:
                for segment in chain:
                    segment.step(self.mushrooms)

        player_cell = (int(self.y // CELL), int(self.x // CELL))

        if self.invulnerable <= 0 and any(
            (s.row, s.col) == player_cell
            for chain in self.chains
            for s in chain
        ):
            self.lives -= 1
            self.respawn()

            if self.lives <= 0:
                self.state = "lose"

        if not self.chains:
            self.wave += 1
            self.spawn_wave()

    def draw(self, screen):
        screen.fill((8, 8, 16))

        # Draw mushrooms and their hit effects.
        for (row, col), hp in self.mushrooms.items():
            cell = (row, col)

            if self.mushroom_flash.get(cell, 0) > 0:
                color = (255, 255, 255)
            else:
                color = mushroom_color(hp)

            center = (
                col * CELL + CELL // 2,
                row * CELL + CELL // 2
            )

            pygame.draw.circle(
                screen, color, center, CELL // 2 - 1
            )

            pygame.draw.rect(
                screen, (230, 230, 200),
                (center[0] - 3, center[1], 6, CELL // 2 - 1)
            )

        # Draw centipede segments.
        for chain in self.chains:
            for index, segment in enumerate(chain):
                center = (
                    segment.col * CELL + CELL // 2,
                    segment.row * CELL + CELL // 2
                )

                color = (
                    (240, 200, 60)
                    if index == 0
                    else (80, 220, 90)
                )

                pygame.draw.circle(
                    screen, color, center, CELL // 2
                )

        # Draw sparks from destroyed segments.
        for x, y, vx, vy, life in HIT_SPARKS:
            radius = max(1, int(4 * life / 0.35))

            pygame.draw.circle(
                screen, (255, 220, 80),
                (int(x), int(y)), radius
            )

        if self.bullet:
            pygame.draw.rect(
                screen, (255, 255, 255),
                (self.bullet.x - 1, self.bullet.y - 6, 3, 10)
            )

        if self.invulnerable <= 0 or int(self.invulnerable * 10) % 2 == 0:
            pygame.draw.polygon(
                screen, (80, 200, 255),
                [
                    (self.x, self.y - 10),
                    (self.x + 10, self.y + 10),
                    (self.x - 10, self.y + 10)
                ]
            )

        hud = self.font.render(
            f"Score {self.score}  Lives {self.lives}  "
            f"Wave {self.wave}  R = reset",
            True, (240, 240, 240)
        )

        screen.blit(hud, (10, ROWS * CELL + 6))

        if self.state == "lose":
            label = self.font.render(
                "GAME OVER - Press R", True, (255, 255, 120)
            )

            screen.blit(
                label,
                label.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            )


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Centipede")

    clock = pygame.time.Clock()
    game = Game()
    running = True

    while running:
        dt = min(clock.tick(60) / 1000, 0.05)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                game.reset()

        game.update(dt, pygame.key.get_pressed())
        game.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
