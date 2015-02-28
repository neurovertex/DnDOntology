package eu.neurovertex.dndsimulator;

/**
 * Created by darkymago on 26/02/15.
 */
public class SimpleWeapon implements Weapon {

    private final Dice damageDice;
    private final String name;
    // TODO: List of effects (poison,...)

    public SimpleWeapon(String name, Dice damageDice) {
        this.name = name;
        this.damageDice = damageDice;
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
    public String toString() {
        return "SimpleWeapon{" +
                "name=" + name +
                ", damageDice=" + damageDice +
                '}';
    }
}
