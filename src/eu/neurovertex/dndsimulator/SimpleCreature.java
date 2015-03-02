package eu.neurovertex.dndsimulator;

import java.util.List;

/**
 * @author Neurovertex
 *         Date: 26/02/15
 *         Time: 16:43
 */
public class SimpleCreature implements Creature {
	private final String name;
    private static final Dice touchDice = new Dice(1, 20, 0);
	private int health;
    private final int ca;
    private final int bba;
    private Weapon weapon;
    private Abilities abilities;

    private static class Abilities { // (Caracteristiques)
        private int str;
        private int dex;
        private int con;
        private int itl;
        private int wis;
        private int cha;

        public Abilities(int str, int dex, int con, int itl, int wis, int cha) {
            this.str = str;
            this.dex = dex;
            this.con = con;
            this.itl = itl;
            this.wis = wis;
            this.cha = cha;
        }

        public Abilities(Dice rollDice) {
            this(7+rollDice.roll(), 7+rollDice.roll(), 7+rollDice.roll(),
                    7+rollDice.roll(), 7+rollDice.roll(), 7+rollDice.roll());
        }

        public int strMod() {return (str/2 - 5);}
        public int dexMod() {return (dex/2 - 5);}
        public int conMod() {return (con/2 - 5);}
        public int intMod() {return (itl/2 - 5);}
        public int wisMod() {return (wis/2 - 5);}
        public int chaMod() {return (cha/2 - 5);}

        @Override
        public String toString() {
            return "Abilities{" +
                    "str=" + str +
                    ", dex=" + dex +
                    ", con=" + con +
                    ", int" + itl +
                    ", wis=" + wis +
                    ", cha=" + cha +
                    '}';
        }
    }

    public SimpleCreature(String name, int health, Abilities abilities, int bba, Weapon weapon) {
		this.name       = name;
		this.health     = health;
        this.abilities  = abilities;
        this.bba        = bba;
        //this.touchDice  = new Dice(1,20,0) ; // one for everyone
        this.ca         = 10 + abilities.dexMod();
        this.weapon     = weapon;
    }

    public SimpleCreature(String name, int health, int bba, Weapon weapon) {
        this(name, health, new Abilities(new Dice(1,6,0)), bba, weapon);
    }

    public SimpleCreature(String name, int health, int bba) {
        this(name, health, new Abilities(new Dice(1,6,0)), bba, SimpleWeapon.Dagger());
    }

    @Override
    public String getName() {
        return name;
    }

    @Override
	public int getHP() {
		return health;
	}

	@Override
	public int getInitiativeMod() {
		return abilities.dexMod();
	}

	@Override
	public void play(List<Creature> enemies, List<Creature> friends) {
		Creature enemy = enemies.get((int) (Math.random() * enemies.size()));
//		System.out.println(toString() +" attacking");
		tryAttack(enemy);
	}

    @Override
    public void tryAttack(Creature enemy) {
        int roll;
        boolean critical;

        System.out.printf("Creature %s try to touch %s", name, enemy.getName());

        // Critical Strike ?
        critical = false;
        roll = touchDice.roll();

        if (roll == 20) {
            critical = true;
            roll = touchDice.roll();
        }

        switch ( weapon.getType() ) {
            case MELEE:
                enemy.takeAttack(weapon, abilities.strMod(), roll + bba, critical);
                break;
            case RANGED:
                enemy.takeAttack(weapon, abilities.dexMod(), roll + bba, critical);
                break;
        }
    }

    @Override
    public void takeAttack(Weapon wpn, int damageMod, int touchRoll, boolean crit) {
        System.out.printf(" with a%s touch roll of %d : ", (crit ? " critical" : ""), touchRoll);

        boolean touched = ca <= touchRoll;
        if (touched || crit) {
            int damage = ((touched && crit) ? wpn.getCriticalMultiplier() : 1)*(wpn.damage() + damageMod);
            System.out.printf("%s taking %d%s damage from %s%n",
                    name, damage, ((touched && crit) ? " critical" : ""), wpn.getDescription());
            health -= damage;
        }
        else
            System.out.printf("Attack missed%n");
        // TODO: effects of weaponry (poison, ...)?
    }

    @Override
	public String toString() {
		return "SimpleCreature{" +
				"name='" + name + '\'' +
				", health=" + health +
				", abilities=" + abilities +
				", weapon=" + weapon +
				'}';
	}
}
