package eu.neurovertex.dndsimulator;

import java.util.ArrayList;
import java.util.List;

/**
 * @author Neurovertex
 *         Date: 12/02/2015, 14:39
 */
public class Main {
	public static void main(String[] args) {
		List<Creature> team1 = new ArrayList<>(), team2 = new ArrayList<>();

		for (int i = 0; i < 5; i++)
			team1.add(new SimpleCreature("Human " + i, Dice.roll(1, 20, 10), Dice.roll(1, 6, 0), 3, SimpleWeapon.LongSword()));
        System.out.println("Created team :\n" + team1);

		for (int i = 0; i < 10; i++)
			team2.add(new SimpleCreature("Goblin " + i, Dice.roll(1, 10, 2), Dice.roll(1, 6, 0), 1));

		Simulator simulator = new Simulator(team1, team2);
		simulator.run();
	}
}
