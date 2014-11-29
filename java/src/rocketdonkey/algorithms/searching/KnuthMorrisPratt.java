package rocketdonkey.algorithms.searching;


/**
 * Knuth-Morris-Pratt search algorithm.
 * Search for the occurrence of a substring within a string, taking into
 * account already observed values.
 */
public class KnuthMorrisPratt {
  // The failure function for the input string.
  private int[] failure;
  // The word to find.
  private String targetWord;
  // The input sequence.
  private String inputString;

  public KnuthMorrisPratt(String targetWord, String inputString) {
    this.targetWord = targetWord;
    this.inputString = inputString;

    generateFailure(targetWord);
  };

  /**
   * Generate the failure function.
   * The failure function is an array that contains information regarding
   * previous observed values. In the case a match-in-progress fails, the table
   * can be used to backtrack to the nearest portion of the match that is a
   * prefix of the target string. This precludes having to inspect candidates
   * that have no chance of matching.
   * @param input The input string for which to construct the failure function.
   * @return The failure function - an array of integers.
   */
  private void generateFailure(String inputString) {
    // The first value will always be -1.
    failure = new int[inputString.length()];
    failure[0] = -1;
    String[] currentMatches = new String[inputString.length()];
    for (int index = 2; index < inputString.length(); ++index) {
      // The string fragment up to this point.
      String frag = inputString.substring(0, index);
      // Using the current substring, find the length of the longest possible
      // suffix which is also a prefix of the substring.
      int fragStart = failure[index-1];

      if (frag.charAt(fragStart) == frag.charAt(frag.length() - 1)) {
        ++fragStart;
        failure[index] = fragStart;
      } else {
        failure[index] = 0;
      }
    }
  };


  /**
   * Find the location of the first occurrence of 'word' in 'input'.
   * @return The integer representing the position of the first occurrence of
   *     'word' in 'input', or -1 if no match found.
   */
  private int findMatch() {
    int matchPosition = 0;
    int currentPosition = 0;

    int inputLen = inputString.length();
    int targetLen = targetWord.length();

    // Continue processing while the current position in input plus the
    // beginning of the current match is less than the length of the input.
    while (matchPosition + currentPosition < inputString.length()) {

      // Check if there is a match at the current position.
      if (targetWord.charAt(matchPosition) ==
            inputString.charAt(currentPosition + matchPosition)) {
        //  If the match position is equal to the length of the target word, it
        //  means we have found a complete match and can return.
        if (matchPosition == targetWord.length() - 1) {
          return currentPosition;
        }
        // Otherwise, increase the match position by one and continue checking.
        ++matchPosition;
      } else {
        // In the case there isn't a match, determine how far back we need to
        // backtrack.
        int failurePosition = failure[matchPosition];
        if (failurePosition > -1) {
          // Increase the current position in the input string to the current
          // match position minus how far back the table says we can backtrack.
          currentPosition += matchPosition - failurePosition;
          matchPosition = failurePosition;
        } else {
          // Otherwise, we haven't matched anything and can just move to the
          // next character.
          matchPosition = 0;
          ++currentPosition;
        }
      }
    }

    return -1;
  };

  /**
   * Return the calculated failure table (used for testing).
   * @return The failure function - an array of integers.
   */
  public int[] getFailure() {
    return failure;
  };

  /**
   * Execute the search.
   */
  public static int search(String word, String input) {
    KnuthMorrisPratt kmp = new KnuthMorrisPratt(word, input);
    kmp.generateFailure(word);
    return kmp.findMatch();
  }
}
