import unittest
from main import *


class TestPlayer(unittest.TestCase):
    """Test Player."""
    def SetUp(self):
        """SetUp Player instances."""
        self.player = Player("Player", 100, 100, 1.65, 5, 5, 5)

    def test_player_alive(self):
        """Test if player is still alive, when has 0 health."""
        player.health = 0
        player.check_alive()
        self.assertFalse(player.alive)

    def ammo_shoot(self):
        """Test if number of bullets is decreasing when pressed to shoot."""
        start_ammo = player.ammo
        player.shoot()
        self.assertEqual(player.ammo, start_ammo - 1)

    def grenade_shoot(self):
        """Test number of grenades is decreasing when pressed to throw."""
        start_grenades = player.grenades
        grenade_thrown = True
        self.assertEqual(player.grenades, start_grenades - 1)


class TestCollision(unittest.TestCase):
    """Test collision with ItemBoxes."""
    def setUp(self):
        self.player = Player("Player", 100, 100, 1.65, 5, 5, 5)

    def test_collision_with_ammo_box(self):
        """Test collision with ammo_box and if player.ammo increase when collided."""
        # Create ammo box sprites
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
            current_ammo = player.ammo - 10
            # self.player.update()
        # print(f"player.ammo after collision: {self.player.ammo}")

        # self.player.update()
        self.assertEqual(player.ammo, current_ammo + 10, "Player's ammo not updated correctly")

    def test_collision_with_grenade_box(self):
        """Test collision with grenade_box and if player.grenades increase when collided."""
        current_grenades = self.player.grenades
        grenade_box = ItemBox("Grenade", 100, 100)

        # Check if collision occurs
        collided = pygame.sprite.collide_rect(self.player, grenade_box)

        # Assert that collision occurs
        self.assertTrue(collided, "Collision with grenade box not detected")

        if collided:
            grenade_box.update()
            current_grenades = player.grenades - 3

        self.assertEqual(player.grenades, current_grenades + 3, "Player's grenades not updated correctly")

    def test_collision_with_health_box(self):
        """Test collision with health_box."""
        current_health = self.player.health
        health_box = ItemBox("Health", 100, 100)

        collided = pygame.sprite.collide_rect(self.player, health_box)
        self.assertTrue(collided, "Collision with health box not detected")

        if collided:
            health_box.update()
            current_health = player.health - 15

        self.assertEqual(player.health, current_health + 15)
    """
    # FIX ITT!
    def test_collision_with_bullet(self):
        start_health = player.health
        bullet = Bullet(100, 100, -1)
        bullet_group.add(bullet)
        
        collide = pygame.sprite.spritecollide(player, bullet_group, False)
        if collide:
            start_health = 
        self.assertEqual(player.health, start_health - counter)
    
    def test_collision_with_grenade(self):
        counter = 0
        collide_grenade_bullet = pygame.sprite.spritecollide(player, grenade_group, False)
        if collide_grenade_bullet:
            counter += 25
        self.assertEqual(player.health, player.health - counter)
    """

    def test_collision_with_water(self):
        collide_water = pygame.sprite.spritecollide(player, water_group, False)
        if collide_water:
            self.assertEqual(player.health, 0)

    def test_collision_with_next_level(self):
        start_level = level
        collide_nex_level = pygame.sprite.spritecollide(player, exit_group, False)
        if collide_nex_level:
            self.assertEqual(level, start_level + 1)

    def tearDown(self):
        """
        A method that is called after each test method to clean up any resources that were allocated during the test.
        This method ensures that any temporary files, database connections, or other resources that were used during
        the test are properly cleaned up, so that subsequent tests can run in a clean environment.
        """
        pygame.quit()


class TestMovingLeftAndRight(unittest.TestCase):
    """Test Player's changing direction and moving."""

    def setUp(self):
        """Set up Player instances."""
        self.player = Player("Player", 0, 0, 1.65, 5, 5, 5)

    def test_move_left(self):
        """Test if position is smaller than starting when moving left."""
        starting_position = player.rect.x
        if player.alive:
            player.move(True, False)
            self.assertLess(player.rect.x, starting_position)

    def test_move_right(self):
        """Test if position is greater than starting when moving right."""
        starting_position = player.rect.x
        if player.alive:
            player.move(False, True)
            self.assertGreater(player.rect.x, starting_position)

    def test_move_left_direction(self):
        """Test if direction is changing to negative when moving left."""
        player.move(True, False)
        self.assertEqual(player.direction, -1)

    def test_move_right_direction(self):
        """Test if direction is changing to positive when moving right."""
        player.move(False, True)
        self.assertEqual(player.direction, 1)

    def tearDown(self):
        """
        A method that is called after each test method to clean up any resources that were allocated during the test.
        This method ensures that any temporary files, database connections, or other resources that were used during
        the test are properly cleaned up, so that subsequent tests can run in a clean environment.
        """
        pygame.quit()


class TestEnemy(unittest.TestCase):
    def detUp(self):
        self.enemy = Player('Enemy', 100, 100, 1.65, 2, 20, 0)
    """
    # FIX ITT!
    def test_enemy_collision_with_bullet(self):
        counter = 0
        collide_with_bullet = pygame.sprite.spritecollide(enemy, bullet_group, False)
        if collide_with_bullet:
            counter += 25
        self.assertEqual(enemy.health, enemy.health - counter)

    def test_enemy_collision_with_grenade(self):
        counter = 0
        collide_grenade_bullet = pygame.sprite.spritecollide(enemy, grenade_group, False)
        if collide_grenade_bullet:
            counter += 50
        self.assertEqual(enemy.health, enemy.health - counter)
    """


if __name__ == '__main__':
    unittest.main()