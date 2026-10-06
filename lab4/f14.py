from tqdm import tqdm
import time

def run():
    print("14. tqdm progress:")
    for _ in tqdm(range(3)):
        time.sleep(0.1)