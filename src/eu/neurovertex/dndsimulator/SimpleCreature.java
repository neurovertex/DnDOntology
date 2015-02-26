package eu.neurovertex.dndsimulator;

import java.util.List;

/**
 * @author Neurovertex
 *         Date: 26/02/15
 *         Time: 16:43
 */
public class SimpleCreature implements Creature {
	private final String name;
	private final int initMod;
	private final Dice attackDice;
	private int health;

	public SimpleCreature(String name, int health, int initMod, Dice attackDice) {
		this.name = name;
		this.health = health;
		this.initMod = initMod;
		this.attackDice = attackDice;
	}

	@Override
	public int getHP() {
		return health;
	}

	@Override
	public int getInitiaiveMod() {
		return initMod;
	}

	@Override
	public void play(List<Creature> enemies, List<Creature> friends) {
		Creature enemy = enemies.get((int) (Math.random() * enemies.size()));
//		System.out.println(toString() +" attacking");
		enemy.takeAttack(this, attackDice.roll());
	}

	@Override
	public void takeAttack(Creature from, int damage) {
//		System.out.printf("Creature %s taking %d damage%n", toString(), damage);
		health -= damage;
	}

	@Override
	public String toString() {
		return "SimpleCreature{" +
				"name='" + name + '\'' +
				", health=" + health +
				", initMod=" + initMod +
				", attackDice=" + attackDice +
				'}';
	}
}
