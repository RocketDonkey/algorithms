package rocketdonkey.algorithms.sorting;

import java.util.Arrays;

import org.junit.Test;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;


/**
 * Tests for Quicksort algorithm.
 */
public class QuicksortTest {

  @Test
  public void testEmptyArray() {
    Quicksort qs = new Quicksort();
    qs.sort(null);
  }

  @Test
  public void testSingleElement() {
    int[] input = {1};

    Quicksort qs = new Quicksort();
    qs.sort(input);
    assertTrue(input[0] == 1);
  }

  @Test
  public void testBasicSort() {
    int[] input = {1, 4, 5, 2, 6, 7};

    Quicksort qs = new Quicksort();
    qs.sort(input);
    if (!isSorted(input)) {
      fail("Input not sorted: " + Arrays.toString(input));
    }
  }

  private boolean isSorted(int[] values) {
    for (int i = 0; i < values.length - 1; ++i) {
      if (values[i] > values[i+1]) {
        return false;
      }
    }
    return true;
  }
}
