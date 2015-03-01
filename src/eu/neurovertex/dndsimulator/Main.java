package eu.neurovertex.dndsimulator;

import com.hp.hpl.jena.ontology.OntModel;
import com.hp.hpl.jena.ontology.OntModelSpec;
import com.hp.hpl.jena.rdf.model.ModelFactory;

import java.io.File;
import java.io.FileReader;
import java.io.IOException;

/**
 * @author Neurovertex
 *         Date: 12/02/2015, 14:39
 */
public class Main {
	public static final String DEFAULTFILE = "dnd.owl", FORMAT = "TTL";

	public static void main(String[] args) throws IOException {
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
