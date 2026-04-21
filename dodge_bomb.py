import os
import sys
import pygame as pg
import random
import time


WIDTH, HEIGHT = 1100, 650
DELTA = {pg.K_UP: (0, -5),
         pg.K_DOWN: (0, +5),
         pg.K_LEFT: (-5, 0),
         pg.K_RIGHT: (5, 0)
         }
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数で与えられたRectが画面外かを判定する関数
    引数：こうかとんRectまたは爆弾Rect
    戻り値：横方向、縦方向判定結果（True: 画面内, False: 画面外）
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate

def get_kk_imags(kk_img: pg.Surface) -> dict[tuple[int, int], pg.Surface]:
    """
    こうかとんの画像を辞書型で管理する関数
    引数：こうかとんの画像Surface
    戻り値：こうかとんの画像辞書
    """
    kk_flip = pg.transform.flip(kk_img, True, False) #反転画像の実装
    kk_dict = {
        ( 0, 0): pg.transform.rotozoom(kk_img, 0, 1.0),
        (+5,  0): pg.transform.rotozoom(kk_flip, 0, 1.0),
        (+5, -5): pg.transform.rotozoom(kk_flip, 45, 1.0),
        ( 0, -5): pg.transform.rotozoom(kk_flip, 90, 1.0),
        (-5, -5): pg.transform.rotozoom(kk_img, 315, 1.0),
        (-5,  0): pg.transform.rotozoom(kk_img, 0, 1.0),
        (-5, +5): pg.transform.rotozoom(kk_img, 45, 1.0),
        ( 0, +5): pg.transform.rotozoom(kk_flip, 270, 1.0),
        (+5, +5): pg.transform.rotozoom(kk_flip, 315, 1.0)
    }
    return kk_dict

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    爆弾のサイズと速度を変える関数
    引数：なし
    戻り値：爆弾の画像リスト、爆弾の速度リスト
    """
    bb_imgs = []
    bb_accs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        bb_img.set_colorkey((0, 0, 0))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_imgs.append(bb_img)
        bb_accs = [a for a in range(1, 11)]

    return bb_imgs, bb_accs

def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバーを表示する関数
    引数：画面Surface
    戻り値：なし
    """
    bg_Suf = pg.Surface((WIDTH, HEIGHT))
    bg_Suf.fill((0, 0, 0))
    bg_Suf.set_alpha(200)

    ft = pg.font.Font(None, 80)
    txt = ft.render("Game Over", True, (255, 225, 225))
    txt_rct = txt.get_rect(center=(WIDTH/2, HEIGHT/2))
    bg_Suf.blit(txt, txt_rct) # 2秒待機
    
    kk2_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 1.0)
    img2_rct = kk2_img.get_rect(center=(WIDTH/2, HEIGHT/2))
    bg_Suf.blit(kk2_img, (img2_rct.left+200, img2_rct.top))
    bg_Suf.blit(kk2_img, (img2_rct.left-200, img2_rct.top))

    screen.blit(bg_Suf, [0, 0])
    pg.display.update()
    time.sleep(5)
    return


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20)) #爆弾
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    # bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    bb_rct.width = bb_img.get_rect().width
    bb_rct.height = bb_img.get_rect().height
    vx, vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0
    bb_imgs, bb_accs = init_bb_imgs()
    kk_imgs = get_kk_imags(kk_img)
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            print("GAME OVER")
            return #GEME OVER
        screen.blit(bg_img, [0, 0]) 

        avx = vx*bb_accs[min(tmr//500, 9)]
        avy = vy*bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, mv in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += mv[0] #横
                sum_mv[1] += mv[1] #縦
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        kk_img = kk_imgs[tuple(sum_mv)]
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(avx, avy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1 
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
