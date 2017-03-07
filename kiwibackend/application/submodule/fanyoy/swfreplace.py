# -*- coding: utf-8 -*-
"""
SwfReplacer:
  Flash の画像置き換えツール(PNG 置き換え対応版)
  必要ライブラリ: Python Imaging Library 1.1.6
"""
import sys
import struct
import zlib
from cStringIO import StringIO
from PIL import Image
from math import ceil

DEBUG = False

swf_tag_name_entry = {
    0:  'End',
    1:  'ShowFrame',
    2:  'DefineShape',
    6:  'DefineBitsJPEG',
    8:  'JPEGTables',
    9:  'SetBackgoundColor',
    11: 'DefineText',
    12: 'DoAction',
    20: 'DefineBitsLossLess',
    21: 'DefineBitsJPEG2',
    22: 'DefineShape2',
    26: 'PlaceObject2',
    32: 'DefineShape3',
    35: 'DefineBitsJPEG3',
    36: 'DefineBitsLossless2',
    37: 'DefineEditText',
    39: 'DefineSprite',
    43: 'FrameLabel',
    48: 'DefineFont2',
    88: 'DefineFontName',
}


def _h32(v):
    return struct.pack('<L', v)


def _h16(v):
    return struct.pack('<H', v)


def le2byte(s):
    "LittleEndian to 2 Byte"
    return struct.unpack('<H', s)[0]


def le4byte(s):
    "LittleEndian to 4 Byte"
    return struct.unpack('<L', s)[0]


def assert_bitslossless(b):
    if DEBUG:
        swf_tag = le2byte(b[:2])
        block_len = swf_tag & 0x3f
        if block_len == 0x3f:
            block_len = le4byte(b[2:6])
        swf_tag = swf_tag >> 6
        swf_tag_name = swf_tag_name_entry[swf_tag]
        assert swf_tag == 20 or swf_tag == 36
        image_id = le2byte(b[6:8])
        format = ord(b[8])
        width = le2byte(b[9:11])
        height = le2byte(b[11:13])
        colormap_count = ord(b[13])
        data = zlib.decompress(b[14:])
        print 'image_id', image_id
        print '\tswf_tag', swf_tag, swf_tag_name
        print '\tblock_len', block_len
        print '\tformat', format
        print '\twidht', width
        print '\theight', height
        print '\tcolormap_count', colormap_count
        print '\tdata', repr(data)

def compress(base_swf):
    "圧縮フラグが付いている場合は、圧縮する"
    header = base_swf[:8]
    tail   = base_swf[8:]
    if   header[:3] == 'FWS': # not compressed
        new_tail = tail
    elif header[:3] == 'CWS': # compressed
        new_tail = zlib.compress(tail)
    return header + new_tail

def decompress(base_swf):
    "圧縮フラグが付いている場合は、展開する"
    header = base_swf[:8]
    tail   = base_swf[8:]
    if   header[:3] == 'FWS': # not compressed
        new_tail = tail
    elif header[:3] == 'CWS': # compressed
        # tail を zlib 展開
        # See http://nakagami.blog.so-net.ne.jp/2010-02-26
        new_tail = zlib.decompress(tail)
    return header + new_tail

class Swf(object):
    def __init__(self, swf):
        self.swf = decompress(swf)
        self.swf_pos = 0
        self.parse_swf_head()
        self.parse_swfblocks()

    def parse_swf_head(self):
        "swf_header"
        self.magic = self.swf_read(3)
        self.version = ord(self.swf_read(1))
        self.file_length = le4byte(self.swf_read(4))

        "swf_header_movie"
        # twips 関連のヘッダは、今は飛ばす
        rectbits = ord(self.swf_read(1)) >> 3
        total_bytes = int(ceil((5 + rectbits * 4) / 8.0))
        self.swf_read(total_bytes - 1)

        # frame 関連
        self.frame_rate_decimal = ord(self.swf_read(1))
        self.frame_rate_integer = ord(self.swf_read(1))
        self.frame_count = le2byte(self.swf_read(2))

        # ヘッダー, twips, frame データを取っておく
        self.swf_head = self.swf[:self.swf_pos]

        if DEBUG:
            print "magic: %s\nver: %d\nlen: %d\n" \
                "frame_rate: %d.%d\ncount: %d\n" % ( \
                self.magic,
                self.version,
                self.file_length,
                self.frame_rate_integer,
                self.frame_rate_decimal,
                self.frame_count)

    def parse_swfblocks(self):
        "Parse/Split blocks."
        self.swf_blocks = []
        block = self.parse_swfblock()
        while block:
            self.swf_blocks.append(block)
            block = self.parse_swfblock()

        if DEBUG:
            for block in self.swf_blocks:
                print block['tag_name'], block['block_len']

    def replace_images(self, images):
        for block in self.swf_blocks:
            if block['tag'] in (20, 21, 36):
                image_id = le2byte(block['value'][6:8])
                if image_id in images:
                    if block['tag'] in (20, 36):   # DefineBitsLossless, DefineBitsLossless2
                        self.replace_lossless(block, images[image_id])
                    elif block['tag'] == 21:   # DefineBitsJPEG2
                        self.replace_jpeg(block, images[image_id])

    def replace_jpeg(self, block, image_data):
        """
        DefineBitsJPEG2 を置き換える関数
        1. SWF ヘッダーの length の置き換え
        2. tag block の書き換え
        """
        assert image_data[:2] == '\xff\xd8'   # JPEG SOI marker
        
        tag_raw = block['value'][:2]
        image_id = block['value'][6:8]

        # 1.
        old_length = block['block_len']
        new_length = len(image_data) + 2
        self.file_length += (new_length - old_length)

        # 2.
        block['block_len'] = new_length
        block['value'] = \
            tag_raw + \
            _h32(new_length) + \
            image_id + \
            image_data

    def replace_lossless(self, block, image_data):
        """
        画像を置き換える際に行うこと
        1. lossless データの置き換え
        2. ヘッダーの length の置き換え
        3. tag block での length の置き換え
        4. width, height, format データの置き換え
        """
        assert_bitslossless(block['value'])

        tag_raw = block['value'][:2]
        old_length = block['block_len']   # block['value'][2:6] と同じはず
        image_id = le2byte(block['value'][6:8])
        # format = ord(block['value'][8])

        # 1.
        g = Image2lossless(image_data, block['tag'])
        fv_read = g.convert()
        new_length = len(fv_read) + 7

        # 2.
        self.file_length += (new_length - old_length)

        # 3.
        block['block_len'] = new_length

        # 4.
        block['value'] = \
            tag_raw + \
            _h32(new_length) + \
            _h16(image_id) + \
            g.get_lossless_format() + \
            _h16(g.width()) + \
            _h16(g.height()) + \
            fv_read
        assert_bitslossless(block['value'])

    def parse_swfblock(self):
        swf_block_start = self.swf_pos
        swf_tag = le2byte(self.swf_read(2))
        block_len = swf_tag & 0x3f
        if block_len == 0x3f:
            block_len = le4byte(self.swf_read(4))
        swf_tag = swf_tag >> 6
        if swf_tag == 0:
            return None
        try:
            swf_tag_name = swf_tag_name_entry[swf_tag]
        except KeyError:
            swf_tag_name = "Unknown"

        ret = {}
        ret['block_start'] = swf_block_start
        ret['tag'] = swf_tag
        ret['block_len'] = block_len
        ret['tag_name'] = swf_tag_name
        self.swf_pos += block_len
        ret['value'] = self.swf[swf_block_start:self.swf_pos]
        return ret

    def swf_read(self, num):   # num byte(s) ずつ swf を読み出す
        self.swf_pos += num
        return self.swf[self.swf_pos - num: self.swf_pos]

    def writer(self, f):
        "swf 出力"
        # ヘッダー長を書き換え
        tmp_swf_data_list = []
        fl = _h32(self.file_length)
        self.swf_head = self.swf_head[:4] + fl + self.swf_head[8:]
        tmp_swf_data_list.append(self.swf_head)
        for block in self.swf_blocks:
            tmp_swf_data_list.append(block['value'])
        tmp_swf_data_list.append('\00\00')
        tmp_swf_data = ''.join(tmp_swf_data_list)
        new_swf = compress(tmp_swf_data)
        f.write(new_swf)


class Image2lossless(object):
    def __init__(self, image_data, tag):
        """
        GIF/PNG 形式から Flash 独自フォーマット
        lossless(2) 形式に変換する

        GIF/PNG での Palette モードの場合
            [transparency に何もセットされていないとき]
            Palette  ->  DefineBitsLossless   format 3

            [transparency がセットされている場合]
                     ->  DefineBitsLossless2  format 3

        PNG で頻繁に用いられる RGB, RGBA モードの場合
            RGB      ->  DefineBitsLossless   format 5
            RGBA     ->  DefineBitsLossless2  format 5
        """
        self.image = Image.open(StringIO(image_data))
        self.tag = tag

    def get_lossless_format(self):
        if self.image.mode == 'P':
            return chr(3)
        elif self.image.mode in ('RGB', 'RGBA'):
            return chr(5)

    def width(self):
        return self.image.size[0]

    def height(self):
        return self.image.size[1]

    def alex_width(self):
        return alex_width(self.image.size[0])

    def colormap_count(self):
        if self.image.mode == 'P':
            """
            パレットの場合、色数を返す
            （ただし 0 から数えるので - 1 する）

            3 で割っているのはパレット形式の場合、
            パレット中に RGB 順で色が並ぶと仮定してるため
            """
            return chr(len(self.image.palette.palette) / 3 - 1)
        else:
            return ""   # Otherwise absent

    def convert(self):
        if self.image.mode == 'P':
            return self.convert_palette()
        elif self.image.mode in ('RGB', 'RGBA'):
            return self.convert_rgb()

    def convert_rgb(self):
        """
        RGB/RGBA 形式の画像を lossless(2) に変換する
        基本的に PNG のみ
        """
        def rgba2argb(l):
            # RGBA で並んでいる列を ARGB に直す
            a = l[3]
            r, g, b = l[0] * a / 255, l[1] * a / 255, l[2] * a / 255
            return chr(a) + chr(r) + chr(g) + chr(b)

        indices = ""
        if self.tag == 20:   # DefineBitsLossless
            for tpl in list(self.image.getdata()):
                # tpl は (23, 136, 244).  PIX24 format
                indices += ('\xff' +
                            ''.join(map(lambda c: chr(c), tpl[:3])))

        elif self.tag == 36:   # DefineBitsLossless2
            for tpl in list(self.image.getdata()):
                # 置き換え先の画像も透明値を持つ事が前提
                assert len(tpl) == 4   # R,G,B,A
                indices += rgba2argb(tpl)

        return self.colormap_count() + zlib.compress(indices)

    def convert_palette(self):
        """
        パレット形式の GIF/PNG 画像を lossless(2) に変換する
        基本的には、GIF、PNG で差異は存在しない
        """
        palette = pack(map(lambda c: ord(c), self.image.palette.palette), 3)

        """
        colormap を定義する
        DefineBitsLossless なら PIL の palette が使えるが
        DefineBitsLossless2 だと、Alpha の値を加える必要がある
        """
        if self.tag == 20:   # DefineBitsLossless
            colormap = self.image.palette.palette
        elif self.tag == 36:  # DefineBitsLossless2
            if 'transparency' in self.image.info:
                transparency = int(self.image.info['transparency'])
            else:
                transparency = 65535
            colormap = ""
            for i, c in enumerate(palette):
                if i == transparency:
                    colormap += ''.join(map(lambda c: chr(c), [0, 0, 0, 0]))
                else:
                    colormap += ''.join(map(lambda c: chr(c), c + [255]))

        """
        実際の indices とくっつける
        もし横幅が alex_width（4 の倍数）でなければ
        画像を 4 の倍数に調節する
        """
        raw_indices = ''.join(
            map(lambda c: chr(c), list(self.image.getdata())))

        if self.width() != alex_width(self.width()):
            indices = adjust_palette_data(raw_indices, self.width())
        else:
            indices = raw_indices

        return self.colormap_count() + zlib.compress(colormap + indices)


def alex_width(num):
    return (num + 3) & -4


def adjust_palette_data(data, width):
    """
    Flash の画像の大きさについては
    width が 4 の倍数でなければならない
    indices をそのようにあわせる
    """
    new_data = ""
    gap = alex_width(width) - width
    for i in range(0, len(data), width):
        new_data += data[i:(i + width)] + '\0' * gap
    return new_data


def pack(l, num):
    ret = []
    for i in range(len(l) / num):
        ret.append(l[i * num: (i + 1) * num])
    return ret


if __name__ == '__main__':
    if len(sys.argv) == 2:
        swf = Swf(swf=open(sys.argv[1]).read())
    else:
        # Test
        replace_images = {}
        replace_images[4] = open('test/dummy_card/01.gif').read()
        replace_images[6] = open('test/dummy_card/03.gif').read()
        replace_images[8] = open('test/dummy_card/02.png').read()
        replace_images[10] = open('test/dummy_card/04.gif').read()
        replace_images[12] = open('test/dummy_card/05.gif').read()
        replace_images[14] = open('test/dummy_card/06.gif').read()
        replace_images[16] = open('test/dummy_card/07.png').read()
        replace_images[18] = open('test/dummy_card/08.gif').read()
        replace_images[20] = open('test/dummy_card/09.gif').read()
        replace_images[22] = open('test/dummy_card/10.gif').read()

        swf = Swf(swf=open('test/card_battle.swf').read())
        # swf = Swf(swf = open('test/card_battle_alpha.swf').read())

        swf.replace_images(replace_images)
        swf.writer(open('test/card_battle_out.swf', 'wb'))
