/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package main;

import fusion.Graphe;
import java.io.IOException;
import java.net.MalformedURLException;
import java.util.HashMap;
import uk.co.magus.fourstore.client.Store;

/**
 *
 * @author CARRARA Nicolas <nicolas.carrara1@etu.univ-lorraine.fr>
 */
public class Main {

    private static String sparql
            = "SELECT ?monster ?type "
            + "WHERE{ <http://dbpedia.org/resource/List_of_Dungeons_&_Dragons_3.5_edition_monsters> dbpprop:name ?monster . ?monster  dbpprop:type ?type}";

    private static String sparql2 = "SELECT * WHERE { ?s ?o ?p } LIMIT 10";
    
    public static void main(String[] args) {

        final String e = "\\\\";
        Store store;
        try {
//            store = new Store("http://fr.dbpedia.org");
            store = new Store("http://dbpedia.org");
            Store store2 = new Store("http://10.10.116.17:8080");
            //simple query
//			String response1 = store.query(sparql);
//			System.out.println(response1);
//			//specifying outputformat
//			String response2 = store.query(sparql,Store.OutputFormat.JSON);
//			System.out.println(response2);
//			//specifying softlimit and default output format
//			String response3 = store.query(sparql,5);
//			System.out.println(response3);
            //specifying outputformat and soft limit
            String response1 = store2.query(sparql, Store.OutputFormat.TAB_SEPARATED, 1);
            System.out.println("" + response1);
            String response4 = store.query(sparql, Store.OutputFormat.TAB_SEPARATED, 1);
            System.out.println("" + response4);
            String[] lines = response4.split("\n");
            System.out.println("" + lines.length);
            for (int i = 0; i < lines.length; i++) {
                String[] ogretab = lines[i].split("/");
                String ogre = ogretab[ogretab.length - 1];
                String ogre1 = ogre.replaceAll("\"", " ");
                String ogre2 = ogre1.replaceAll("_\\Q(\\E.*\\Q)\\E", " "); // pour enlever les précision entre parenthèse
                lines[i] = ogre2;
                System.out.println("" + lines[i]);
            }
        } catch (MalformedURLException ex) {
            ex.printStackTrace();
        } catch (IOException ex) {
            ex.printStackTrace();
        }

        Graphe source = new Graphe(triplets, new HashMap<>());
        Graphe target = new Graphe(triplets2, new HashMap<>());

        System.out.println("" + source);
        System.out.println("" + target);
        source.completeMerge(target);

        System.out.println("" + source);

    }
}
