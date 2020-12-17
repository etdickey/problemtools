import java.util.*;

public class estimating {
    public static void main(String args[]) {
        Scanner input = new Scanner(System.in);

        while (input.hasNextDouble()) {
            double r = input.nextDouble();
            int n = input.nextInt(), c = input.nextInt();

            if (r == 0.0 && n == 0 && c == 0) break;

            double truth = Math.PI * r * r;
            double est = c * 4.0 * r * r / n;
            System.out.println(truth + " " + est);
        }
    }
}
