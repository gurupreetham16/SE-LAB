import pygame
from pathlib import Path

from .player import Player
from .platform import Platform
from .hazard import Hazard


WHITE = (255, 255, 255)
BLACK = (20, 20, 25)
BROWN = (150, 100, 60)
RED = (220, 60, 60)
GREEN = (0, 200, 0)
YELLOW = (245, 220, 70)
GRAY = (180, 180, 180)


class GameEngine:
    DIFFICULTIES = {
        "Easy": {"gravity": 0.45, "jump": -13},
        "Medium": {"gravity": 0.60, "jump": -12},
        "Hard": {"gravity": 0.85, "jump": -11},
    }

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.start_x = 40
        self.start_y = height - 120
        self.goal_x = 740
        self.score = 0

        self.font = pygame.font.SysFont("Arial", 30)
        self.big_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 24)

        self.sounds = self._load_sounds()
        self.difficulty = "Medium"
        self.gravity = self.DIFFICULTIES[self.difficulty]["gravity"]

        self._build_level()
        self.game_over = False
        self.game_over_reason = ""

    def _load_sounds(self):
        base = Path(__file__).resolve().parent.parent / "assets" / "sounds"

        sounds = {}
        for name in ("jump", "goal", "death"):
            try:
                sounds[name] = pygame.mixer.Sound(str(base / f"{name}.wav"))
            except (pygame.error, FileNotFoundError):
                sounds[name] = None
        return sounds

    def _play(self, name):
        sound = self.sounds.get(name)
        if sound is not None:
            sound.play()

    def _build_level(self):
        self.player = Player(self.start_x, self.start_y)
        self.player.jump_strength = self.DIFFICULTIES[
            self.difficulty
        ]["jump"]

        ground_y = self.height - 40
        self.platforms = [
            Platform(0, ground_y, 160),
            Platform(220, ground_y, 140),
            Platform(420, ground_y - 60, 120),
            Platform(600, ground_y, 180),
        ]

        self.hazards = [
            Hazard(240, ground_y - 14, 100)
        ]

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if self.game_over:
            if event.key == pygame.K_1:
                self.restart("Easy")
            elif event.key == pygame.K_2:
                self.restart("Medium")
            elif event.key == pygame.K_3:
                self.restart("Hard")
            elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                pygame.event.post(
                    pygame.event.Event(pygame.QUIT)
                )
            return

        if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
            if self.player.jump():
                self._play("jump")

    def handle_input(self):
        if self.game_over:
            self.player.vx = 0
            return

        keys = pygame.key.get_pressed()
        self.player.vx = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.vx = -self.player.speed

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.vx = self.player.speed

    def _set_game_over(self, reason):
        if self.game_over:
            return

        self.game_over = True
        self.game_over_reason = reason
        self.player.vx = 0
        self._play("death")

    def update(self):
        if self.game_over:
            return

        self.player.vy += self.gravity

        # Horizontal movement.
        self.player.x += self.player.vx
        self.player.x = max(
            0,
            min(self.width - self.player.width, self.player.x)
        )

        # Task 1:
        # Continuous/swept vertical collision detection.
        # Save the previous bottom before moving, then detect
        # whether the player crossed a platform's top surface
        # during this frame. This prevents tunneling at high
        # fall speeds.
        previous_bottom = self.player.y + self.player.height

        self.player.y += self.player.vy

        current_bottom = self.player.y + self.player.height
        self.player.on_ground = False

        if self.player.vy >= 0:
            for platform in self.platforms:
                rect = platform.rect()

                horizontal_overlap = (
                    self.player.x < rect.right
                    and self.player.x + self.player.width > rect.left
                )

                crossed_top = (
                    previous_bottom <= rect.top
                    and current_bottom >= rect.top
                )

                if horizontal_overlap and crossed_top:
                    self.player.y = rect.top - self.player.height
                    self.player.vy = 0
                    self.player.on_ground = True
                    break

        # Hazard collision.
        for hazard in self.hazards:
            if self.player.rect().colliderect(hazard.rect()):
                self._set_game_over("You hit the hazard!")
                return

        # Fell below the screen.
        if self.player.y > self.height:
            self._set_game_over("You fell off the level!")
            return

        # Goal reached.
        if self.player.x >= self.goal_x:
            self.score += 1
            self._play("goal")
            self.player.reset(self.start_x, self.start_y)

    def restart(self, difficulty):
        self.difficulty = difficulty
        self.gravity = self.DIFFICULTIES[difficulty]["gravity"]
        self._build_level()
        self.game_over = False
        self.game_over_reason = ""

    def render(self, screen):
        for platform in self.platforms:
            pygame.draw.rect(screen, BROWN, platform.rect())

        for hazard in self.hazards:
            pygame.draw.rect(screen, RED, hazard.rect())

        goal_rect = pygame.Rect(self.goal_x, 0, 6, self.height)
        pygame.draw.rect(screen, GREEN, goal_rect)

        pygame.draw.rect(screen, WHITE, self.player.rect())

        score_text = self.font.render(
            f"Score: {self.score}", True, WHITE
        )
        screen.blit(score_text, (10, 10))

        difficulty_text = self.small_font.render(
            f"Difficulty: {self.difficulty}", True, WHITE
        )
        screen.blit(difficulty_text, (10, 45))

        if self.game_over:
            overlay = pygame.Surface(
                (self.width, self.height),
                pygame.SRCALPHA
            )
            overlay.fill((0, 0, 0, 165))
            screen.blit(overlay, (0, 0))

            title = self.big_font.render(
                "GAME OVER", True, WHITE
            )
            screen.blit(
                title,
                title.get_rect(
                    center=(self.width // 2, 95)
                )
            )

            reason = self.small_font.render(
                self.game_over_reason, True, WHITE
            )
            screen.blit(
                reason,
                reason.get_rect(
                    center=(self.width // 2, 155)
                )
            )

            final_score = self.font.render(
                f"Final Score: {self.score}", True, YELLOW
            )
            screen.blit(
                final_score,
                final_score.get_rect(
                    center=(self.width // 2, 205)
                )
            )

            line1 = self.small_font.render(
                "1 - Easy     2 - Medium     3 - Hard",
                True, WHITE
            )
            line2 = self.small_font.render(
                "Choose a difficulty to replay",
                True, GRAY
            )
            line3 = self.small_font.render(
                "Q / ESC - Exit",
                True, GRAY
            )

            screen.blit(
                line1,
                line1.get_rect(
                    center=(self.width // 2, 275)
                )
            )
            screen.blit(
                line2,
                line2.get_rect(
                    center=(self.width // 2, 315)
                )
            )
            screen.blit(
                line3,
                line3.get_rect(
                    center=(self.width // 2, 350)
                )
            )
