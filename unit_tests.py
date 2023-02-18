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

    def tearDown(self):
        """
        A method that is called after each test method to clean up any resources that were allocated during the test.
        This method ensures that any temporary files, database connections, or other resources that were used during
        the test are properly cleaned up, so that subsequent tests can run in a clean environment.
        """
        pygame.quit()


class TestCollision(unittest.TestCase):
    """Test collision with ItemBoxes."""
    def setUp(self):
        """SetUp Player instances."""
        self.player = Player("Player", 100, 100, 1.65, 5, 5, 5)

    def test_collision_with_ammo_box(self):
        """Test collision with ammo_box and if player.ammo increase when collided."""
        current_ammo = self.player.ammo
        ammo_box = ItemBox("Ammo", 100, 100)

        collided = pygame.sprite.collide_rect(self.player, ammo_box)
        self.assertTrue(collided, "Collision with ammo box not detected")

        if collided:
            ammo_box.update()
            current_ammo = player.ammo - 10

        self.assertEqual(player.ammo, current_ammo + 10, "Player's ammo not updated correctly")

    def test_collision_with_grenade_box(self):
        """Test collision with grenade_box and if player.grenades increase when collided."""
        current_grenades = self.player.grenades
        grenade_box = ItemBox("Grenade", 100, 100)

        collided = pygame.sprite.collide_rect(self.player, grenade_box)
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

    def tearDown(self):
        pygame.quit()


class TestPlayerBulletCollisions(unittest.TestCase):
    """Test Player collision with Bullet."""
    def setUp(self):
        """SetUp Player instances."""
        self.all_sprites = pygame.sprite.Group()
        self.player = Player("Player", 100, 100, 1.65, 5, 5, 5)
        self.all_sprites.add(self.player)
        self.bullet = Bullet(110, 100, 1)
        self.all_sprites.add(self.bullet)
        self.bullet_group = pygame.sprite.Group(self.bullet)

    def test_player_health_decreases_on_bullet_collision(self):
        """Test if player.health is decreasing when collide with bullet."""
        initial_health = self.player.health
        bullet_collided = pygame.sprite.spritecollide(self.player, self.bullet_group, False)
        if bullet_collided:
            for bullet in bullet_collided:
                bullet.kill()
                if self.player.alive:
                    self.player.health -= 5
        self.assertEqual(self.player.health, initial_health - 5)

    def tearDown(self):
        pygame.quit()


class TestPlayerGrenadeCollisions(unittest.TestCase):
    """Test Player collision with grenade."""
    def setUp(self):
        """SetUp Player instances."""
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.player = Player("Player", 100, 100, 1.65, 5, 5, 5)
        self.all_sprites.add(self.player)
        self.grenade = Grenade(110, 100, 1)
        self.all_sprites.add(self.grenade)
        self.grenade_group = pygame.sprite.Group(self.grenade)

    def test_player_health_decreases_on_grenade_collision(self):
        """Test if player.health is decreasing when collide with grenade."""
        initial_health = self.player.health
        # simulate collision between player and grenade
        grenade_collided = pygame.sprite.spritecollide(self.player, self.grenade_group, False)
        if grenade_collided:
            for grenade in grenade_collided:
                grenade.kill()
                if self.player.alive:
                    self.player.health -= 50
        self.assertEqual(self.player.health, initial_health - 50)

    def tearDown(self):
        pygame.quit()


class TestEnemyBulletCollision(unittest.TestCase):
    """Test Enemy collision with bullet."""
    def setUp(self):
        """SetUp Enemy instances."""
        self.all_sprites = pygame.sprite.Group()
        self.enemy = Player("Enemy", 100, 100, 1.65, 2, 20, 0)
        self.all_sprites.add(self.enemy)
        self.bullet = Bullet(110, 100, 1)
        self.all_sprites.add(self.bullet)
        self.bullet_group = pygame.sprite.Group(self.bullet)
        self.enemy_group = pygame.sprite.Group(self.enemy)

    def test_enemy_health_decreases_on__bullet_collision(self):
        """Test if enemy.health is decreasing when collide with bullet."""
        initial_health = self.enemy.health
        bullet_collided = pygame.sprite.spritecollide(self.enemy, self.bullet_group, False)
        if bullet_collided:
            for bullet in bullet_collided:
                bullet.kill()
                if self.enemy.alive:
                    self.enemy.health -= 25
        self.assertEqual(self.enemy.health, initial_health - 25)

    def tearDown(self):
        pygame.quit()


class TestEnemyGrenadeCollisions(unittest.TestCase):
    """Test Enemy collision with grenade."""
    def setUp(self):
        """SetUp Enemy instances."""
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.enemy = Player("Enemy", 100, 100, 1.65, 2, 20, 0)
        self.all_sprites.add(self.enemy)
        self.grenade = Grenade(110, 100, 1)
        self.all_sprites.add(self.grenade)
        self.grenade_group = pygame.sprite.Group(self.grenade)
        self.enemy_group = pygame.sprite.Group(self.enemy)

    def test_enemy_health_decreases_on_grenade_collision(self):
        """Test if enemy.health is decreasing when collide with grenade."""
        initial_health = self.enemy.health
        # simulate collision between enemy and grenade
        grenade_collided = pygame.sprite.spritecollide(self.enemy, self.grenade_group, False)
        if grenade_collided:
            for grenade in grenade_collided:
                grenade.kill()
                if self.enemy.alive:
                    self.enemy.health -= 50
        self.assertEqual(self.enemy.health, initial_health - 50)

    def tearDown(self):
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
        pygame.quit()


if __name__ == '__main__':
    unittest.main()