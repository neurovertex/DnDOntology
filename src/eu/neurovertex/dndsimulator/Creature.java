package eu.neurovertex.dndsimulator;

import java.util.List;

/**
 * @author Neurovertex
 *         Date: 26/02/15
 *         Time: 16:19
 */
public interface Creature {
	public int getHP();

	public int getInitiaiveMod();

	public void play(List<Creature> enemies, List<Creature> friends);

	public void takeAttack(Creature from, int damage);
}
