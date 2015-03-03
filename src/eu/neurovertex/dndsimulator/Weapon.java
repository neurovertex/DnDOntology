package eu.neurovertex.dndsimulator;

/**
 * @author darkymago
 * 		Date : 26/02/15
 */
public interface Weapon {

    public int damage();

    public int getCriticalMultiplier();

    public WeaponType getType();

    public String getDescription();

	public enum WeaponType {MELEE, RANGED}

}