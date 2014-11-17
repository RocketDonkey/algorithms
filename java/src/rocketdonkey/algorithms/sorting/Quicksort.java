package rocketdonkey.algorithms.sorting;


/**
 * Quicksort implementation.
 *
 * Quicksort is a divide-and-conquer algorithm. Quicksort divides the input
 * into two pieces, sorts them and then joins them back together.
 *
 * Basic idea:
 *   1. Pick a pivot.
 *   2. Reorder so that all elements less than the pivot are before it, and all
 *      items greater than the pivot are after it.
 *   3. Recursively do this to the arrays on either side of the pivot.
 *
 * Average complexity: O(n log n)
 */
public class Quicksort {

  // Internal store for the values to sort.
  private int[] values;

  /**
   * Apply the Quicksort algorithm to an array of values.
   * @param input An array of integers to sort.
   */
  public void sort(int[] input) {
    // If the input is empty, just return.
    if (input == null || input.length == 0) {
      return;
    }
    this.values = input;
    // The initial input will be from 0 to the length of the array.
    quicksort(0, input.length - 1);
  }

  private void quicksort(int low, int high) {
    // Pick a pivot value. As these inputs are index values into the underlying
    // array, for an array [2, 5, 3, 6, 1], finding the middle value with input
    // indices (2, 4) would be:
    //   1. Subtract the low value from the high value (this gets the range
    //   between the two index values).
    //   2. Divide it by two to get a 'normalized' midpoint (which will be used
    //   as an offset in the next step).
    //   3. Add the offset to the original 'low' value to get the true position
    //   in the complete array.
    int pivot = this.values[low + (high-low) / 2];

    // These are the markers that will be advanced. When the recursive call is
    // done, these markers and the initial function call arguments will be used
    // to determine the next subarray to process.
    int lowIndex = low;
    int highIndex = high;

    // When swapping, we need to know that we can 'safely' swap the two,
    // because we don't want to swap two items where both items should actually
    // be on the same side of the pivot.
    while (lowIndex <= highIndex) {
      // Move up the 'low' number while it is still less than the pivot.
      while (this.values[lowIndex] < pivot) {
        ++lowIndex;
      }

      // Similarly, reduce the 'high' number while it is still greater than the
      // pivot.
      while (this.values[highIndex] > pivot) {
        --highIndex;
      }

      // Now swap the values around if necessary.
      if (lowIndex <= highIndex) {
        swapValues(lowIndex, highIndex);
        ++lowIndex;
        --highIndex;
      }
    }

    // Now recursively sort the subarrays. For each subarray, we want
    // everything from the lower bound up to the pivot or pivot up to the
    // higher bound, but only the index has moved (otherwise, we are done
    // sorting that subarray).
    if (low < highIndex) {
      quicksort(low, highIndex);
    }
    if (lowIndex < high) {
      quicksort(lowIndex, high);
    }
  }

  private void swapValues(int low, int high) {
    int tmp = this.values[low];
    this.values[low] = this.values[high];
    this.values[high] = tmp;
  }
};
