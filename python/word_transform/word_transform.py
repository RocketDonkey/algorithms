"""Word Transform - change a word into another word.

Given a source word (s) of length n, convert it into target (t) (also of length
n), where each intermediate state is itself a valid word.

Example:
  Source: dog
  Target: cat
  Possible path: dog -> cog -> cot -> cat
"""

import collections
import sys
import time


WORD_SOURCE = '/usr/share/dict/words'


def GeneratePossibilities(word):
  """Given a word, generate a list of wildcard patterns from that word.

  Example: 'cat' -> ['*at', 'c*t', 'ca*']

  Args:
    word: The string word for which to generate the possibilities.

  Returns:
    A list of all patterns that can be achieved by 'wildcarding' one character
        at a time.
  """
  return ['%s*%s' % (word[:pos], word[pos+1:]) for pos in xrange(len(word))]


class WordNode(object):
  """A node representing a word and its 'links'.

  Args:
    word: The string word for which to create a WordNode.
    possibilities: A list of wildcard patterns that could match this word.
  """

  def __init__(self, word, possibilities):
    self.word = word
    self._map = {possibility: [] for possibility in possibilities}

  def __iter__(self):
    """Iterate through the keys of the WordNode's internal map."""
    return self._map.iterkeys()

  def __repr__(self):
    """Representation of a WordNode."""
    return '%s (%s)' % (self.__class__.__name__, self.word)

  def IterMatches(self):
    """Iterate through the internal map, return words matching each pattern.

    Returns:
      An iterator over the values of the internal map of wildcard patterns.
    """
    return self._map.itervalues()

  def AddMatches(self, word_key, matches):
    """Add a list of matches to the corresponding key for a WordNode.

    For example, a key of 'c*t' for the word 'cat' would match 'cot' and 'cut'.

    Args:
      word_key: The string wildcard pattern to which to add match_word.
      matches: The list of string word matches to add.
    """
    self._map[word_key].extend(matches)


class WordGraph(object):
  """A container for WordNodes."""

  def __init__(self, source, target):
    self._source = source
    self._target = target

    self._map = {}
    self._key_map = collections.defaultdict(list)

    # Generate the mapping of possible words.
    length = len(source)
    with open(WORD_SOURCE) as file_:
      for word in file_:
        word = word.strip()
        if len(word) == length:
          # For each word, find all possible matches, where a match is defined
          # as a pattern with a wildcard that with the proper substitution would
          # match the input word (e.g. '*at' and 'c*t' both match 'cat').
          possibilities = GeneratePossibilities(word)
          for possibility in possibilities:
            self._key_map[possibility].append(word)
          node = WordNode(word, possibilities)
          self._map[word] = node

    # For each word, create a WordNode and add it to the internal map. Then,
    # generate all possible 'legal' transformations for the word.
    for word, node in self._map.iteritems():
      for word_key in node:
        # For each wildcard pattern in the word, find all possible words.
        node.AddMatches(word_key, self._key_map[word_key])

  def FindPath(self):
    """Find a path from the source word to the target."""
    observed = set()
    queue = [[self._map[self._source]]]
    while queue:
      # Get the current path. This pops from the beginning, which gives priority
      # to the 'closest' matches.
      path = queue.pop(0)

      # Get the last node from the current path.
      node = path[-1]
      if node in observed:
        continue
      observed.add(node)

      # Return if we found a match.
      if node.word == self._target:
        return path

      # Otherwise, add all of the potential candidates for this node.
      for matches in node.IterMatches():
        for match in matches:
          new_path = list(path)
          new_path.append(self._map[match])
          queue.append(new_path)



def PrintExampleData():
  """Print a summary of example word transformations and their timings."""
  print 'Testing performance for word patterns of increasing length.\n'
  pairs = [
      ('at', 'to',),
      ('dog', 'cat',),
      ('cold', 'warm',),
      ('thing', 'items',),
      ('summer', 'winter',),
      ('longest', 'boredom',),
  ]
  GenerateTable([TimeRun(source, target) for source, target in pairs])


def GenerateTable(runs):
  """Generate a table summarizing the transformation.

  Args:
    runs: A list of lists of the form:
      [source, target, moves, time_to_generate, time_to_find]
  """
  print '+---------+---------+-------+-----------+-----------+'
  print '| Source  | Target  | Moves | Gen. Time | Find Time |'
  print '+---------+---------+-------+-----------+-----------+'

  for run in runs:
    # Ignore the full path when generating the table.
    run = [str(element) for element in run[:-1]]
    print '| {:7s} | {:7s} | {:5s} | {:9s} | {:9s} |'.format(*run)

  print '+---------+---------+-------+-----------+-----------+'


def TimeRun(source, target):
  """Attempt a transformation and return the results.

  Args:
    source: The source word.
    target: The target word.

  Returns:
    A tuple of the form:
        (source, target, len(path), graph_gen_time, path_gen_time, path)
  """
  # Generate the word graph.
  pattern_start = time.time()
  word_graph = WordGraph(source, target)
  pattern_time = '%f' % (time.time() - pattern_start)

  # Find the path.
  path_start = time.time()
  path = word_graph.FindPath()
  path_time = '%f' % (time.time() - path_start)


  if not path:
    path_time = 'No match'
    path = []
    path_len = 'N/A'
  else:
    # THe number of moves (length of the path - 1).
    path_len = len(path) - 1


  return (source, target, path_len, pattern_time, path_time, path)


def main():
  """Generate a path from a source word to a target word."""
  if len(sys.argv) == 1:
    PrintExampleData()
    sys.exit(0)
  elif len(sys.argv) != 3:
    print 'Usage: word_transform <source_word> <target_word>\n'
    sys.exit(1)

  # Calculate the path from the source word the the target word.
  source, target = sys.argv[1:]
  if len(source) != len(target):
    print 'Source and target words must be the same length!\n'
    sys.exit(1)

  print 'Transforming %s -> %s\n' % (source, target)
  results = TimeRun(source, target)
  GenerateTable([results])

  if results[-1]:
    print '\nPath:'
    for index, node in enumerate(results[-1]):
      print index, node.word


if __name__ == '__main__':
  main()
