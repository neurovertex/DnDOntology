package eu.neurovertex.dndsimulator;

import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

import javax.xml.parsers.ParserConfigurationException;
import java.io.IOException;
import java.util.*;

// needed for Jena example
// needed for creatures example

/**
 * @author Neurovertex
 *         Date: 12/02/2015, 14:39
 */
public class Main {
	public static final String DEFAULTFILE = "dnd_test.ttl", FORMAT = "TTL", DATABASEFILE = "parser/database-en.xml";

	public static void main(String[] args) throws IOException, ParserConfigurationException, SAXException {

//		Creatures example :
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

	public static List<Node> asList(NodeList n) {
		return n.getLength() == 0 ?
				Collections.<Node>emptyList() : new NodeListWrapper(n);
	}

	private static String normalizeClassName(String name) {
		String replace = name.replaceAll("[^\\w ]+", "").replace(' ', '-');
		return replace.matches("^\\d.*") ? "Dnd" + replace : replace;
	}

	public static String normalizeInstanceName(String name) {
		return normalizeClassName(name).toUpperCase();
	}

	public static String capitalizeFirst(String s) {
		StringBuilder sb = new StringBuilder(s.trim().toLowerCase());
		sb.setCharAt(0, Character.toUpperCase(sb.charAt(0)));
		for (int i = 1; i < sb.length(); i++)
			if (!Character.isLetterOrDigit(sb.charAt(i - 1)))
				sb.setCharAt(i, Character.toUpperCase(sb.charAt(i)));
		return sb.toString();
	}

	static final class NodeListWrapper extends AbstractList<Node>
			implements RandomAccess {
		private final NodeList list;

		NodeListWrapper(NodeList l) {
			list = l;
		}

		public Node get(int index) {
			return list.item(index);
		}

		public int size() {
			return list.getLength();
		}
	}
}
