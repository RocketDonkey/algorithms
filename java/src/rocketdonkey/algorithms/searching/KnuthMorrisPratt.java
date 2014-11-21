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
  private String word;
  // The input sequence.
  private String input;

  public KnuthMorrisPratt(String word, String input) {
    generateFailure(input);
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
  private void generateFailure(String input) {
    // The first value will always be -1.
    failure = new int[input.length()];
    failure[0] = -1;
    String[] currentMatches = new String[input.length()];
    for (int index = 2; index < input.length(); ++index) {
      // The string fragment up to this point.
      String frag = input.substring(0, index);
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
    kmp.generateFailure(input);
    return 0;
  }
}
