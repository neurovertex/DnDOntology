package eu.neurovertex.dndsimulator;

import java.util.List;

/**
 * @author Neurovertex
 *         Date: 26/02/15
 *         Time: 16:19
 */
public interface Creature {
    public String getName();

	public int getHP();

	public int getInitiativeMod();

	public void play(List<Creature> enemies, List<Creature> friends);

    public void tryAttack(Creature to);

	public void takeAttack(Weapon wpn, int damageMod, int roll, boolean crit);

	public enum Loyalty {
		LAWFUL("LOYAL"), NEUTRAL("NEUTRE_LOYAUTE"), CHAOTIC("CHAOTIQUE");
		public final String uri;

		Loyalty(String uri) {
			this.uri = uri;
		}
	}

	public enum Morality {
		GOOD("BON"), NEUTRAL("NEUTRE_MORALE"), EVIL("MAUVAIS");
		public final String uri;

		Morality(String uri) {
			this.uri = uri;
		}


	}
}
