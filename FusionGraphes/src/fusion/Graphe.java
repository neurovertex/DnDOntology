/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package fusion;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.Stack;

/**
 *
 * @author CARRARA Nicolas <nicolas.carrara1@etu.univ-lorraine.fr>
 */
public class Graphe {

    private final int LEFT = 0;
    private final int MIDDLE = 1;
    private final int RIGHT = 2;

    private Map<String, Set<String>> synonymes;

    /**
     * @return the noeuds
     */
    public HashMap<String, Set<Couple>> getNoeuds() {
        return noeuds;
    }

    public final class Couple {

        String urileft;
        String uriright;

        Couple(String urileft, String uriright) {
            this.urileft = urileft;
            this.uriright = uriright;
        }

        Couple(Couple c) {
            this.urileft = c.urileft;
            this.uriright = c.uriright;
        }

        @Override
        public Object clone() {
            return new Couple(this);
        }

        public boolean equals(Object o) {
            Couple c = (Couple) o;
            boolean isEqualLeft = Utils.hammingWithSynonymes(urileft, c.urileft, synonymes) < SEUIL;
            boolean isEqualRigth = Utils.hammingWithSynonymes(uriright, c.uriright, synonymes) < SEUIL;

            return isEqualLeft && isEqualRigth;
        }

        public String toString() {
            return "[" + urileft + " , " + uriright + "]";
        }

    }

    private HashMap<String, Set<Couple>> noeuds;

    public static double SEUIL = 0.2;

    // on suppose qu'il n y a pas de doublons
    public Graphe(String[][] triplets, Map<String, Set<String>> synonymes) {
        this.synonymes = synonymes;
        noeuds = new HashMap<>();
        for (String[] t : triplets) {
            if (noeuds.get(t[LEFT]) == null) {
                Set<Couple> couples = new HashSet<>();
                noeuds.put(t[LEFT], couples);
            }
            if (noeuds.get(t[RIGHT]) == null) {
                Set<Couple> couples = new HashSet<>();
                noeuds.put(t[RIGHT], couples);

            }
            Couple couple = new Couple(t[LEFT], t[RIGHT]);
            if (noeuds.get(t[MIDDLE]) == null) {
                Set<Couple> couples = new HashSet<>();
                noeuds.put(t[MIDDLE], couples);

            }
            noeuds.get(t[MIDDLE]).add(couple);
        }
    }

    public void completeMerge(Graphe target) {
        // on récupère tout les couples qu'on a pas déjà
        target.noeuds.forEach((kt, ct) -> {
            Set<Couple> couples;
            String k = getSimilarKey(kt);
            if (k == null) {
                couples = new HashSet<>();
                noeuds.put(kt, couples);
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
        for (String k : noeuds.keySet()) {
//            System.out.println("===> k : "+k);
            if ((d = Utils.hammingWithSynonymes(k, key, synonymes)) < SEUIL) {
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
        Set<Couple> couplesSource = noeuds.get(key);
        if (couplesSource == null) {
            couplesSource = new HashSet<>();
            noeuds.put(key, couplesSource);
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
                    noeuds.put(c.urileft, couples);
                    urilefttemp = c.urileft;
                }
                if (uririghttemp == null) {
                    Set<Couple> couples = new HashSet<>();
                    noeuds.put(c.uriright, couples);
                    uririghttemp = c.uriright;
                }
                couplesSource.add(new Couple(urilefttemp, uririghttemp));
            }
        }
    }

    // on suppose que g1 est inclu dans g2
    public Map<String, Set<Couple>> pdifference(/*Graphe g1, */Map<String, Set<Couple>> hm) {
        Map<String, Set<Couple>> res = new HashMap<>();

        for (String key : hm.keySet()) {
            if (!noeuds.containsKey(key)) {
                res.put(key, new HashSet<>());
            }

            for (Couple c : hm.get(key)) {
                if (!(noeuds.containsKey(c.urileft) && noeuds.containsKey(c.uriright))) {
                    if (res.containsKey(key)) {
                    } else {
                        res.put(key, new HashSet<>());
                    }
                    res.get(key).add((Couple) c.clone());
                    if (!noeuds.containsKey(c.urileft)) {
                        if (!res.containsKey(c.urileft)) {
                            res.put(c.urileft, new HashSet<>());
                        }
                    }
                    if (!noeuds.containsKey(c.uriright)) {
                        if (!res.containsKey(c.uriright)) {
                            res.put(c.uriright, new HashSet<>());
                        }
                    }
                }
            }
        }
        return res;
    }

    /**
     *
     * @param g2
     * @return les triplets correspondants à g2/this au sens ensembliste
     */
    public String[][] difference(Graphe g2) {
        return toTripleStore(pdifference(g2.getNoeuds()));
    }

    public String[][] toTripleStore() {
        return toTripleStore(noeuds);
    }

    public static String[][] toTripleStore(Map<String, Set<Couple>> map) {
        Stack<String[]> pile = new Stack<>();
        int size = 0;
        for (String key : map.keySet()) {
            for (Couple c : map.get(key)) {
                size++;
                String[] triplet = {c.urileft, key, c.uriright};
                pile.push(triplet);
            }
        }
        String[][] triplets = new String[size][3];
        size--;
        while (!pile.empty()) {
            triplets[size] = pile.pop();
            size--;
        }
        ArrayList l;
        return triplets;
    }

}
