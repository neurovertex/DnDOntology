/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

import fusion.Graphe;
import java.util.HashMap;
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
        HashMap<String,String> synonymes = new HashMap<>();
        synonymes.put("lol", "kikoo");
        source = new Graphe(triplets,synonymes);
        target = new Graphe(triplets2,synonymes);
        targetapprox = new Graphe(triplets3,synonymes);
    }
    
    @After
    public void tearDown() {
    }
    
    private Graphe source;
    private Graphe target;
    private Graphe targetapprox;
    private String[][] triplets = 
    {
        {"alice","aime","bob"},
        {"bob","deteste","alice"},
        {"alice","subc","Femme"},
        {"benjamin","lol","deMerde"}
    };
    private String[][] triplets2 = 
    {
        {"alice","aime","marcel"},
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
         System.out.println(""+target.getNoeuds());
         source.completeMerge(target);
         System.out.println(""+source.getNoeuds());
     }
     @Test
     public void mergeApprox() {
         System.out.println(""+source.getNoeuds());
         System.out.println(""+targetapprox.getNoeuds());
         source.completeMerge(targetapprox);
         System.out.println(""+source.getNoeuds());
     }
}
