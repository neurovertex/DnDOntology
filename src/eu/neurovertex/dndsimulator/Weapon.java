package eu.neurovertex.dndsimulator;

/**
 * Created by darkymago on 26/02/15.
 */
public interface Weapon {

    public enum WeaponType { MELEE, RANGED}

    public int damage();

    public int getCriticalMultiplier();

    public WeaponType getType();

    public String getDescription();

}