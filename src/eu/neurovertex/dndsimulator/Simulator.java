package eu.neurovertex.dndsimulator;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Iterator;
import java.util.List;
import java.util.function.Predicate;

/**
 * @author Neurovertex
 *         Date: 26/02/15
 *         Time: 16:20
 */
public class Simulator implements Runnable {
	private List<Creature> team1, team2;

	public Simulator(List<Creature> team1, List<Creature> team2) {
		this.team1 = team1;
		this.team2 = team2;
	}

	@Override
	public void run() {
		List<List<TeamCreature>> creatures = getTeamCreatures();
		List<Creature> team1 = new ArrayList<>(this.team1), team2 = new ArrayList<>(this.team2);
		Predicate<Creature> isDead = c -> c.getHP() <= 0;

		Iterator<List<TeamCreature>> iterator = creatures.iterator();
		int turn = 1;
		while (team1.size() > 0 && team2.size() > 0) {
			List<TeamCreature> current = iterator.next();
			for (TeamCreature tc : current) {
				if (tc.team == 1)
					tc.creature.play(team2, team1);
				else
					tc.creature.play(team1, team2);
			}

			if (team1.removeIf(isDead))
				System.out.println("Creatures from team1 died");
			if (team2.removeIf(isDead))
				System.out.println("Creatures from team2 died");

			if (!iterator.hasNext()) {
				iterator = creatures.iterator();
				System.out.println("Turn " + turn++ + " passed");
			}
		}

		System.out.print("Combat ended. Victory : ");
		if (team1.size() > 0)
			System.out.println("team1");
		else if (team2.size() > 0)
			System.out.println("team2");
		else
			System.out.println("none. Draw!");
	}

	private void displayTeam(List<Creature> team) {
		for (Creature c : team)
			System.out.printf("\t%s%n", c);
	}

	private List<List<TeamCreature>> getTeamCreatures() {
		List<TeamCreature> teamCreatures = new ArrayList<>();
		team1.stream().map(c -> rollInitiative(c, 1)).forEach(teamCreatures::add);
		team2.stream().map(c -> rollInitiative(c, 2)).forEach(teamCreatures::add);

		Collections.sort(teamCreatures);

		List<List<TeamCreature>> creatures = new ArrayList<>();
		{
			List<TeamCreature> current = null;
			TeamCreature last = null;
			for (TeamCreature c : teamCreatures) {
				if (current == null || c.initiative != last.initiative) {
					current = new ArrayList<>();
					creatures.add(current);
				}
				current.add(c);
				last = c;
			}
		}
		return creatures;
	}

	private TeamCreature rollInitiative(Creature c, int team) {
		TeamCreature tc = new TeamCreature();
		tc.creature = c;
		tc.team = team;
		tc.initiative = Dice.roll(1, 20, c.getInitiaiveMod());
		return tc;
	}

	private class TeamCreature implements Comparable<TeamCreature> {
		Creature creature;
		int team, initiative;

		@Override
		public int compareTo(TeamCreature o) {
			return Integer.compare(initiative, o.initiative);
		}
	}
}
