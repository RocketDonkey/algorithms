package rocketdonkey.algorithms.sorting;

import org.junit.runner.JUnitCore;
import org.junit.runner.Result;
import org.junit.runner.notification.Failure;


/**
 * Test runner for Java sorting algorithms.
 * To run: To run this, go to the classes/
 *   1. Go to the classes/ directory.
 *   2. Run javac -d ./ ../src/rocketdonkey/algorithms/sorting/*.java.
 *   3. Run java rocketdonkey.algorithms.sorting.TestRunner.
 */
public class TestRunner {
  public static void main(String[] args) {
    Result result = JUnitCore.runClasses(QuicksortTest.class);
    for (Failure failure : result.getFailures()) {
      System.out.println(failure.toString());
    }
  };
};
