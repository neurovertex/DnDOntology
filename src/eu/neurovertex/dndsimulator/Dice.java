package eu.neurovertex.dndsimulator;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * @author Neurovertex
 *         Date: 26/02/15
 *         Time: 16:45
 */
public class Dice {
	private static final Pattern DICEPATTERN = Pattern.compile(".*(?<!\\d)(\\d+) ?d ?(\\d+)(.\\d+)?.*");
	private final int n, d, plus;

	public Dice(int n, int d, int plus) {
		this.n = n;
		this.d = d;
		this.plus = plus;
	}

	public static Dice parse(String in) {
		Matcher m = DICEPATTERN.matcher(in);
		if (m.matches())
			try {
				int n = Integer.parseInt(m.group(1)),
						d = Integer.parseInt(m.group(2)), p;
				if (m.group(3) != null)
					p = Integer.parseInt(m.group(3));
				else
					p = 0;
				return new Dice(n, d, p);
			} catch (Exception e) {
				e.printStackTrace();
			}
		System.err.println("Error parsing : " + in);
		return null;
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
		return String.format("%dd%d%s", n, d, plus == 0 ? "" : (plus > 0 ? " +" : " ") + plus);
	}

    public String getDescription() { return String.format("%dd%d+%d", n, d, plus); }

	public int getNumber() {
		return n;
	}

	public int getFaces() {
		return d;
	}

	public int getAdded() {
		return plus;
	}
}
