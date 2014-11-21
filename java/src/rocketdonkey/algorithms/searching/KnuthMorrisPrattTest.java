package rocketdonkey.algorithms.searching;

import java.util.HashMap;
import java.util.Map;

import org.junit.Test;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertArrayEquals;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;

/**
 * Tests of KMP algorithm.
 */
public class KnuthMorrisPrattTest {

  @Test
  public void testGenerateTable() {
    HashMap<String, int[]> tables = new HashMap<String, int[]>();
    tables.put("ABAB", new int[]{-1, 0, 0, 1});
    tables.put("ABABAC", new int[]{-1, 0, 0, 1, 2, 3});
    tables.put("ABCDABD", new int[]{-1, 0, 0, 0, 0, 1, 2});
    tables.put("ABABABC", new int[]{-1, 0, 0, 1, 2, 3, 4});
    tables.put("BANANA", new int[]{-1, 0, 0, 0, 0, 0});
    tables.put(
        "PARTICIPATE IN PARACHUTE",
        // Hopefully I'll learn better ways to format this...
        new int[]{
          -1, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0,
          0, 0, 0, 0, 1, 2, 3, 0, 0, 0, 0, 0}
    );

    for (Map.Entry<String, int[]> pair : tables.entrySet()) {
      KnuthMorrisPratt kmp = new KnuthMorrisPratt("", pair.getKey());
      assertArrayEquals(pair.getValue(), kmp.getFailure());
    }
  }
}
