import argparse
import random
import re

class Markov:
  start_words = []
  chain = {}

  def __init__(self, file):
    try:
      self.file = open(file, 'r')
    except FileNotFoundError:
      print('Error: file not found')

  def parse(self):
    pattern = re.compile('[\W_]+')
    for line in self.file:
      sentences = line.split('.')
      for s in sentences:
        words = [pattern.sub('', word).strip() for word in s.split(' ')]
        self.start_words.append(words[0])

        for i in range(len(words)-1):
          cur_word = words[i].lower()
          nxt_word = words[i+1].lower()
          if cur_word in self.chain:
            self.chain[cur_word].append(nxt_word)
          else:
            self.chain[cur_word] = [nxt_word]
    pass

  def gen(self, n):
    output = [random.choice(self.start_words)]
    cur_word = output[0].lower()
    for i in range(n):
      try:
        nxt_word = random.choice(self.chain[cur_word])
      except KeyError:
        nxt_word = random.choice(self.start_words)
      output.append(nxt_word)
      cur_word = nxt_word.lower()
    return ' '.join(output)

if __name__ == '__main__':
  arg_parser = argparse.ArgumentParser(description='A simple python Markov text generator.')
  arg_parser.add_argument('file', type=str, help='file to generate markov chain from')
  arg_parser.add_argument(
    '--n',
    type=int,
    default=50,
    metavar='num_words',
    help='integer value which determines how many words the text generator outputs. Has a default value of 50.')
  args = arg_parser.parse_args()
  markov = Markov(args.file)
  markov.parse()
  print(markov.gen(args.n))
