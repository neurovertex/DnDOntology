/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

import fusion.Graphe;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Set;
import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;

/**
 *
 * @author CARRARA Nicolas <nicolas.carrara1@etu.univ-lorraine.fr>
 */
public class GrapheTest {
    
    
    
    public GrapheTest() {
    }
    
    @BeforeClass
    public static void setUpClass() {
    }
    
    @AfterClass
    public static void tearDownClass() {
    }
    
    @Before
    public void setUp() {
        HashMap<String,Set<String>> synonymes = new HashMap<>();
        Set set = new HashSet<String>();
        set.add("kikoo");
        synonymes.put("lol",set);
        source = new Graphe(triplets,synonymes);
        source_copy = new Graphe(triplets,synonymes);
        target = new Graphe(triplets2,synonymes);
        targetapprox = new Graphe(triplets3,synonymes);
    }
    
    @After
    public void tearDown() {
    }
    
    private Graphe source;
    private Graphe source_copy;
    private Graphe target;
    private Graphe targetapprox;
    private String[][] triplets = 
    {
        {"alice","aime","bob"},
        {"bob","deteste","alice"},
        {"alice","subc","Femme"},
//        {"benjamin","lol","deMerde"}
    };
    private String[][] triplets2 = 
    {
        {"alice","aime","marcel"},
        {"alice","aime","bob"}
    };
    private String[][] triplets3 = 
    {
        {"alicee","aime","marcel"},
        {"nicolas","kikoo","deFille"}
    };

    // TODO add test methods here.
    // The methods must be annotated with annotation @Test. For example:
    //
//     @Test
     public void creation() {
         System.out.println(""+source.getNoeuds());
//         System.out.println(""+source_copy.getNoeuds());
         System.out.println(""+target.getNoeuds());
         source.completeMerge(target);
         System.out.println(""+source.getNoeuds());
//         System.out.println(""+source_copy.pdifference(source));
     }
//     @Test
     public void mergeApprox() {
         System.out.println(""+source.getNoeuds());
         System.out.println(""+targetapprox.getNoeuds());
         source.completeMerge(targetapprox);
         System.out.println(""+source.getNoeuds());
     }
     
     @Test 
     public void differenceTest(){
         
         System.out.println(""+source.getNoeuds());
         source.completeMerge(target);
         System.out.println(""+target.getNoeuds());
         System.out.println(""+source.getNoeuds());
         System.out.println("diff "+source_copy.pdifference(source.getNoeuds()));
         System.out.println(""+Arrays.deepToString(source_copy.difference(source)));
     
     }
     
//     @Test
     public void toTripleStoreTest(){
         System.out.println(""+Arrays.deepToString(source.toTripleStore()));
     }
}
