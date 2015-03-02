package eu.neurovertex.dndsimulator;

/**
 * @author Neurovertex
 *         Date: 26/02/15
 *         Time: 16:45
 */
public class Dice {
	private final int n, d, plus;

	public Dice(int n, int d, int plus) {
		this.n = n;
		this.d = d;
		this.plus = plus;
	}

	public static int roll(int n, int d, int plus) {
		int sum = plus;
		for (int i = 0; i < n; i++)
			sum += (int) (Math.random() * d) + 1;
		return sum;
	}

	public int roll() {
		return roll(n, d, plus);
	}

	@Override
	public String toString() {
		return String.format("Dice{%dd%d+%d}", n, d, plus);
	}

    public String getDescription() { return String.format("%dd%d+%d", n, d, plus); }
}
