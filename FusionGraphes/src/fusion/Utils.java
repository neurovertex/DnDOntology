package fusion;

/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
import java.util.ArrayList;
import java.util.HashMap;

/**
 *
 * @author thomas
 */
public class Utils {

    public static double hammingWithSynonymes(String s1, String s2, HashMap<String, String> synonymes) {
        if(s1 == null || s2 == null){
            return 1;
        }
        String synonyme;
        if ((synonyme = synonymes.get(s1)) != null) {
            if (synonyme.equals(s2)) {
                return 0;
            }
        }
        
        if ((synonyme = synonymes.get(s2)) != null) {
            if (synonyme.equals(s1)) {
                return 0;
            }
        }
        
        return hamming(s1,s2);
    }

    public static double hamming(String s1, String s2) {
        int taillemin = Math.min(s1.length(), s2.length());
        char[] c1 = s1.toCharArray();
        char[] c2 = s2.toCharArray();
        double somme = 0.;
        for (int i = 0; i < taillemin; i++) {
            if (c1[i] != c2[i]) {
                somme++;
            }
        }

        return (double) (somme + Math.abs(s1.length() - s2.length())) / Math.max(s1.length(), s2.length());
    }

    public static double ngram(String s1, String s2, int taille) {
        ArrayList<String> l1 = new ArrayList<>();
        ArrayList<String> l2 = new ArrayList<>();
        s1.split("t");

        for (int i = 0; i < s1.length() - taille + 1; i++) {
            l1.add("" + s1.subSequence(i, i + taille));
        }

        for (int i = 0; i < s2.length() - taille + 1; i++) {
            l2.add("" + s2.subSequence(i, i + taille));
        }
        int intersect = 0;
        for (String s : l1) {
            if (l2.contains(s)) {
                intersect++;
            }
        }
        return (double) intersect / (Math.min(s1.length(), s2.length()) - taille + 1);
    }

    public static void main(String[] args) {
//        System.out.println("n-gram ="+Utils.ngram("FRANCE", "FRENCH", 1) );
//        System.out.println("hamming ="+Utils.hamming("FRANCE", "FRENCH"));
        System.out.println("hamming =" + Utils.hamming("alice", "alicee"));
        System.out.println("hamming =" + Utils.hamming("alice", "aime"));
        System.out.println("hamming =" + Utils.hamming("alice", "marcel"));
//        System.out.println("hamming ="+Utils.hamming("Naw York", "New York City"));
    }

}
