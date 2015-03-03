package eu.neurovertex.dndsimulator;

/**
 * 26/02/15
 * @author darkymago
 */
public class SimpleWeapon implements Weapon {

    private final Dice      damageDice;
    private final String    name;
    private final int       multiplier;
    private final WeaponType type;
    // TODO: List of effects (poison,...)

    public SimpleWeapon(String name, Dice damageDice, int multiplier, WeaponType type) {
        this.name       = name;
        this.damageDice = damageDice;
        this.multiplier = multiplier;
        this.type       = type;
    }

    public SimpleWeapon(String name, Dice damageDice) {
        this(name, damageDice, 2, WeaponType.MELEE);
    }

    public static SimpleWeapon Dagger() {
        return new SimpleWeapon("Dagger", new Dice(1, 4, 0));
    }

    public static SimpleWeapon LongSword() {
        return new SimpleWeapon("LongSword", new Dice(1, 8, 0));
    }

    @Override
    public int damage() {
        return damageDice.roll();
    }

    @Override
    public int getCriticalMultiplier() {
        return multiplier;
    }

    @Override
    public WeaponType getType() {
        return type;
    }

    @Override
    public String getDescription() { return name + "(" + damageDice.getDescription() + ")"; }

    @Override
    public String toString() {
        return "SimpleWeapon{" +
                "name=" + name +
                ", damageDice=" + damageDice +
                '}';
    }
}
