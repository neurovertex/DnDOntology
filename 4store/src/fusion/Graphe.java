/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package fusion;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Set;

/**
 *
 * @author CARRARA Nicolas <nicolas.carrara1@etu.univ-lorraine.fr>
 */
public class Graphe {

    private final int LEFT = 0;
    private final int MIDDLE = 1;
    private final int RIGHT = 2;

    private HashMap<String,String> synonymes;
    
    /**
     * @return the noeuds
     */
    public HashMap<String, Set<Couple>> getNoeuds() {
        return noeuds;
    }

    public void setNoeuds(HashMap<String, Set<Couple>> noeuds) {
        this.noeuds = noeuds;
    }

    public class Couple {

        String urileft;
        String uriright;

        Couple(String urileft, String uriright) {
            this.urileft = urileft;
            this.uriright = uriright;
        }

        public boolean equals(Object o) {
            Couple c = (Couple) o;
            boolean isEqualLeft = Utils.ngramWithSynonymes(urileft, c.urileft, synonymes) < SEUIL;
            boolean isEqualRigth = Utils.ngramWithSynonymes(uriright, c.uriright, synonymes) < SEUIL;

            return isEqualLeft && isEqualRigth;
        }

        public String toString() {
            return "[" + urileft + " , " + uriright + "]";
        }

    }

    private HashMap<String, Set<Couple>> noeuds;


    public static double SEUIL = 0.2;

    // on suppose qu'il n y a pas de doublons
    public Graphe(String[][] triplets, HashMap<String,String> synonymes) {
        this.synonymes = synonymes;
        setNoeuds(new HashMap<>());
        for (String[] t : triplets) {
            if (getNoeuds().get(t[LEFT]) == null) {
                Set<Couple> couples = new HashSet<>();
                getNoeuds().put(t[LEFT], couples);
            }
            if (getNoeuds().get(t[RIGHT]) == null) {
                Set<Couple> couples = new HashSet<>();
                getNoeuds().put(t[RIGHT], couples);

            }
            Couple couple = new Couple(t[LEFT], t[RIGHT]);
            if (getNoeuds().get(t[MIDDLE]) == null) {
                Set<Couple> couples = new HashSet<>();
                getNoeuds().put(t[MIDDLE], couples);

            }
            getNoeuds().get(t[MIDDLE]).add(couple);
        }
    }

    public void completeMerge(Graphe target) {
        // on récupère tout les couples qu'on a pas déjà
        target.getNoeuds().forEach((kt, ct) -> {
            Set<Couple> couples;
            String k = getSimilarKey(kt);
            if (k == null) {
                couples = new HashSet<>();
                getNoeuds().put(kt, couples);
                k = kt;
            }
//            System.out.println("K : "+k);
//            System.out.println("ct : "+ct);
            addAllApprox(k, ct);
        });
    }

    public final String getSimilarKey(String key) {
//        System.out.println("====================> key : "+key);
        double min = Double.MAX_VALUE;
        String res = null;
        double d;
        for (String k : getNoeuds().keySet()) {
//            System.out.println("===> k : "+k);
            if ((d = Utils.ngramWithSynonymes(k, key, synonymes)) < SEUIL) {
//                System.out.println("in");
                if (d < min) {
//                     System.out.println("zoub");
                    min = d;
                    res = k;
                }
            }
        }
        return res;

    }

    public final void addAllApprox(String key, Set<Couple> couplesTarget) {
        Set<Couple> couplesSource = getNoeuds().get(key);
        if (couplesSource == null) {
            couplesSource = new HashSet<>();
            getNoeuds().put(key, couplesSource);
        }
        String uririghttemp;
        String urilefttemp;
        for (Couple c : couplesTarget) {
            // containt utilise le equals avec les seuils définit
            if (couplesSource.contains(c)) {
                // on fait rien
            } else {
                // on ajoute avec le vocabulaire de la base source
//                System.out.println("c : "+c);
                uririghttemp = getSimilarKey(c.uriright);
                urilefttemp = getSimilarKey(c.urileft);
//                System.out.println(""+urilefttemp);
//                System.out.println(""+uririghttemp);
                if (urilefttemp == null) {
                    Set<Couple> couples = new HashSet<>();
                    getNoeuds().put(c.urileft, couples);
                    urilefttemp = c.urileft;
                }
                if (uririghttemp == null) {
                    Set<Couple> couples = new HashSet<>();
                    getNoeuds().put(c.uriright, couples);
                    uririghttemp = c.uriright;
                }
                couplesSource.add(new Couple(urilefttemp, uririghttemp));
            }
        }
    }

}
