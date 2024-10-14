from datetime import datetime


def dump(obj, label='dump', mode='a'):
    with open(f'__{label}.txt', mode) as out:
        def write(msg):
            out.write(f'{datetime.now():%M%S} {msg}\n')
        try:
            for k, v in sorted(vars(obj).items()):
                write(f'{k} = {v}')
        except Exception:
            write(f'{obj}')
