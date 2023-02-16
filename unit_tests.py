import unittest
import pygame

from main import *


class TestPlayer(unittest.TestCase):
    def test_player_alive(self):
        player.health = 0
        player.check_alive()
        self.assertFalse(player.alive)

    def ammo_shoot(self):
        self.player = Solder("Player", 100, 100, 1.65, 5, 5, 5)
        start_ammo = self.player.ammo
        player.shoot()
        self.assertEqual(player.ammo, start_ammo - 1)

    def grenade_shoot(self):
        start_grenades = player.grenades
        grenade_thrown = True
        self.assertEqual(player.grenades, start_grenades - 1)


class TestCollision(unittest.TestCase):
    def test_collision_with_ammo_box(self):
        # Create player and ammo box sprites
        self.player = Solder("Player", 100, 100, 1.65, 5, 5, 5)
        current_ammo = self.player.ammo

        # shoot pressed
        ammo_box = ItemBox("Ammo", 100, 100)

        # Set player position to be at the same position as the ammo box
        # self.player.rect.center = ammo_box.rect.center

        # Check if collision occurs
        collided = pygame.sprite.collide_rect(self.player, ammo_box)

        # Assert that collision occurs
        self.assertTrue(collided, "Collision with ammo box not detected")

        if collided:
            ammo_box.update()
            current_ammo = player.ammo - 15
            # self.player.update()
        # print(f"player.ammo after collision: {self.player.ammo}")

        # self.player.update()
        self.assertEqual(player.ammo, current_ammo + 15, "Player's ammo not updated correctly")

    def test_collision_with_grenade(self):
        self.player = Solder("Player", 100, 100, 1.65, 5, 5, 5)
        current_grenades = self.player.grenades
        grenade_box = ItemBox("Grenade", 100, 100)

        # Check if collision occurs
        collided = pygame.sprite.collide_rect(self.player, grenade_box)

        # Assert that collision occurs
        self.assertTrue(collided, "Collision with grenade box not detected")

        if collided:
            grenade_box.update()
            #
            current_grenades = player.grenades - 3

        self.assertEqual(player.grenades, current_grenades + 3, "Player's grenades not updated correctly")

    def test_collision_with_health(self):
        self.player = Solder("Player", 100, 100, 1.65, 5, 5, 5)
        current_health = player.health
        health_box = ItemBox("Health", 100, 100)

        collide_bullet = pygame.sprite.spritecollide(player, bullet_group, False)
        if collide_bullet:
            self.assertLess(player.health, current_health)
            current_health = player.health

        collide_grenade_bullet = pygame.sprite.spritecollide(player, grenade_group, False)
        if collide_grenade_bullet:
            self.assertLess(player.health, current_health)
            current_health = player.health

        # Check if collision occurs
        collided_with_health_box = pygame.sprite.collide_rect(self.player, health_box)
        if collided_with_health_box:
            self.assertGreater(player.health, player.health - 25)
            current_health = player.health


class TestMovingLeftAndRight(unittest.TestCase):
    def setUp(self):
        self.player = Solder("Player", 0, 0, 1.65, 5, 5, 5)

    def test_move_left(self):
        starting_postition = player.rect.x
        player.move(True, False)
        self.assertLess(player.rect.x, starting_postition)

    def test_move_right(self):
        starting_postition = player.rect.x
        player.move(False, True)
        self.assertGreater(player.rect.x, starting_postition)

    def test_move_left_direction(self):
        player.move(True, False)
        self.assertEqual(player.direction, -1)

    def test_move_right_direction(self):
        player.move(False, True)
        self.assertEqual(player.direction, 1)

    def tearDown(self):
        pygame.quit()


if __name__ == '__main__':
    unittest.main()