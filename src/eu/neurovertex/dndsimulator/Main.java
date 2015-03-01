package eu.neurovertex.dndsimulator;

// needed for Jena example
import com.hp.hpl.jena.ontology.OntModel;
import com.hp.hpl.jena.ontology.OntModelSpec;
import com.hp.hpl.jena.rdf.model.ModelFactory;

import java.io.File;
import java.io.FileReader;
import java.io.IOException;

// needed for creatures example
import java.util.ArrayList;
import java.util.List;

/**
 * @author Neurovertex
 *         Date: 12/02/2015, 14:39
 */
public class Main {
	public static final String DEFAULTFILE = "dnd.owl", FORMAT = "TTL";

    public static void main(String[] args) throws IOException {
        // Jena example :
        mainJena(args);

        // Creatures example :
        mainCreas(/*args*/);
    }

    public static void mainCreas(/*String[] args*/) {
        List<Creature> team1 = new ArrayList<>(), team2 = new ArrayList<>();

        for (int i = 0; i < 5; i++)
            team1.add(new SimpleCreature("Human " + i, Dice.roll(1, 20, 10), 3, SimpleWeapon.LongSword()));
        System.out.println("Created team :\n" + team1);

        for (int i = 0; i < 10; i++)
            team2.add(new SimpleCreature("Goblin " + i, Dice.roll(1, 10, 2), 1));

        Simulator simulator = new Simulator(team1, team2);
        simulator.run();
    }

	public static void mainJena(String[] args) throws IOException {
		/**
		 * @see http://jena.apache.org/documentation/inference/#owl
		 */
		OntModel ontology = ModelFactory.createOntologyModel(OntModelSpec.OWL_MEM);
		File file = new File(args.length > 0 ? args[0] : DEFAULTFILE);
		try (FileReader reader = new FileReader(file)) {
			ontology.read(reader, FORMAT);
		}

		System.out.println(ontology.getOntClass(ontology.expandPrefix("dnd:Possession")));

		ontology.getNsPrefixMap().entrySet().forEach(System.out::println);
	}
}
