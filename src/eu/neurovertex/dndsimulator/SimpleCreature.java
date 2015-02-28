package eu.neurovertex.dndsimulator;

import java.util.List;

/**
 * @author Neurovertex
 *         Date: 26/02/15
 *         Time: 16:43
 */
public class SimpleCreature implements Creature {
	private final String name;
	private final int dexMod;
    private final Dice touchDice;
	private int health;
    private final int ca;
    private final int bba;
    private Weapon weapon;

    public SimpleCreature(String name, int health, int dexMod, int bba, Weapon weapon) {
		this.name = name;
		this.health = health;
		this.dexMod = dexMod;
        this.bba = 10 + dexMod;
        this.touchDice = new Dice(1,20,0) ;
        this.ca = 10 + dexMod;
        this.weapon = weapon;
    }

    public SimpleCreature(String name, int health, int dexMod, int bba) {
        this(name, health, dexMod, bba, SimpleWeapon.Dagger());
    }

	@Override
	public int getHP() {
		return health;
	}

	@Override
	public int getInitiativeMod() {
		return dexMod;
	}

	@Override
	public void play(List<Creature> enemies, List<Creature> friends) {
		Creature enemy = enemies.get((int) (Math.random() * enemies.size()));
//		System.out.println(toString() +" attacking");
		tryAttack(enemy);
	}

    @Override
    public void tryAttack(Creature enemy) {
        System.out.printf("Creature %s try to touch %s", name, enemy.toString());
        enemy.defenseOn(weapon, touchDice.roll());
    }

    @Override
	public void takeAttack(Weapon weapon) {
		System.out.printf("Creature %s taking damage from %s%n", name, weapon.toString());
        // For now, just normal damage from one weapon
		health -= weapon.damage();
        // TODO: effects of weaponry (poison, ...)?
	}

    @Override
    public void defenseOn(Weapon weapon, int touchRoll) {
        System.out.printf("Creature %s with a touch roll of %d%n", name, touchRoll);
        if (ca <= touchRoll)
            takeAttack(weapon);
    }

    @Override
	public String toString() {
		return "SimpleCreature{" +
				"name='" + name + '\'' +
				", health=" + health +
				", dexMod=" + dexMod +
				", weapon=" + weapon +
				'}';
	}
}
