package com.company;

import fusion.Graphe;
import org.semanticweb.owlapi.apibinding.OWLManager;
import org.semanticweb.owlapi.model.*;
import uk.co.magus.fourstore.client.Store;

import java.io.File;
import java.io.IOException;
import java.net.MalformedURLException;
import java.util.*;

public class Main {

    private static OWLOntologyManager m= OWLManager.createOWLOntologyManager();
    private static File fichOnt=new File("../dnd.ttl");
    private static File fichOntOut=new File("../dndCompleted.ttl");

    private static String sparql = "SELECT * WHERE { ?s ?p ?o }";
    private static String sparql1
            = "select distinct ?monsters (SAMPLE(?types) AS ?type) (SAMPLE(?alignments) as ?alignment) where {\n" +
            "{<http://dbpedia.org/resource/List_of_Dungeons_&_Dragons_3.5_edition_monsters> dbpprop:name ?monster}\n" +
            "UNION\n" +
            "{?monster dcterms:subject <http://dbpedia.org/resource/Category:Dungeons_&_Dragons_standard_creatures>}\n" +
            "UNION\n" +
            "{?monster dcterms:subject <http://dbpedia.org/resource/Category:Dungeons_&_Dragons_creatures_from_folklore_and_mythology>}\n" +
            "UNION\n" +
            "{?monster dcterms:subject <http://dbpedia.org/resource/Category:Dungeons_&_Dragons_creatures>}\n" +
            "UNION\n" +
            "{<http://dbpedia.org/resource/List_of_Dungeons_&_Dragons_3.5_edition_monsters> dbpprop:name ?monster . ?monster dbpprop:type ?typess}\n" +
            "UNION\n" +
            "{?monster dcterms:subject <http://dbpedia.org/resource/Category:Dungeons_&_Dragons_creatures_from_folklore_and_mythology> . ?monster dbpprop:type ?typess}\n" +
            "UNION\n" +
            "{?monster dcterms:subject<http://dbpedia.org/resource/Category:Dungeons_&_Dragons_standard_creatures> . ?monster dbpprop:type ?typess}\n" +
            "UNION\n" +
            "{?monster dcterms:subject <http://dbpedia.org/resource/Category:Dungeons_&_Dragons_creatures> . ?monster dbpprop:type ?typess}\n" +
            "UNION\n" +
            "{<http://dbpedia.org/resource/List_of_Dungeons_&_Dragons_3.5_edition_monsters> dbpprop:name ?monster . ?monster dbpprop:alignment ?alignments}\n" +
            "UNION\n" +
            "{?monster dcterms:subject<http://dbpedia.org/resource/Category:Dungeons_&_Dragons_standard_creatures> . ?monster dbpprop:alignment ?alignments}\n" +
            "UNION\n" +
            "{?monster dcterms:subject <http://dbpedia.org/resource/Category:Dungeons_&_Dragons_creatures> . ?monster dbpprop:alignment ?alignments}\n" +
            "BIND(strafter(str(?monster), \"http://dbpedia.org/resource/\") as ?monsters)\n" +
            "BIND(strafter(str(?typess), \"http://dbpedia.org/resource/\") as ?types)\n" +
            "\n" +
            "}";
            /*= "SELECT ?monster "//?type "
            + "WHERE{ <http://dbpedia.org/resource/List_of_Dungeons_&_Dragons_3.5_edition_monsters> dbpprop:name ?monster . ?monster  dbpprop:type ?type}";*/

    private static ArrayList<String[]> triplets = new ArrayList<String[]>();
    private static ArrayList<String[]> triplets2 = new ArrayList<String[]>();

    public static void main(String[] args) {
        Store store;
        Store store1;
        try {
            System.out.println("Start");
            store = new Store("http://localhost:8080");
            store1 = new Store("http://dbpedia.org");
            String[] morale = {"Good","Evil","Neutral"};
            String[] loyaute = {"Chaotic","Lawful","Neutral"};
            /*//simple query
            String response1 = store.query(sparql);
            System.out.println(response1);
            //specifying outputformat
            String response2 = store.query(sparql,Store.OutputFormat.JSON);
            System.out.println(response2);
            //specifying softlimit and default output format
            String response3 = store.query(sparql,5);
            System.out.println(response3);*/
            //specifying outputformat and soft limit
            String response4 = store.query(sparql,Store.OutputFormat.TAB_SEPARATED);//, 1);
            System.out.println(response4);
            String[] lines = response4.split("\n");
            for (int i = 1; i < lines.length - 1; i++) {
                String[] ogretab = lines[i].split("\t");
                String[] temp = new String[3];
                for (int j = 0; j < ogretab.length; j++) {
                    if (ogretab[j].contains("#")) {
                        temp[j] = ogretab[j].split("#")[1].split(">")[0];
                        if (temp[j].contains("\'"))
                            temp[j] = temp[j].split("\'")[1].split("\'")[0];
                    }
                    //else
                        //temp[j] = "untitled" + ogretab[j].split("untitled")[1].split(">")[0];
                    //System.out.println(triplets[i - 1][j]);
                }
                triplets.add(temp);
            }
            String response5 = store1.query(sparql1, Store.OutputFormat.TAB_SEPARATED);//, 1);
            System.out.println(response5);
            String[] lines1 = response5.split("\n");
            for (int i = 1; i < lines1.length; i++) {
                String[] ogretab = lines1[i].split("\t");
                String[] tempMonstre = new String[3];
                String[] tempType = new String[3];
                String[] tempAlignement = new String[3];
                //String[] tempMonstreType = new String[3];
                String[] tempMonstreAlignement = new String[3];
                List<String> tempListAlignement = new ArrayList<>();
                String ogre = "";
                if (ogretab.length > 0 && !ogretab[0].equals("") && !ogretab[0].equals("\"\"") && (!ogretab[0].contains("List") && !ogretab[0].contains("Index")) && !ogretab[0].contains("edition")) {
                    ogre = ogretab[0];
                    ogre = ogre.replaceAll("\"", "");
                    ogre = ogre.replace("_(Dungeons_&_Dragons)", "");
                    ogre = ogre.replace("\'", "");
                    ogre = ogre.replace(" ", "_");
                    ogre = ogre.toUpperCase(Locale.ROOT);
                    tempMonstre[0] = ogre;
                    tempMonstre[1] = "type";
                    tempMonstre[2] = "Monstre";
                }
                if (ogretab.length > 1 && !ogretab[1].equals("") && !ogretab[1].equals("\"\"") && (!ogretab[1].contains("\"List\"") && !ogretab[0].contains("\"Index\""))) {
                    String ogre1 = ogretab[1];
                    ogre1 = ogre1.replaceAll("\"","");
                    ogre1 = ogre1.replace("_(Dungeons_&_Dragons)","");
                    ogre1 = ogre1.replace("\'", "");
                    ogre1 = ogre1.replace(" ", "_");
                    tempMonstre[2] = ogre1;
                    tempType[0] = ogre1;
                    tempType[1] = "subClassOf";
                    tempType[2] = "Monstre";
                    /*tempMonstreType[0] = ogre;
                    tempMonstreType[1] = "";
                    tempMonstreType[2] = ogre1;*/
                }
                if (ogretab.length == 3 && !ogretab[2].equals("") && !ogretab[2].equals("\"\"") && !ogretab[2].contains("http") && !ogretab[2].contains("depending") && !ogretab[2].contains("depending")) {
                    String ogre2 = ogretab[2];
                    ogre2 = ogre2.replaceAll("\"","");
                    ogre2 = ogre2.replace("_(Dungeons_&_Dragons)","");
                    ogre2 = ogre2.replace("\'", "");
                    ogre2 = ogre2.replace(" ", "_");
                    ogre2 = ogre2.toUpperCase();
                    String[] ogre2Tab = ogre2.split("_");
                    for (int j = 0; j < ogre2Tab.length; j++) {
                        ogre2Tab[j] = ogre2Tab[j].toLowerCase();
                        ogre2Tab[j] = Character.toString(ogre2Tab[j].charAt(0)).toUpperCase()+ogre2Tab[j].substring(1);
                        for (int k = 0; k < loyaute.length; k++) {
                            if (loyaute[k].compareTo(ogre2Tab[j]) == 0) {
                                tempListAlignement.add(loyaute[k]);
                                j++;
                                break;
                            }
                        }
                        for (int k = 0; k < morale.length; k++) {
                            if (j == ogre2Tab.length)
                                break;
                            if (morale[k].compareTo(ogre2Tab[j]) == 0) {
                                tempListAlignement.add(morale[k]);
                                break;
                            }
                        }
                    }
                    /*tempAlignement[0] = ogre2;
                    tempAlignement[1] = "type";
                    tempAlignement[2] = "Alignement";
                    tempMonstreAlignement[0] = ogre;
                    tempMonstreAlignement[1] = "a_pour_alignement";
                    tempMonstreAlignement[2] = ogre2;*///ne sert plus mais au cas ou
                }
                if (ogretab.length > 0 && tempMonstre[0] != null) {
                    triplets2.add(tempMonstre);
                }
                if (ogretab.length > 1 && tempType[0] != null) {
                    triplets2.add(tempType);
                    //triplets2.add(tempMonstreType);
                }
                if (ogretab.length > 2 && tempAlignement[0] != null && tempMonstreAlignement[0] != null) {
                    triplets2.add(tempAlignement);
                    for (int j = 0; j < tempListAlignement.size(); j++) {
                        tempMonstreAlignement[0] = ogre;
                        tempMonstreAlignement[1] = "a_pour_alignement";
                        tempMonstreAlignement[2] = tempListAlignement.get(j);
                        triplets2.add(tempMonstreAlignement);
                        tempMonstreAlignement = new String[3];
                    }
                }
                //String ogre2 = ogre.replaceAll("_\\Q(\\E.*\\Q)\\E", " "); // pour enlever les précision entre parenthèse
                //System.out.println("" + lines1[i]);
            }
            System.out.println("Done");
        } catch (MalformedURLException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
        System.out.println(Arrays.deepToString(triplets2.toArray()));

        String[][] tripletsTab = new String[triplets.size()][3];
        String[][] triplets2Tab = new String[triplets2.size()][3];

        for (int i = 0; i < triplets.size(); i++) {
            tripletsTab[i] = triplets.get(i);
        }
        for (int i = 0; i < triplets2.size(); i++) {
            triplets2Tab[i] = triplets2.get(i);
        }

        Graphe source = new Graphe(tripletsTab, new HashMap<>());
        Graphe source_copy = new Graphe(tripletsTab, new HashMap<>());
        Graphe target = new Graphe(triplets2Tab, new HashMap<>());

        System.out.println("" + source.getNoeuds());
        System.out.println("" + target.getNoeuds());
        source.completeMerge(target);

        System.out.println("" + source.getNoeuds());

        source.completeMerge(target);
        String[][] results = source_copy.difference(source);
        System.out.println("" + Arrays.deepToString(results));

        //On complète la base de Connaissance
        try {
            OWLOntology ontology=m.loadOntologyFromOntologyDocument(fichOnt);


            IRI iriOntology=ontology.getOntologyID().getOntologyIRI().get();

            OWLAxiom axiom;
            AddAxiom ad;

            for(int i=0;i<results.length;i++) {
                axiom = Main.getAxOf(ontology, results[i], iriOntology);
                ad = new AddAxiom(ontology, axiom);
                m.applyChange(ad);
            }

            m.saveOntology(ontology, IRI.create(fichOntOut));

            System.out.println("Done");

        } catch (OWLOntologyCreationException e) {
            System.out.println("Impossible d'ouvrir le fichier'");
            e.printStackTrace();
        } catch (OWLOntologyStorageException e) {
            System.out.println("Impossible d'exporter l'ontologie");
            e.printStackTrace();
        }
    }

    private static OWLAxiom getAxOf(OWLOntology ontology,String[] a,IRI iriOntology){
        OWLAxiom axiom=null;
        OWLDataFactory df=m.getOWLDataFactory();
        if(a[1].equalsIgnoreCase("subclassOf")){
            OWLClass clsA =df.getOWLClass(IRI.create(iriOntology +"#"+a[0]));
            OWLClass clsB =df.getOWLClass(IRI.create(iriOntology +"#"+a[2]));
            axiom= df.getOWLSubClassOfAxiom(clsA, clsB);
        }else if (a[1].equalsIgnoreCase("type")){

            OWLIndividual clsA =df.getOWLNamedIndividual(IRI.create(iriOntology + "#" + a[0]));
            OWLClass clsB =df.getOWLClass(IRI.create(iriOntology + "#" + a[2]));
            axiom= df.getOWLClassAssertionAxiom(clsB, clsA);

        }else if(a[1].equalsIgnoreCase("a_pour_alignement")){
            OWLIndividual clsA =df.getOWLNamedIndividual(IRI.create(iriOntology + "#" + a[0]));
            OWLIndividual clsB =df.getOWLNamedIndividual(IRI.create(iriOntology + "#" + a[2]));
            OWLObjectProperty prop=df.getOWLObjectProperty(IRI.create(iriOntology + "#" + a[1]));
            axiom=df.getOWLObjectPropertyAssertionAxiom(prop, clsA,clsB);
        }
        return axiom;
    }
}