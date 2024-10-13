import random, string, segno, tqdm, time

def password_generate(symbols_count: int, use_special_symbol: bool = False):
    """Генерация надёжного пароля для вашей социальной сети!"""
    if not use_special_symbol:
        psw = list(string.ascii_letters + string.digits)
        random.shuffle(psw)
        return ''.join(psw[:symbols_count])
    if use_special_symbol:
        psw = list(string.ascii_letters + string.digits)
        random.shuffle(psw)
        special_symbols = ['&', '!', '$', '%', '*', '@']
        return ''.join(psw[:symbols_count]) + random.choice(special_symbols)
    
def qr_create(content: str, name: str = 'name.png'):
    segno.make_qr(content).save(name=name, scale=10)

def progress_bar(obj: int):
    count = 0
    for _ in tqdm.tqdm(range(obj), 'Пожалуйста подождите, выполняются вычисления...', ncols=70, colour='#009FBD'):
        count += 1
        time.sleep(0.1)
    return count