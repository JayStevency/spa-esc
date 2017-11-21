"""
:style:
[
    (style name, {
        keyword list
    }),

    ...
]

:big category:
{
    big category: (
        default,
        category list
    ),

    ...
}

:category:
[
    (category name, {
        keyword list
    }),

    ...
]

"""

STYLE = [
    ('normal', {
        'regular', '레귤러',
        'normal', '노말',
        'default', '기본',
    }),
    ('slim', {
        'slim', '슬림',
        'tight', '타이트',
    }),
    ('wide', {
        'over fit', 'overfit', '오버핏', '오버사이즈', 'oversize', 'over size',
        'wide', '와이드',
        'loose', '루즈',
        '가오리',
    }),
    ('skinny', {
        'skinny', '스키니',
    }),
]

BIG_CATEGORY = {
    'top': (
        'sweat_shirts',
        {'sweater', 'sweat_shirts', 't_shirts', 'shirts', 'sleeveless', 'swimwear'}
    ),
    'bottom': (
        'pants',
        {'pants', 'skirt', 'leggings'}
    ),
    'onepiece': (
        'onepiece',
        {'onepiece', 'dress', 'jumpsuit', 'bodysuit'}
    ),
    'outer': (
        'jacket',
        {'robe', 'vest', 'cardigan', 'jumper', 'jacket', 'coat', 'parka'}
    ),
}

CATEGORY = [
    ('t_shirts', {
        '티셔츠', '티 ', '팔티', 't-shirt', 'tee',
        '피케', 'pk티', 'pk shirt', 'pk t-shirt', 'pk t',
        '폴로셔츠', '럭비 셔츠', 't(반팔)', 't(긴팔)', '넥t'
    }),
    ('sweater', {
        '스웨터', 'sweater',
    }),
    ('sweat_shirts', {
        '스웨트 셔츠', '스웨트셔츠', '스웨셔츠', '스웨 셔츠', '스웻셔츠', '스웻 셔츠', 'sweat', 'sweatshirt', 'sweat shirt',
        '맨투맨', 'mtm',
        '풀오버', 'pullover',
        '후드', '후디', '후드티', 'hood', 'hoodie',
    }),
    ('shirts', {
        '셔츠', '남방', 'shirt',
        '블라우스', 'blouse', ' bl ',
    }),
    ('sleeveless', {
        '슬리브리스', 'sleeveless',
        '뷔스티에', 'bustier',
        '슬립', 'slip',
        '캐미솔', 'camisole',
        '탱크탑', 'tank top', 'tanktop',
    }),
    ('swimwear', {
        '스윔웨어', '래시가드', 'swim wear', 'swimwear',
        '스윔수트', 'swimsuit'
    }),
    ('pants', {
        '팬츠', '바지', 'pant', 'trouser',
        '진 ', '청바지', '데님팬츠', 'jean',
        '쇼트팬츠', '쇼츠', '쇼트 팬츠', 'short',
        '슬랙스', 'slacks', '치노', '진'
    }),
    ('skirt', {
        '스커트', '치마', 'skirt', 'apron', 'skt'
    }),
    ('leggings', {
        '레깅스', 'leggings', '타이즈',
    }),
    ('onepiece', {
        '원피스', 'onepiece', 'one piece', ' ops ', ' op ',
    }),
    ('dress', {
        '드레스', 'dress',
    }),
    ('jumpsuit', {
        '롬퍼', 'romper',
        '점프수트', 'jump', 'jumpsuit', 'jump suit',
    }),
    ('bodysuit', {
        '바디수트', 'bodysuit'
    }),
    ('robe', {
        '로브', 'robe',
    }),
    ('vest', {
        '베스트', '조끼', 'vest',
    }),
    ('cardigan', {
        '가디건', '카디건', 'cardigan',
    }),
    ('jumper', {
        '점퍼', '점퍼형', 'jumper', ' jp ',
        '스카잔', 'shirket',
        '바람막이', '윈드브레이커', 'windbreaker',
        '블루종', 'blouson',
    }),
    ('pajama', {
        '파자마'
    }),
    ('jacket', {
        '재킷', '자켓', '재킷형', '자켓형', 'jacket', 'jackets', 'anorak', ' jk ',
        '보머', '봄버', 'bomber',
        '트러커', 'trucker',
        '블레이저', 'blazer',
        '무스탕', 'mustang',
        '야상', '피재킷', '데님자켓',
        '수트', 'suit'
    }),
    ('coat', {
        '코트', '코트형', ' coat', 'coat ', 'coats', ' ct ',
        '바바리', 'bby',
    }),
    ('parka', {
        '파카', 'parka',
    }),
    ('belt', {
        '벨트', 'belt'
    }),
    ('underwear', {
        '바디쉐이프', '팬티', '브라', '드로즈', '트렁크스', '복서브리프', '힙허거', '쇼츠'    }),
    ('socks', {
        'socks', '삭스', '양말'
    })
]
