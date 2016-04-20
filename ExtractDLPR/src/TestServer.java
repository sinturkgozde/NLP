import java.io.*;
import java.net.*;
import java.security.*;

import edu.stanford.nlp.ie.AbstractSequenceClassifier;
import edu.stanford.nlp.ie.crf.CRFClassifier;

public class TestServer {
	static AbstractSequenceClassifier classifier;
	private static int port = 3150, maxConnections = 0;

	// Listen for incoming connections and handle them
	public static void main(String[] args) {

		int i = 0;

		try {
			classifier = CRFClassifier
					.getClassifierNoExceptions("classifiers/english.all.3class.distsim.crf.ser.gz");
			ServerSocket listener = new ServerSocket(port);
			Socket server;

			while ((i++ < maxConnections) || (maxConnections == 0)) {
				doComms connection;

				server = listener.accept();
				doComms conn_c = new doComms(server);
				Thread t = new Thread(conn_c);
				t.start();
			}
		} catch (IOException ioe) {
			// System.out.println("IOException on socket listen: " + ioe);
			ioe.printStackTrace();
		}
	}

}

class doComms implements Runnable {
	private Socket server;
	private String line, input;

	doComms(Socket server) {
		this.server = server;
	}

	public void run() {

		input = "";

		try {
			// Get input from the client
			DataInputStream in = new DataInputStream(server.getInputStream());
			PrintStream out = new PrintStream(server.getOutputStream());

			while ((line = in.readLine()) != null) {

				TestServer.classifier.classifyToString(line);
				System.out
						.println(TestServer.classifier.classifyToString(line));
				out.print(TestServer.classifier.classifyToString(line));
				input = input + line;

			}

			out.println("Overall message is:" + input);

			server.close();
		} catch (IOException ioe) {
			ioe.printStackTrace();
		}
	}
}
