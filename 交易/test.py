RAW_DATA = ['./PTB/ptb.train.txt', './PTB/ptb.test.txt', './PTB/ptb.valid.txt']
OUTPUT_DATA = ['./PTB/ptb.train', './PTB/ptb.test', './PTB/ptb.valid']
for raw, output in zip(RAW_DATA, OUTPUT_DATA):
    print(raw)
    print(output)