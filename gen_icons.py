#!/usr/bin/env python3
"""Gera ícones PNG para o PWA da Biblioteca Maria Clara usando apenas stdlib."""
import struct, zlib, os, math

def make_png(size):
    """Cria um PNG de tamanho `size`x`size` com o ícone de livro desenhado pixel a pixel."""
    w = h = size
    # Fundo: azul escuro #0b2545
    bg = (11, 37, 69)
    # Livro: branco/creme
    book_body = (240, 235, 210)
    # Lombada: dourado
    spine = (212, 160, 23)
    # Linhas do texto: azul médio
    lines = (90, 140, 190)
    # Brilho das páginas
    page_edge = (255, 252, 240)

    pixels = []
    cx, cy = w / 2, h / 2

    # Margens do livro (40% a 90% do tamanho)
    pad = size * 0.12
    bx1 = int(pad)
    bx2 = int(w - pad)
    by1 = int(h * 0.10)
    by2 = int(h * 0.90)
    spine_w = max(2, int((bx2 - bx1) * 0.12))

    for y in range(h):
        row = []
        for x in range(w):
            # Fundo com gradiente sutil
            t = y / h
            r = int(bg[0] * (1 - t * 0.3))
            g = int(bg[1] * (1 - t * 0.2))
            b = int(bg[2] * (1 - t * 0.1))
            color = (r, g, b, 255)

            in_book = bx1 <= x < bx2 and by1 <= y < by2

            if in_book:
                # Lombada (esquerda do livro)
                if x < bx1 + spine_w:
                    color = (*spine, 255)
                else:
                    # Corpo do livro
                    color = (*book_body, 255)

                    # Linhas simulando texto (só no miolo)
                    inner_x1 = bx1 + spine_w + max(2, size // 16)
                    inner_x2 = bx2 - max(2, size // 16)
                    inner_y1 = by1 + max(3, size // 10)
                    inner_y2 = by2 - max(3, size // 12)
                    line_h = max(1, size // 20)
                    line_gap = max(2, size // 12)

                    if inner_x1 <= x <= inner_x2 and inner_y1 <= y <= inner_y2:
                        rel_y = y - inner_y1
                        cycle = line_h + line_gap
                        if rel_y % cycle < line_h:
                            # Linhas mais curtas no final (simulando parágrafo)
                            last_line = (inner_y2 - inner_y1) // cycle
                            line_num = rel_y // cycle
                            if line_num == last_line:
                                if x <= inner_x1 + (inner_x2 - inner_x1) * 0.55:
                                    color = (*lines, 255)
                            else:
                                color = (*lines, 255)

                # Borda direita do livro (páginas)
                if x >= bx2 - max(1, size // 40):
                    color = (*page_edge, 255)
                # Borda topo e base
                if y == by1 or y == by2 - 1:
                    color = (*page_edge, 255)

            # Sombra sob o livro
            shadow_y = by2
            shadow_h = max(2, size // 20)
            if shadow_y <= y < shadow_y + shadow_h and bx1 + spine_w <= x < bx2:
                alpha = int(120 * (1 - (y - shadow_y) / shadow_h))
                color = (0, 0, 0, alpha)

            row.extend(color)
        pixels.append(bytes(row))

    def pack_chunk(chunk_type, data):
        c = chunk_type + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)

    raw = b''
    for row in pixels:
        raw += b'\x00' + row  # filter type None

    compressed = zlib.compress(raw, 9)

    png = b'\x89PNG\r\n\x1a\n'
    png += pack_chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0))
    png += pack_chunk(b'IDAT', compressed)
    png += pack_chunk(b'IEND', b'')
    return png


sizes = [72, 96, 128, 144, 152, 192, 384, 512]
os.makedirs('icons', exist_ok=True)
for s in sizes:
    data = make_png(s)
    path = f'icons/icon-{s}.png'
    with open(path, 'wb') as f:
        f.write(data)
    print(f'  ✅ {path} ({len(data)} bytes)')

# Também gera o favicon.ico (32x32)
ico_data = make_png(32)
with open('favicon.png', 'wb') as f:
    f.write(ico_data)
print('  ✅ favicon.png (32x32)')

print('\nTodos os ícones gerados com sucesso!')
