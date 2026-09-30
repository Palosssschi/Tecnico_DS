import tkinter as tk
import random
import math

# Plants vs Zombies - simplified Tkinter clone
# Controls:
# 1 Sunflower, 2 Peashooter, 3 WallNut, 4 CherryBomb, 5 Repeater
# 6 IceShooter, 7 SunShroom, 8 TallNut, s toggle shovel, r restart

ROWS = 5
COLS = 9
MENU_WIDTH = 250
FIELD_GAP = 40
CELL_W = 100
CELL_H = 120
GRID_X = MENU_WIDTH + FIELD_GAP
GRID_Y = FIELD_GAP
SCREEN_W = GRID_X + COLS * CELL_W + FIELD_GAP
SCREEN_H = GRID_Y + ROWS * CELL_H + FIELD_GAP
# CORREÇÃO: Zumbis agora nascem exatamente na linha limite do Grid
SPAWN_X = GRID_X + COLS * CELL_W 
TICKS_PER_MIN = 3600

class Sun:
    def __init__(self, x, y, value=25):
        self.x = x
        self.y = y
        self.radius = 18
        self.value = value
        self.collected = False
        self.life = 900
    def update(self):
        self.life -= 1
        if self.life <= 0:
            self.collected = True
    def draw(self, c):
        if self.collected: return
        radius = max(6, int(min(CELL_W, CELL_H) * 0.18))
        c.create_oval(self.x-radius, self.y-radius, self.x+radius, self.y+radius, fill='#FFD700', outline='orange')
        c.create_text(self.x, self.y, text=str(self.value), fill='black', font=('Arial', max(6, int(radius*0.6)), 'bold'))

class Projectile:
    def __init__(self, x, y, speed=8, damage=25, effect=None, slow_factor=1.0, slow_duration=0, source=None):
        self.x = x
        self.y = y
        scale = max(0.3, CELL_W / 100.0)
        self.vx = speed * scale
        self.damage = damage
        self.effect = effect
        self.slow_factor = slow_factor
        self.slow_duration = slow_duration
        self.source = source
        self.active = True
        self.torch_boost = False
    def update(self):
        self.x += self.vx
        if self.x > SCREEN_W + 50:
            self.active = False
    def draw(self, c):
        if not self.active: return
        color = '#26ab08' if self.effect is None else '#ADD8E6'
        if self.torch_boost:
            color = '#b30006'
        r = max(4, int(min(CELL_W, CELL_H) * 0.12))
        c.create_oval(self.x-r, self.y-r, self.x+r, self.y+r, fill=color, outline='black')

class Plant:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = GRID_X + col * CELL_W + CELL_W//2
        self.y = GRID_Y + row * CELL_H + CELL_H//2
        self.health = 100
        self.max_health = self.health
        self.active = True
    def update(self, game):
        pass
    def draw(self, c):
        pass
    def draw_health(self, c):
        if not self.active: return
        pct = max(0, min(1.0, self.health / getattr(self, 'max_health', 100)))
        bw = max(24, int(CELL_W * 0.4))
        x1 = self.x - bw//2
        y1 = self.y - max(18, int(CELL_H * 0.35))
        x2 = x1 + int(bw * pct)
        c.create_rectangle(x1, y1, x1 + bw, y1 + 6, fill='black')
        c.create_rectangle(x1, y1, x2, y1 + 6, fill='red', outline='')

    def cell_draw_size(self):
        hw = max(8, int(CELL_W * 0.4))
        hh = max(8, int(CELL_H * 0.4))
        return hw, hh

class Sunflower(Plant):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.timer = 0
        self.period = 240
    def update(self, game):
        if not self.active: return
        self.timer += 1
        if self.timer >= self.period:
            self.timer = 0
            game.suns.append(Sun(self.x, self.y - 20, value=25))
    def draw(self, c):
        if not self.active: return
        hw, hh = self.cell_draw_size()
        c.create_rectangle(self.x-hw, self.y-hh, self.x+hw, self.y+hh, fill='#9ACD32', outline='black')
        c.create_text(self.x, self.y, text='Sun', font=('Arial', max(8, int(hh*0.5)), 'bold'))
        self.draw_health(c)

class Peashooter(Plant):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.cooldown = 0
        self.rate = 60
    def update(self, game):
        if not self.active: return
        if self.cooldown > 0:
            self.cooldown -= 1
            return
        target = None
        for z in game.zombies:
            if z.row == self.row and z.x <= SPAWN_X and z.x > GRID_X:
                target = z
                break
        if target:
            p = Projectile(self.x + 30, self.y, speed=9, damage=22, source='peashooter')
            game.projectiles.append(p)
            self.cooldown = self.rate
    def draw(self, c):
        if not self.active: return
        hw, hh = self.cell_draw_size()
        c.create_rectangle(self.x-hw, self.y-hh, self.x+hw, self.y+hh, fill='#3CB371', outline='black')
        c.create_text(self.x, self.y, text='Pea', font=('Arial', max(8, int(hh*0.45)), 'bold'))
        self.draw_health(c)

class Repeater(Plant):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.cooldown = 0
        self.rate = 90
    def update(self, game):
        if not self.active: return
        if self.cooldown > 0:
            self.cooldown -= 1
            return
        target = None
        for z in game.zombies:
            if z.row == self.row and z.x <= SPAWN_X and z.x > GRID_X:
                target = z
                break
        if target:
            p1 = Projectile(self.x + 30, self.y - 4, speed=9, damage=18, source='repeater')
            p2 = Projectile(self.x + 30, self.y + 4, speed=9, damage=18, source='repeater')
            game.projectiles.append(p1)
            game.projectiles.append(p2)
            self.cooldown = self.rate
    def draw(self, c):
        if not self.active: return
        hw, hh = self.cell_draw_size()
        c.create_rectangle(self.x-hw, self.y-hh, self.x+hw, self.y+hh, fill='#556B2F', outline='black')
        c.create_text(self.x, self.y, text='Rep', font=('Arial', max(8, int(hh*0.45)), 'bold'))
        self.draw_health(c)

class IceShooter(Plant):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.cooldown = 0
        self.rate = 80
    def update(self, game):
        if not self.active: return
        if self.cooldown > 0:
            self.cooldown -= 1
            return
        target = None
        for z in game.zombies:
            if z.row == self.row and z.x <= SPAWN_X and z.x > GRID_X:
                target = z
                break
        if target:
            p = Projectile(self.x + 30, self.y, speed=9, damage=18, effect='slow', slow_factor=0.5, slow_duration=120, source='iceshooter')
            game.projectiles.append(p)
            self.cooldown = self.rate
    def draw(self, c):
        if not self.active: return
        hw, hh = self.cell_draw_size()
        c.create_rectangle(self.x-hw, self.y-hh, self.x+hw, self.y+hh, fill='#ADD8E6', outline='black')
        c.create_text(self.x, self.y, text='Ice', font=('Arial', max(8, int(hh*0.45)), 'bold'))
        self.draw_health(c)

class Torchwood(Plant):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.health = 200
        self.max_health = self.health
    def update(self, game):
        if not self.active: return
        for pr in list(game.projectiles):
            if not (pr.active and abs(pr.x - self.x) < 40 and abs(pr.y - self.y) < 40):
                continue
            if getattr(pr, 'torch_boosted', False):
                continue
            pr.torch_boost = True
            if pr.source in ('peashooter', 'repeater'):
                pr.damage = max(1, pr.damage * 2.0)
                pr.torch_boosted = True
            elif pr.source == 'iceshooter' and getattr(pr, 'effect', None) == 'slow':
                pr.effect = None
                pr.slow_duration = 0
                pr.slow_factor = 1.0
                pr.torch_boosted = True
            
    def draw(self, c):
        if not self.active: return
        hw, hh = self.cell_draw_size()
        c.create_rectangle(self.x-hw, self.y-hh, self.x+hw, self.y+hh, fill='#FF6347', outline='black')
        c.create_text(self.x, self.y, text='Torch', font=('Arial', max(8, int(hh*0.45)), 'bold'))
        self.draw_health(c)

class CherryBomb(Plant):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.timer = 90
        self.health = 1
        self.max_health = 1
    def update(self, game):
        if not self.active: return
        self.timer -= 1
        if self.timer <= 0:
            for z in list(game.zombies):
                if z.active and math.hypot(z.x - self.x, z.y - self.y) < 100:
                    z.health -= 200000
                    if z.health <= 0:
                        z.active = False
            game.grid[self.row][self.col] = None
            self.active = False
    def draw(self, c):
        if not self.active: return
        hw, hh = self.cell_draw_size()
        ch_w = max(10, int(hw * 0.8))
        ch_h = max(10, int(hh * 0.8))
        c.create_oval(self.x-ch_w, self.y-ch_h, self.x+ch_w, self.y+ch_h, fill='red', outline='black')
        c.create_text(self.x, self.y, text='Boom', font=('Arial', max(8, int(hh*0.45)), 'bold'))

class WallNut(Plant):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.health = 350
        self.max_health = self.health
    def update(self, game):
        return
    def draw(self, c):
        if not self.active: return
        hw, hh = self.cell_draw_size()
        c.create_oval(self.x-hw, self.y-hh, self.x+hw, self.y+hh, fill='#DEB887', outline='black')
        c.create_text(self.x, self.y, text='Wall', font=('Arial', max(8, int(hh*0.6)), 'bold'))
        self.draw_health(c)

class TallNut(Plant):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.health = 500
        self.max_health = self.health
    def update(self, game):
        return
    def draw(self, c):
        if not self.active: return
        hw, hh = self.cell_draw_size()
        t_hw = max(hw, int(CELL_W * 0.45))
        t_hh = max(hh, int(CELL_H * 0.5))
        c.create_rectangle(self.x-t_hw, self.y-t_hh, self.x+t_hw, self.y+t_hh, fill='#A0522D', outline='black')
        c.create_text(self.x, self.y, text='Tall', font=('Arial', max(8, int(hh*0.45)), 'bold'))
        self.draw_health(c)

    @property
    def blocks_vault(self):
        return True

class PotatoMine(Plant):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.armed = False
        self.arm_timer = 150
        self.health = 1
        self.max_health = 1
    def update(self, game):
        if not self.active: return
        if not self.armed:
            self.arm_timer -= 1
            if self.arm_timer <= 0:
                self.armed = True
        if self.armed:
            for z in game.zombies:
                if z.row == self.row and z.active and math.hypot(z.x - self.x, z.y - self.y) < 50:
                    for z2 in list(game.zombies):
                        if math.hypot(z2.x - self.x, z2.y - self.y) < 120:
                            z2.health -= 250
                            if z2.health <= 0:
                                z2.active = False
                    game.grid[self.row][self.col] = None
                    self.active = False
                    return
    def draw(self, c):
        if not self.active: return
        hw, hh = self.cell_draw_size()
        pm_w = max(8, int(hw * 0.8))
        pm_h = max(6, int(hh * 0.5))
        color = '#FF0000' if self.armed else '#D2691E'
        c.create_oval(self.x-pm_w, self.y-pm_h, self.x+pm_w, self.y+pm_h, fill=color, outline='black')
        if self.armed:
            c.create_text(self.x, self.y - max(12, hh), text='Armed!', font=('Arial', max(8, int(hh*0.4)), 'bold'), fill='red')
        self.draw_health(c)

class Spikeweed(Plant):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.health = 60
        self.max_health = self.health
        self.indigestible = True
    def update(self, game):
        if not self.active: return
        for z in game.zombies:
            colpos = int((z.x - GRID_X) // CELL_W)
            if z.row == self.row and colpos == self.col and z.active:
                z.health -= 1
                if z.health <= 0:
                    z.active = False
    def draw(self, c):
        if not self.active: return
        hw, hh = self.cell_draw_size()
        sp_w = max(6, int(hw * 0.6))
        sp_h = max(6, int(hh * 0.6))
        c.create_polygon(self.x-sp_w, self.y+int(sp_h*0.6), self.x, self.y-int(sp_h*1.2), self.x+sp_w, self.y+int(sp_h*0.6), fill='#556B2F', outline='black')
        self.draw_health(c)

    @property
    def blocks_vault(self):
        return False

class Chomper(Plant):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.cooldown = 0
        self.rate = 100
        self.health = 180
        self.max_health = self.health
        self.bite_timer = 0
        self.bite_cooldown = 450
    def update(self, game):
        if not self.active: return
        if self.bite_timer > 0:
            self.bite_timer -= 1
            return
        for z in game.zombies:
            if z.row != self.row or not z.active:
                continue
            z_col = int((z.x - GRID_X) // CELL_W)
            if self.col < z_col <= self.col + 1.5:
                z.health = 0
                z.active = False
                self.bite_timer = self.bite_cooldown
                return
    def draw(self, c):
        if not self.active: return
        hw, hh = self.cell_draw_size()
        c.create_rectangle(self.x-int(hw*0.9), self.y-int(hh*0.9), self.x+int(hw*0.9), self.y+int(hh*0.9), fill='#9932CC', outline='black')
        c.create_text(self.x, self.y, text='Chomp', font=('Arial', max(8, int(hh*0.45)), 'bold'))
        self.draw_health(c)

class Zombie:
    def __init__(self, row):
        self.row = row
        self.x = SPAWN_X
        self.y = GRID_Y + row * CELL_H + CELL_H//2
        zscale = max(0.3, CELL_W / 100.0)
        self.vx = (-0.8 - random.random()*0.3) * zscale
        self.health = 150
        self.max_health = self.health
        self.active = True
        self.slow_timer = 0
        self.slow_factor = 1.0
        self.color = '#556B2F'
        self.type_name = 'Normal'
    def update(self, game):
        if not self.active: return
        col = int((self.x - GRID_X) // CELL_W)
        if 0 <= col < COLS:
            plant = game.grid[self.row][col]
            if plant and plant.active and abs(self.x - plant.x) < max(20, int(CELL_W * 0.3)):
                if not getattr(plant, 'indigestible', False):
                    plant.health -= 0.5
                    if plant.health <= 0:
                        plant.active = False
                    return
        if getattr(self, 'slow_timer', 0) > 0:
            eff = self.slow_factor
            self.color = '#66CCAD'
            self.slow_timer -= 1
            if self.slow_timer <= 0:
                self.slow_factor = 1.0
                self.color = '#556B2F'
        else:
            eff = 1.0
        self.x += self.vx * eff
        if self.x < GRID_X - 20:
            game.lost = True
    def draw(self, c):
        if not self.active: return
        zw = max(12, int(CELL_W * 0.24))
        zh = max(14, int(CELL_H * 0.32))
        c.create_rectangle(self.x-zw, self.y-zh, self.x+zw, self.y+zh, fill=getattr(self, 'color', '#556B2F'), outline='black')
        c.create_text(self.x, self.y, text=str(int(self.health)), fill='white', font=('Arial', max(6, int(zh*0.35)), 'bold'))
        pct = max(0, min(1.0, self.health / getattr(self, 'max_health', 100)))
        bw = max(24, int(CELL_W * 0.4))
        x1 = self.x - bw//2
        y1 = self.y - zh - max(6, int(CELL_H * 0.08))
        x2 = x1 + int(bw * pct)
        c.create_rectangle(x1, y1, x1 + bw, y1 + 6, fill='black')
        c.create_rectangle(x1, y1, x2, y1 + 6, fill='red', outline='')
        t = getattr(self, 'type_name', '')
        if t == 'Conehead':
            poly_w = max(8, int(zw * 0.9))
            poly_h = max(8, int(zh * 0.9))
            c.create_polygon(self.x-poly_w, self.y-zh, self.x+poly_w, self.y-zh, self.x, self.y-zh-poly_h, fill='#FFD27F', outline='black')
        elif t == 'Bucket':
            b_w = max(10, int(zw * 0.9))
            c.create_rectangle(self.x-b_w, self.y-zh-max(6, int(zh*0.5)), self.x+b_w, self.y-zh-max(2, int(zh*0.2)), fill='#444444', outline='black')
        elif t == 'PoleVault':
            c.create_line(self.x+int(zw*0.9), self.y+int(zh*0.4), self.x+int(zw*1.8), self.y-int(zh*0.9), fill='sienna', width=max(2, int(CELL_W*0.02)))
        elif t == 'Fast':
            c.create_line(self.x+int(zw*1.1), self.y-int(zh*0.1), self.x+int(zw*1.5), self.y-int(zh*0.2), fill='white')
        elif t == 'Stroller':
            c.create_oval(self.x-int(zw*1.25), self.y-int(zh*0.15), self.x-int(zw*0.8), self.y-int(zh*0.05), fill='black')

class FastZombie(Zombie):
    def __init__(self, row):
        super().__init__(row)
        zscale = max(0.3, CELL_W / 100.0)
        self.vx = (-1.4 - random.random()*0.3) * zscale
        self.health = 100
        self.max_health = self.health
        self.color = '#66CC66'
        self.type_name = 'Fast'

class ConeheadZombie(Zombie):
    def __init__(self, row):
        super().__init__(row)
        zscale = max(0.3, CELL_W / 100.0)
        self.vx = (-0.5 - random.random()*0.15) * zscale
        self.health = 230
        self.max_health = self.health
        self.color = '#C38B00'
        self.type_name = 'Conehead'

class BucketheadZombie(Zombie):
    def __init__(self, row):
        super().__init__(row)
        zscale = max(0.3, CELL_W / 100.0)
        self.vx = (-0.4 - random.random()*0.1) * zscale
        self.health = 350
        self.max_health = self.health
        self.color = '#6E7B8B'
        self.type_name = 'Bucket'

class PoleVaultZombie(Zombie):
    def __init__(self, row):
        super().__init__(row)
        zscale = max(0.3, CELL_W / 100.0)
        self.vx = (-1.0 - random.random()*0.2) * zscale
        self.health = 160
        self.max_health = self.health
        self.vaulted = False
        self.color = '#AAAA55'
        self.type_name = 'PoleVault'
    def update(self, game):
        if not self.active: return
        col = int((self.x - GRID_X) // CELL_W)
        if 0 <= col < COLS:
            plant = game.grid[self.row][col]
            if plant and plant.active and not self.vaulted and abs(self.x - plant.x) < max(20, int(CELL_W * 0.3)) and not getattr(plant, 'blocks_vault', False):
                self.x += CELL_W
                self.vaulted = True
                return
        if getattr(self, 'slow_timer', 0) > 0:
            eff = self.slow_factor
            self.slow_timer -= 1
            if self.slow_timer <= 0:
                self.slow_factor = 1.0
        else:
            eff = 1.0
        self.x += self.vx * eff
        if self.x < GRID_X - 20:
            game.lost = True

class StrollerZombie(Zombie):
    def __init__(self, row):
        super().__init__(row)
        zscale = max(0.3, CELL_W / 100.0)
        self.vx = (-0.4 - random.random()*0.05) * zscale
        self.health = 90
        self.max_health = self.health
        self.color = '#99AABB'
        self.type_name = 'Stroller'

class BruteZombie(Zombie):
    def __init__(self, row):
        super().__init__(row)
        zscale = max(0.3, CELL_W / 100.0)
        self.vx = (-0.3 - random.random()*0.05) * zscale
        self.health = 600
        self.max_health = self.health
        self.color = '#553333'
        self.type_name = 'Brute'

class ChargerZombie(Zombie):
    def __init__(self, row):
        super().__init__(row)
        zscale = max(0.3, CELL_W / 100.0)
        self.vx = (-0.9 - random.random()*0.2) * zscale
        self.health = 180
        self.max_health = self.health
        self.color = '#CC6666'
        self.type_name = 'Charger'
        self.charging = 0
        self.has_smashed = False
    def update(self, game):
        if not self.active: return
        col = int((self.x - GRID_X) // CELL_W)
        if 0 <= col < COLS:
            plant = game.grid[self.row][col]
            if plant and plant.active and not self.has_smashed and abs(self.x - plant.x) < max(24, int(CELL_W * 0.35)) and self.charging == 0:
                self.charging = 60
                zscale = max(0.3, CELL_W / 100.0)
                self.vx = -3.0 * zscale
        if self.charging > 0:
            self.charging -= 1
            if self.charging == 0 and not self.has_smashed:
                col = int((self.x - GRID_X) // CELL_W)
                if 0 <= col < COLS:
                    plant = game.grid[self.row][col]
                    if plant and plant.active:
                        plant.active = False
                        self.has_smashed = True
                        zscale = max(0.3, CELL_W / 100.0)
                        self.vx = (-0.18 - random.random()*0.04) * zscale
        if getattr(self, 'slow_timer', 0) > 0:
            eff = self.slow_factor
            self.slow_timer -= 1
            if self.slow_timer <= 0:
                self.slow_factor = 1.0
        else:
            eff = 1.0
        self.x += self.vx * eff
        if self.x < GRID_X - 20:
            game.lost = True

class Game:
    def __init__(self, root):
        self.root = root
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        globals()['SCREEN_W'] = sw
        globals()['SCREEN_H'] = sh
        self.canvas = tk.Canvas(root, width=SCREEN_W, height=SCREEN_H, bg='#87CEEB')
        self.canvas.pack(fill='both', expand=True)
        self.root.title('Plants vs Zombies - Minimal')

        self.grid = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.plant_type = 'sunflower'
        self.suns = []
        self.projectiles = []
        self.zombies = []
        self.card_regions = []
        self.button_regions = []
        self.score = 0
        self.sun_currency = 100
        self.spawn_timer = 0
        self.spawn_rate = 420
        self.lost = False
        self.won = False
        self.wave = 1
        self.ticks = 0

        self.root.bind('<Button-1>', self.on_click)
        self.root.bind('1', lambda e: self.select_plant('sunflower'))
        self.root.bind('2', lambda e: self.select_plant('peashooter'))
        self.root.bind('3', lambda e: self.select_plant('wallnut'))
        self.root.bind('4', lambda e: self.select_plant('cherry'))
        self.root.bind('5', lambda e: self.select_plant('repeater'))
        self.root.bind('6', lambda e: self.select_plant('iceshooter'))
        self.root.bind('7', lambda e: self.select_plant('torchwood'))
        self.root.bind('8', lambda e: self.select_plant('tallnut'))
        self.root.bind('9', lambda e: self.select_plant('potatomine'))
        self.root.bind('0', lambda e: self.select_plant('spikeweed'))
        self.root.bind('-', lambda e: self.select_plant('chomper'))
        self.root.bind('s', lambda e: self.toggle_shovel())
        self.root.bind('r', lambda e: self.restart())

        self.plant_cards = [
            ('1', 'Sunflower', 'sunflower', 50, 'Sun'),
            ('2', 'Peashooter', 'peashooter', 100, 'Pea'),
            ('3', 'WallNut', 'wallnut', 75, 'Wal'),
            ('4', 'CherryBomb', 'cherry', 150, 'Boom'),
            ('5', 'Repeater', 'repeater', 200,'Rep'),
            ('6', 'IceShooter', 'iceshooter', 125, 'Ice'),
            ('7', 'Torchwood', 'torchwood', 75, 'Torch'),
            ('8', 'TallNut', 'tallnut', 150, 'Tall'),
            ('9', 'PotatoMine', 'potatomine', 50, 'PM'),
            ('0', 'Spikeweed', 'spikeweed', 125, 'Spk'),
            ('-', 'Chomper', 'chomper', 200, 'Cho'),
        ]

        self.loop()
        self.recalc_layout(SCREEN_W, SCREEN_H)
        self.canvas.bind('<Configure>', self.on_resize)

    def on_resize(self, event):
        try:
            w = int(event.width)
            h = int(event.height)
        except Exception:
            w = SCREEN_W
            h = SCREEN_H
        self.recalc_layout(w, h)

    def recalc_layout(self, width, height):
        globals()['SCREEN_W'] = max(200, int(width))
        globals()['SCREEN_H'] = max(200, int(height))
        field_w = max(100, SCREEN_W - MENU_WIDTH - 2 * FIELD_GAP)
        field_h = max(100, SCREEN_H - 2 * FIELD_GAP)
        globals()['CELL_W'] = max(20, field_w // COLS)
        globals()['CELL_H'] = max(20, field_h // ROWS)
        globals()['GRID_X'] = MENU_WIDTH + FIELD_GAP
        globals()['GRID_Y'] = FIELD_GAP
        # CORREÇÃO: Ponto de spawn também recalculado sem o offset de +50 pixels externos
        globals()['SPAWN_X'] = GRID_X + COLS * CELL_W 
        try:
            self.canvas.config(width=SCREEN_W, height=SCREEN_H)
        except Exception:
            pass
        for r in range(ROWS):
            for c in range(COLS):
                p = self.grid[r][c]
                if p:
                    p.x = GRID_X + c * CELL_W + CELL_W // 2
                    p.y = GRID_Y + r * CELL_H + CELL_H // 2
        
        # CORREÇÃO: Reposiciona os zumbis ativos para as novas alturas das linhas caso a tela mude de tamanho
        if hasattr(self, 'zombies'):
            for z in self.zombies:
                z.y = GRID_Y + z.row * CELL_H + CELL_H // 2

    def select_plant(self, ptype):
        self.plant_type = ptype

    def toggle_shovel(self):
        if self.plant_type == 'shovel':
            self.plant_type = 'sunflower'
        else:
            self.plant_type = 'shovel'

    def on_click(self, event):
        for x1, y1, x2, y2, ptype in self.card_regions:
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                self.select_plant(ptype)
                return
        for x1, y1, x2, y2, action in self.button_regions:
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                if action == 'shovel':
                    self.select_plant('shovel')
                return
        for s in self.suns:
            if not s.collected and math.hypot(event.x - s.x, event.y - s.y) < s.radius + 6:
                s.collected = True
                self.sun_currency += s.value
                return
        if self.plant_type == 'shovel':
            col = (event.x - GRID_X) // CELL_W
            row = (event.y - GRID_Y) // CELL_H
            if not (0 <= col < COLS and 0 <= row < ROWS):
                return
            col = int(col); row = int(row)
            if self.grid[row][col] is not None:
                self.grid[row][col] = None
            return
        col = (event.x - GRID_X) // CELL_W
        row = (event.y - GRID_Y) // CELL_H
        if not (0 <= col < COLS and 0 <= row < ROWS):
            return
        col = int(col); row = int(row)
        if self.grid[row][col] is not None:
            return
        if self.plant_type == 'sunflower':
            cost = 50
        elif self.plant_type == 'peashooter':
            cost = 100
        elif self.plant_type == 'wallnut':
            cost = 75
        elif self.plant_type == 'cherry':
            cost = 150
        elif self.plant_type == 'repeater':
            cost = 200
        elif self.plant_type == 'iceshooter':
            cost = 125
        elif self.plant_type == 'torchwood':
            cost = 75
        elif self.plant_type == 'tallnut':
            cost = 150
        elif self.plant_type == 'potatomine':
            cost = 50
        elif self.plant_type == 'spikeweed':
            cost = 125
        elif self.plant_type == 'chomper':
            cost = 200
        else:
            cost = 100
        if self.sun_currency < cost:
            return
        self.sun_currency -= cost
        if self.plant_type == 'sunflower':
            p = Sunflower(row, col)
        elif self.plant_type == 'peashooter':
            p = Peashooter(row, col)
        elif self.plant_type == 'wallnut':
            p = WallNut(row, col)
        elif self.plant_type == 'cherry':
            p = CherryBomb(row, col)
        elif self.plant_type == 'repeater':
            p = Repeater(row, col)
        elif self.plant_type == 'iceshooter':
            p = IceShooter(row, col)
        elif self.plant_type == 'torchwood':
            p = Torchwood(row, col)
        elif self.plant_type == 'tallnut':
            p = TallNut(row, col)
        elif self.plant_type == 'potatomine':
            p = PotatoMine(row, col)
        elif self.plant_type == 'spikeweed':
            p = Spikeweed(row, col)
        elif self.plant_type == 'chomper':
            p = Chomper(row, col)
        else:
            p = Peashooter(row, col)
        self.grid[row][col] = p
        if self.plant_type == 'sunflower':
            self.suns.append(Sun(p.x, p.y - 20, value=15))

    def spawn_zombie(self):
        r = random.randrange(0, ROWS)
        difficulty = min(1.0, self.ticks / 6000.0)
        weights = {
            'Zombie': 30,
            'FastZombie': 18,
            'PoleVaultZombie': 8,
            'ConeheadZombie': 18,
            'BucketheadZombie': 10,
            'StrollerZombie': 8,
            'BruteZombie': 6,
            'ChargerZombie': 12,
        }
        weights['ConeheadZombie'] += int(difficulty * 20)
        weights['BucketheadZombie'] += int(difficulty * 30)
        weights['PoleVaultZombie'] += int(difficulty * 10)
        weights['BruteZombie'] += int(difficulty * 6)
        weights['ChargerZombie'] += int(difficulty * 10)
        choices = list(weights.keys())
        w = list(weights.values())
        pick = random.choices(choices, weights=w, k=1)[0]
        if pick == 'Zombie':
            z = Zombie(r)
        elif pick == 'FastZombie':
            z = FastZombie(r)
        elif pick == 'PoleVaultZombie':
            z = PoleVaultZombie(r)
        elif pick == 'ConeheadZombie':
            z = ConeheadZombie(r)
        elif pick == 'BucketheadZombie':
            z = BucketheadZombie(r)
        elif pick == 'StrollerZombie':
            z = StrollerZombie(r)
        elif pick == 'BruteZombie':
            z = BruteZombie(r)
        else:
            z = ChargerZombie(r)
        extra_from_wave = (self.wave-1) * 20
        extra_from_time = int(self.ticks / 600) * 10
        extra_from_minutes = (self.ticks // TICKS_PER_MIN) * 50
        z.health += extra_from_wave + extra_from_time
        z.health += extra_from_minutes
        z.max_health = getattr(z, 'max_health', z.health)
        self.zombies.append(z)

    def loop(self):
        self.ticks += 1
        if not self.lost and not self.won:
            for r in range(ROWS):
                for c in range(COLS):
                    p = self.grid[r][c]
                    if p:
                        p.update(self)
                        if not p.active:
                            self.grid[r][c] = None
            for s in list(self.suns):
                s.update()
                if s.collected:
                    self.suns.remove(s)
            for pr in list(self.projectiles):
                pr.update()
                if not pr.active:
                    self.projectiles.remove(pr)
            for z in list(self.zombies):
                z.update(self)
                if z.health <= 0:
                    z.active = False
                if not z.active:
                    try:
                        self.zombies.remove(z)
                        self.score += 10
                    except ValueError:
                        pass
            for pr in list(self.projectiles):
                for z in self.zombies:
                    if not z.active:
                        continue
                    thresh_x = max(16, int(CELL_W * 0.28))
                    thresh_y = max(12, int(CELL_H * 0.28))
                    if abs(pr.x - z.x) < thresh_x and abs(pr.y - z.y) < thresh_y:
                        z.health -= pr.damage
                        if pr.source == 'iceshooter':
                            z.color = '#48cbef'
                        if getattr(pr, 'effect', None) == 'slow':
                            z.slow_timer = max(getattr(z, 'slow_timer', 0), pr.slow_duration)
                            z.slow_factor = pr.slow_factor
                        pr.active = False
                        break
            self.spawn_timer += 1
            if self.spawn_timer >= self.spawn_rate:
                self.spawn_timer = 0
                self.spawn_zombie()
                if self.spawn_rate > 120:
                    self.spawn_rate -= 6
            if self.ticks > 0 and self.ticks % 1200 == 0 and self.spawn_rate > 60:
                self.spawn_rate = max(60, self.spawn_rate - 8)
            if self.ticks > 0 and self.ticks % TICKS_PER_MIN == 0:
                self.spawn_rate = max(40, self.spawn_rate - 40)
                self.wave += 1
            if random.random() < 0.004:
                sx = GRID_X + random.randint(0, COLS-1) * CELL_W + CELL_W//2
                sy = GRID_Y + random.randint(0, ROWS-1) * CELL_H + CELL_H//2 - 20
                self.suns.append(Sun(sx, sy, value=25))
            if self.score >= 300 * self.wave:
                self.won = True
        self.draw()
        self.root.after(16, self.loop)

    def draw_grid(self):
        for r in range(ROWS):
            for c in range(COLS):
                x1 = GRID_X + c*CELL_W
                y1 = GRID_Y + r*CELL_H
                x2 = x1 + CELL_W
                y2 = y1 + CELL_H
                self.canvas.create_rectangle(x1, y1, x2, y2, fill='#7CFC00', outline='darkgreen')

    def draw(self):
        self.canvas.delete('all')
        self.canvas.create_rectangle(0,0,SCREEN_W,SCREEN_H, fill='#87CEEB', outline='')
        self.canvas.create_rectangle(0,0,MENU_WIDTH,SCREEN_H, fill='#deb887', outline='black')
        self.canvas.create_text(20,10, text=f'Suns: {self.sun_currency}', anchor='nw', font=('Arial', 14, 'bold'))
        self.canvas.create_text(20,40, text=f'Score: {self.score}', anchor='nw', font=('Arial', 12))
        self.canvas.create_text(20,70, text=f'Plant: {self.plant_type}', anchor='nw', font=('Arial', 12))
        self.canvas.create_text(20,100, text=f'Wave: {self.wave}', anchor='nw', font=('Arial', 12))

        total = len(self.plant_cards)
        start_x = 10
        available_w = MENU_WIDTH - 20
        gap = 6
        card_w = min(126, available_w)
        card_h = 40
        y_top = 120
        self.card_regions = []
        self.button_regions = []

        visuals = {
            'sunflower': ('rect', '#9ACD32'),
            'peashooter': ('rect', '#3CB371'),
            'wallnut': ('oval', '#DEB887'),
            'cherry': ('oval', 'red'),
            'repeater': ('rect', '#556B2F'),
            'iceshooter': ('rect', '#ADD8E6'),
            'torchwood': ('rect', '#FF6347'),
            'tallnut': ('rect', '#A0522D'),
            'potatomine': ('oval', '#8B4513'),
            'spikeweed': ('poly', '#556B2F'),
            'chomper': ('rect', '#9932CC'),
        }

        for idx, (key, label, name, cost, abbrev) in enumerate(self.plant_cards):
            x = start_x
            y = y_top + idx * (card_h + gap)
            outline = 'gold' if self.plant_type == name else 'black'
            fill_bg = '#f8f8f8' if self.sun_currency >= cost else '#eee'
            self.canvas.create_rectangle(x, y, x + card_w, y + card_h, fill=fill_bg, outline=outline)
            self.card_regions.append((x, y, x + card_w, y + card_h, name))
            vis = visuals.get(name, ('rect', '#999999'))
            shape, color = vis
            cx = x + 14
            cy = y + card_h//2
            if shape == 'rect':
                self.canvas.create_rectangle(cx-10, cy-10, cx+10, cy+10, fill=color, outline='black')
            elif shape == 'oval':
                self.canvas.create_oval(cx-10, cy-8, cx+10, cy+8, fill=color, outline='black')
            elif shape == 'poly':
                self.canvas.create_polygon(cx-10, cy+6, cx, cy-8, cx+10, cy+6, fill=color, outline='black')
            self.canvas.create_text(x + 6, y + 6, text=key, anchor='nw', font=('Arial', 9, 'bold'))
            self.canvas.create_text(x + 32, y + card_h//2, text=label, anchor='w', font=('Arial', 8, 'bold'))
            self.canvas.create_text(x + card_w - 6, y + card_h//2, text=str(cost), anchor='e', font=('Arial', 9, 'bold'))

        button_x = start_x
        button_y = y_top + total * (card_h + gap) + gap
        button_h = 32
        button_w = card_w
        button_fill = '#f8f8f8' if self.plant_type != 'shovel' else '#ffe4b5'
        button_outline = 'gold' if self.plant_type == 'shovel' else 'black'
        self.canvas.create_rectangle(button_x, button_y, button_x + button_w, button_y + button_h, fill=button_fill, outline=button_outline)
        self.canvas.create_text(button_x + button_w/2, button_y + button_h/2, text='Shovel', font=('Arial', 9, 'bold'))
        self.button_regions.append((button_x, button_y, button_x + button_w, button_y + button_h, 'shovel'))

        hint_y = button_y + button_h + 8
        hint_y = min(hint_y, SCREEN_H - 20)

        self.draw_grid()
        for r in range(ROWS):
            for c in range(COLS):
                p = self.grid[r][c]
                if p:
                    p.draw(self.canvas)
        for s in self.suns:
            s.draw(self.canvas)
        for pr in self.projectiles:
            pr.draw(self.canvas)
        for z in self.zombies:
            z.draw(self.canvas)
        if self.lost:
            self.canvas.create_text(SCREEN_W//2, SCREEN_H//2, text='GAME OVER', font=('Arial', 32, 'bold'), fill='red')
            self.canvas.create_text(SCREEN_W//2, SCREEN_H//2+40, text="Press 'r' to restart", font=('Arial', 16))
        if self.won:
            self.canvas.create_text(SCREEN_W//2, SCREEN_H//2, text='YOU WIN', font=('Arial', 32, 'bold'), fill='green')
            self.canvas.create_text(SCREEN_W//2, SCREEN_H//2+40, text="Press 'r' to restart", font=('Arial', 16))

    def restart(self):
        self.grid = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.suns = []
        self.projectiles = []
        self.zombies = []
        self.score = 0
        self.sun_currency = 75
        self.spawn_timer = 0
        self.spawn_rate = 420
        self.lost = False
        self.won = False
        self.wave = 1
        self.ticks = 0

if __name__ == '__main__':
    root = tk.Tk()
    game = Game(root)
    root.mainloop()